import os
import os.path as path
import sys
import time
import json
import numpy as np

from scipy.sparse import hstack

# some functions to help with logging
from helperFunctions.sendMessages import printParent
from helperFunctions.sendMessages import messageParent
from helperFunctions.sendMessages import obviousPrint

# here are all the individual files that do most of the work. 
# mainPythonProcess.py mostly just coordinates and lays out the order
from helperFunctions import concat
from helperFunctions import join
from helperFunctions import groupBy
from helperFunctions import featureEngineering
from helperFunctions import sumById
from helperFunctions import removeUniques
from helperFunctions import polynomialFeatures
from helperFunctions import imputingMissingValues
from helperFunctions import listToDict
from helperFunctions import noUniquesRedux
from helperFunctions import dictVectorizing
from helperFunctions import featureSelecting
from helperFunctions import minMax
from helperFunctions import brainjs
from helperFunctions import writeToFile


# grab arguments
args = json.loads( sys.argv[1] )
trainingFile = args['trainingData']
testingFile = args['testingData']
test = args['test']

# 1. concatenate together the training and testing data sets
# this ensures that whatever transitions we perform in data-formatter will be equally applied to both the training and testing data set
# dataDescription identifies whether each column is "output","id","categorical", or "continuous"
dataDescription, headerRow, trainingLength, X, idColumn, outputColumn, idHeader, problemType, dataDescriptionRaw, hasCustomValidationSplit, validationSplitColumn = concat.inputFiles(trainingFile, testingFile)
if args['verbose'] != 0:
    printParent('finished concatting the training and testing files together')


labelEncoded = False
labelMapping = None
try:
    for val in outputColumn:
        val = float(val)
except:
    labelEncoded = True
    # build a list of all the unique values in outputColumn
    uniqueOutputVals = list(set(outputColumn))
    labelMapping = {}
    for idx, val in enumerate(uniqueOutputVals):
        labelMapping[val] = idx
    for idx, val in enumerate(outputColumn):
        outputColumn[idx] = labelMapping[val]

messageParent({
    'labelEncoded': labelEncoded,
    'labelMapping': labelMapping
    }, 'fileNames')


# for development purposes, take a consistent tiny subset of the data
# X = [x for rowIdx, x in enumerate(X) if rowIdx % 100 == 0]



# save the pretty name for the output column
outputHeader = headerRow[ dataDescription.index('output') ]
args['idHeader'] = idHeader
args['outputHeader'] = outputHeader

# we have already saved id and output into separate columns, so we need to remove those from our headerRow and dataDescription
# once we have removed the values we are not using, we can use dataDescriptionRaw to create dateIndices and groupByIndices
try:
    # the user does not have to pass in an id header or a validation split for the training data
    del headerRow[ dataDescription.index('id') ]
    del dataDescriptionRaw[ dataDescription.index('id') ]
    dataDescription.remove('id')

    del headerRow[ dataDescription.index('validation split') ]
    del dataDescriptionRaw[ dataDescription.index('validation split') ]
    dataDescription.remove('validation split')
except:
    pass
del headerRow[ dataDescription.index('output') ]
del dataDescriptionRaw[ dataDescription.index('output') ]
dataDescription.remove('output')

# we have ignored the data in the "IGNORE" columns, but now we need to remove those identifiers from headerRow and dataDescription
ignoredIndices = [idx for idx, x in enumerate(dataDescription) if x == 'ignore']
for index in reversed(ignoredIndices):
    del headerRow[index]
    del dataDescription[index]
    del dataDescriptionRaw[index]

groupByIndices = []
dateIndices = []
nlpIndices = []
for colIndex, colType in enumerate(dataDescriptionRaw):
    if colType == 'date':
        dateIndices.append(colIndex)
    elif colType == 'nlp':
        nlpIndices.append(colIndex)
    elif colType[0:7] == 'groupby':
        groupByIndices.append(colIndex)

# trainingLength is the length of the training data set, so we can separate training and testing at the end
args['trainingLength'] = trainingLength

# throughout this file, we will send messages back to the parent process if we are currently running the tests. 
if(test):
    messageParent([dataDescription, headerRow, trainingLength, X], 'concat.py')


if args['joinFileName'][-4:] == '.csv':
    X, dataDescription, headerRow, groupByIndices, dateIndices = join.datasets(X, args['joinFileName'], headerRow, dataDescription, args, groupByIndices, dateIndices)

if test:
    messageParent([X, dataDescription, headerRow, problemType], 'join.py')
if args['verbose'] != 0:
    printParent('finished joining the data')

# 2. Perform some feature engineering:

# 2A. if we have a date column, do some feature engineering on it!
# this functionality is mostly complete, but hasn't been finished yet
# NOTE: you can only pass in a single date column for now.
if len(dateIndices) > 0:
    X, dataDescription, headerRow = featureEngineering.dates(X, dataDescription, headerRow )

# 2B. if we have some text, perform some nlp transformations on it
if len(nlpIndices) > 0:
    X, nlpColumns, nlpDataDescription, nlpHeaderRow = featureEngineering.nlp(X, dataDescription, headerRow )

