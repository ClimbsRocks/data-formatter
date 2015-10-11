import csv
from sendMessages import printParent
from sendMessages import messageParent
from sendMessages import obviousPrint

def inputFiles(trainingFile, testingFile):
    outputData = []
    with open(trainingFile, 'rU') as trainingInput:
        trainingRows = csv.reader(trainingInput)
        for row in trainingRows:
            outputData.append(row)
        trainingLength = len(outputData)

    with open(testingFile, 'rU') as testingInput:
        testingRows = csv.reader(testingInput)
        firstRow = True
        for row in testingRows:
            if firstRow:
                firstRow = False
            else:
                outputData.append(row)

    return [trainingLength, outputData]
