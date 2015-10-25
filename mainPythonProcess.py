import os
import os.path as path
import sys
import time
import json
import numpy as np

# some functions to help with logging
from helperFunctions.sendMessages import printParent
from helperFunctions.sendMessages import messageParent
from helperFunctions.sendMessages import obviousPrint

# here are all the individual files that do most of the work. 
# mainPythonProcess.py mostly just coordinates and lays out the order
from helperFunctions import concat
from helperFunctions import removeUniques
from helperFunctions import imputingMissingValues
from helperFunctions import listToDict
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
concattedResults = concat.inputFiles(trainingFile, testingFile)

# dataDescription identifies whether each column is "output","id","categorical", or "continuous"
dataDescription = concattedResults[0]
headerRow = concattedResults[1]

# save the pretty name for the ID column
idHeader = headerRow[ dataDescription.index('id') ]
# save the pretty name for the output column
outputHeader = headerRow[ dataDescription.index('output') ]
args['idHeader'] = idHeader
args['outputHeader'] = outputHeader

# we have already saved id and output into separate columns, so we need to remove those from our headerRow and dataDescription
del headerRow[ dataDescription.index('id') ]
dataDescription.remove('id')
del headerRow[ dataDescription.index('output') ]
dataDescription.remove('output')

# trainingLength is the length of the training data set, so we can separate training and testing at the end
trainingLength = concattedResults[2]
args['trainingLength'] = trainingLength

X = concattedResults[3]
idColumn = concattedResults[4]
outputColumn = concattedResults[5]

# throughout this file, we will send messages back to the parent process if we are currently running the tests. 
if(test):
    messageParent([dataDescription, headerRow, trainingLength, X], 'concat.py')

# 2. Remove unique categorical values from the dataset
    # Unique categorical values are items like an individual person's name
    # Clearly, they are not broadly useful for making predictions, and contribute to overfitting
noUniquesResults = removeUniques.remove( X, dataDescription, headerRow )
X = noUniquesResults[ 0 ]

# some columns may contain only unique values. In that case, we will delete those columns, which will have an effect on dataDescription and headerRow
dataDescription = noUniquesResults[ 1 ]
headerRow = noUniquesResults[ 2 ]


# 2. fill in missing values. Please dive into this file to make sure your placeholder for missing values is included in the list we use. 
    # we are including args only so that we can write to files at the intermediate stages for debugging
    # TODO: remove args from this arguments list once debugging is finished. 
imputedValuesResults = imputingMissingValues.cleanAll(dataDescription, X, headerRow, args )
X = imputedValuesResults[ 0 ]
dataDescription = imputedValuesResults[ 1 ]
headerRow = imputedValuesResults[ 2 ]

# handle all these new return values in mainPythonProcess
# might have to tweak a test or two further down the line for this new number of columns. 
# writeToFile.writeData(imputedValuesResults, args, headerRow, False )

# writeToFile.writeData(X, args, headerRow, False )

if(test):
    messageParent([X, idColumn, outputColumn], 'imputingMissingValues.py')

# 3. convert entire dataset to have categorical data encoded properly. 
# This turns information like a single column holding city names of 'SF' and 'Akron' into two separate columns, one for 'Akron=True' and one for 'SF=True'.
# This is called one-hot encoding, and is a standard way of handling categorical data. 
listOfDicts = listToDict.all(X, headerRow)
vectorizedInfo = dictVectorizing.vectorize(listOfDicts)
X = vectorizedInfo[0].tolist()
vectorizedHeaderRow = vectorizedInfo[1]

if(test):
    # the data become too big to send over in one huge string, so we are splitting it up into two separate messages
    messageParent( X[0:150000], 'dictVectorizing.py' )
    messageParent( X[150000:], 'dictVectorizing.py' )



# 4. Feature Selection means picking only those features that are actually predictive and useful
    # say a column of names is passed in. This will then be turned into categorical data ("Suzy=True","Preston=True"), one for each name
    # clearly, this data is not going to be useful, unless we way overfit the training set. 
    # feature selection helps avoid such cases by only including the data that is actually predictive. 
    # this helps models train faster, and is actually more predictive in the end since there's less noise to distract from the valuable features. 
# passing in a value of 0.001 as the featureImportanceThreshold number means we are only eliminating features that are close to meaningless. 

featureSelectingResults = featureSelecting.select(X, outputColumn, trainingLength, 0.001, vectorizedHeaderRow, test )
X = featureSelectingResults[0]
filteredHeaderRow = featureSelectingResults[1]



# 5. write results to file
# this is the data we need for most scikit-learn algorithms!
writeToFile.writeMetadata( outputColumn, idColumn, args, filteredHeaderRow )
writeToFile.writeData(X, args, filteredHeaderRow, False )

if(test):
    messageParent(X.tolist(), 'featureSelecting.py')

# 6. for neural networks:
# normalize the data to be values between -1 and 1
X = minMax.normalize( X )
writeToFile.writeData(X, args, filteredHeaderRow, True )
if( test ):
    messageParent(X.tolist(), 'minMax.py')

# 7. format data specifically for brain.js, which takes a different format than scikit-neural-network
brainX = brainjs.format( X.tolist(), outputColumn, idColumn, args )
if( test ):
    messageParent( brainX, 'brainjs.py' )

printParent('we have written your fully transformed data to a folder at:')
printParent( args['outputFolder'] )

messageParent( '', 'finishedFormatting' )
