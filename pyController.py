import sys
from sendMessages import printParent
from sendMessages import messageParent
from sendMessages import obviousPrint

import concat
import minMax

# grab arguments
trainingFile = sys.argv[1]
testingFile = sys.argv[2]
test = sys.argv[3]

concattedResults = concat.inputFiles(trainingFile, testingFile)
allData = concattedResults[1]
trainingLength = concattedResults[0]

if(test):
    messageParent(concattedResults, 'concat.py')

minMaxNormalizedResults = minMax.normalize(allData)

if(test):
    messageParent(minMaxNormalizedResults, 'minMax.py')