# 3. if the user asked us to group by anything, do so!
if len(groupByIndices) > 0:
    X, dataDescription, headerRow = groupBy.compute(X, groupByIndices, dataDescription, headerRow, outputColumn, trainingLength )


# 2. Remove unique categorical values from the dataset
    # Unique categorical values are items like an individual person's name
    # Clearly, they are not broadly useful for making predictions, and contribute to overfitting
    # some columns may contain only unique values. In that case, we will delete those columns, which will have an effect on dataDescription and headerRow
X, dataDescription, headerRow = removeUniques.remove( X, dataDescription, headerRow )

if args['verbose'] != 0:
    printParent('finished removing non-unique categorical values')


# 3. fill in missing values. Please dive into this file to make sure your placeholder for missing values is included in the list we use. 

X, dataDescription, headerRow = imputingMissingValues.cleanAll(dataDescription, X, headerRow )

if(test):
    messageParent([X, idColumn, outputColumn], 'imputingMissingValues.py')

if args['verbose'] != 0:
    printParent('finished imputing missing values')

# 3. create all the interactions between features
# this will take all features, and create new features that are the interactions between them (multiplied together)
# this step can add huge amounts of space complexity, and is a good place to check if concerned about memory
# because of the memory issues, we do not run this by default, and will only run it if you tell us to. 
if args['allFeatureCombinations']:
    X, headerRow, dataDescription = polynomialFeatures.addAll(X, headerRow, dataDescription)
    if args['verbose'] != 0:
        printParent('finished trying to add in combinations of the existing features as new features')

# 4. if we have a single ID spread across multiple rows, sum by ID so that each ID ends up being only a single row with the aggregated results of all the relevant rows
X, idColumn, trainingLength, outputColumn = sumById.sum(dataDescription, X, headerRow, idColumn, trainingLength, outputColumn)

args['trainingLength'] = trainingLength
args['testingLength'] = len(X) - args['trainingLength']

if(test):
    messageParent([X, idColumn, trainingLength, outputColumn], 'sumById.py')

if args['verbose'] != 0:
    printParent('finished grouping by ID if relevant')

# 3. convert entire dataset to have categorical data encoded properly. 
# This turns information like a single column holding city names of 'SF' and 'Akron' into two separate columns, one for 'Akron=True' and one for 'SF=True'.
# This is called one-hot encoding, and is a standard way of handling categorical data. 
X, vectorizedHeaderRow = dictVectorizing.vectorize(X)

if args['verbose'] != 0:
    printParent('finished vectorizing the categorical values')

if(test):
    try:
        # the data become too big to send over in one huge string, so we are splitting it up into two separate messages
        messageParent( X[0:150000].toarray().tolist(), 'dictVectorizing.py' )
        messageParent( X[150000:].toarray().tolist(), 'dictVectorizing.py' )
    except:
        messageParent( X.toarray().tolist(), 'dictVectorizing.py' )


# 4. Feature Selection means picking only those features that are actually predictive and useful
    # say a column of names is passed in. This will then be turned into categorical data ("Suzy=True","Preston=True"), one for each name
    # clearly, this data is not going to be useful, unless we way overfit the training set. 
    # feature selection helps avoid such cases by only including the data that is actually predictive. 
    # this helps models train faster, and is actually more predictive in the end since there's less noise to distract from the valuable features. 
# passing in a value of 0.001 as the featureImportanceThreshold number means we are only eliminating features that are close to meaningless. 

if not args['keepAllFeatures']:
    X, headerRow = featureSelecting.select(X, outputColumn, args['trainingLength'], 0.001, vectorizedHeaderRow, test, problemType )
    # X = featureSelectingResults[0]
    # headerRow = featureSelectingResults[1]

    if args['verbose'] != 0:
        printParent('finished running feature selecting')

# 5. write results to file
# this is the data we need for most scikit-learn algorithms!
writeToFile.writeMetadata( outputColumn, idColumn, args, headerRow, validationSplitColumn, hasCustomValidationSplit )

# if we have nlp data, append it now
try:
    X = hstack([X,nlpColumns], format='csr')
    headerRow = headerRow + nlpHeaderRow
except:
    pass
    
writeToFile.writeDataSparse(X, args, headerRow, False )

if(test):
    messageParent(X.toarray().tolist(), 'featureSelecting.py')

# 6. for neural networks:
# normalize the data to be values between -1 and 1
X = minMax.normalize( X, False )
if problemType == 'regression':
    outputColumn = minMax.normalize( outputColumn[0:trainingLength], True )
writeToFile.writeDataSparse(X, args, headerRow, outputColumn[0:trainingLength] )

if( test ):
    messageParent(X.toarray().tolist(), 'minMax.py')

# # 7. format data specifically for brain.js, which takes a different format than scikit-neural-network
# # this module is currently deprecated until someone requests it again. 
# brainX = brainjs.format( X.tolist(), outputColumn, idColumn, args )
# # if( test ):
# #     messageParent( brainX, 'brainjs.py' )

messageParent({
    'trainingDataLength': args['trainingLength'],
    'testingDataLength': args['testingLength'],
    'problemType': problemType
}, 'fileNames')

printParent('we have written your fully transformed data to a folder at:')
printParent( args['outputFolder'] )

messageParent( '', 'finishedFormatting' )
