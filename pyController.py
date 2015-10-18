import os
import os.path as path
import sys
import time
import json
import numpy as np
from sendMessages import printParent
from sendMessages import messageParent
from sendMessages import obviousPrint

import concat
import minMax
import imputingMissingValues
import listToDict
import dictVectorizing
import featureSelecting
import writeToFile
import brainjs

# grab arguments
args = json.loads( sys.argv[1] )
trainingFile = args['trainingData']
testingFile = args['testingData']
test = args['test']

concattedResults = concat.inputFiles(trainingFile, testingFile)

# we are identifying whether each column is "output","id","categorical", or "continuous"
dataDescription = concattedResults[0]
headerRow = concattedResults[1]
del headerRow[ dataDescription.index('id') ]
dataDescription.remove('id')
del headerRow[ dataDescription.index('output') ]
dataDescription.remove('output')

trainingLength = concattedResults[2]
args['trainingLength'] = trainingLength
X = concattedResults[3]
idColumn = concattedResults[4]
outputColumn = concattedResults[5]

if(test):
    messageParent([dataDescription, headerRow, trainingLength, X], 'concat.py')


X = imputingMissingValues.cleanAll(dataDescription, trainingLength, X)

if(test):
    messageParent([X, idColumn, outputColumn], 'imputingMissingValues.py')

# 3. convert entire dataset to have categorical data encoded properly
listOfDicts = listToDict.all(X, headerRow)
vectorizedInfo = dictVectorizing.vectorize(listOfDicts)
X = vectorizedInfo[0].tolist()
vectorizedHeaderRow = vectorizedInfo[1]

if(test):
    # the data become too big to send over in one huge string, so we are splitting it up into two separate messages
    messageParent( X[0:150000], 'dictVectorizing.py' )
    messageParent( X[150000:], 'dictVectorizing.py' )

# immediate next steps:
    # 4. run training data through rfecv- fit_transform
        # make sure that rfecv is saved and written to file!
    # 5. run testing data through that same rfecv to make sure it's handled in the exact same way

# passing in a value of 0.001 as the featureImportanceThreshold number means we are only eliminating features that are close to meaningless. 
featureSelectingResults = featureSelecting.select(X, outputColumn, trainingLength, 0.001, vectorizedHeaderRow, test )
X = featureSelectingResults[0]
filteredHeaderRow = featureSelectingResults[1]

# write results to file
writeToFile.writeMetadata( outputColumn, idColumn, args, filteredHeaderRow )
writeToFile.writeData(X, args, filteredHeaderRow )

if(test):
    messageParent(X.tolist(), 'featureSelecting.py')

brainX = brainjs.format( X, outputColumn, idColumn, args )
if( test ):
    messageParent( brainX, 'brainjs.py' )



