import sys
from sendMessages import printParent
from sendMessages import messageParent
from sendMessages import obviousPrint

import concat
import minMax
import imputingMissingValues

# grab arguments
trainingFile = sys.argv[1]
testingFile = sys.argv[2]
test = sys.argv[3]

concattedResults = concat.inputFiles(trainingFile, testingFile)

# we are identifying whether each column is "output","id","categorical", or "numerical"
dataDescription = [x.lower() for x in concattedResults[0]]
headerRow = [x.lower() for x in concattedResults[1]]
trainingLength = concattedResults[2]
allData = concattedResults[3]

if(test):
    messageParent([dataDescription, headerRow, trainingLength, allData], 'concat.py')


imputedResults = imputingMissingValues.cleanAll(dataDescription, trainingLength, allData)

if(test):
    messageParent(imputedResults, 'imputingMissingValues.py')


# minMaxNormalizedResults = minMax.normalize(allData)

# if(test):
#     messageParent(minMaxNormalizedResults, 'minMax.py')

