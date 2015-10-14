import sys
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

# grab arguments
trainingFile = sys.argv[1]
testingFile = sys.argv[2]
test = sys.argv[3]

concattedResults = concat.inputFiles(trainingFile, testingFile)

# we are identifying whether each column is "output","id","categorical", or "continuous"
dataDescription = concattedResults[0]
headerRow = concattedResults[1]
del headerRow[ dataDescription.index('id') ]
dataDescription.remove('id')
del headerRow[ dataDescription.index('output') ]
dataDescription.remove('output')

trainingLength = concattedResults[2]
allData = concattedResults[3]
idColumn = concattedResults[4]
outputColumn = concattedResults[5]

if(test):
    messageParent([dataDescription, headerRow, trainingLength, allData], 'concat.py')


imputedResults = imputingMissingValues.cleanAll(dataDescription, trainingLength, allData)

if(test):
    messageParent([imputedResults, idColumn, outputColumn], 'imputingMissingValues.py')

# 3. convert entire dataset to have categorical data encoded properly
listOfDicts = listToDict.all(imputedResults, headerRow)
vectorized = dictVectorizing.vectorize(listOfDicts)

if(test):
    # the data become too big to send over in one huge string, so we are splitting it up into two separate messages
    messageParent(vectorized.tolist()[0:150000], 'dictVectorizing.py' )
    messageParent(vectorized.tolist()[150000:], 'dictVectorizing.py' )

# immediate next steps:
    # 4. run training data through rfecv- fit_transform
        # make sure that rfecv is saved and written to file!
    # 5. run testing data through that same rfecv to make sure it's handled in the exact same way
# featureSelectedResults = featureSelecting.select(vectorized, outputColumn)

    # 6. at this point, we are ready to start considering specific formatting (min-max, brain.js, and sci-kit learn)


# minMaxNormalizedResults = minMax.normalize(dataDescription, imputedResults)

# if(test):
#     messageParent( [minMaxNormalizedResults, idColumn, outputColumn], 'minMax.py')

