import concat
import sys
from sendMessages import printParent
from sendMessages import messageParent
from sendMessages import obviousPrint
# grab arguments
trainingFile = sys.argv[1]
testingFile = sys.argv[2]
test = sys.argv[3]

concattedResults = concat.inputFiles(trainingFile, testingFile)

if(test):
    messageParent(concattedResults, 'concat.py')

