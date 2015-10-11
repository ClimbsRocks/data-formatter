from sendMessages import printParent
from sendMessages import messageParent
from sendMessages import obviousPrint
import concat
# grab arguments
trainingFile = sys.argv[0]
testingFile = sys.argv[1]
test = sys.argv[3]

concattedResults = concat.inputFiles(trainingFile, testingFile)

if(test):
    messageParent(concattedResults, 'concat.py')

