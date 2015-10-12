import csv
from sendMessages import printParent
from sendMessages import messageParent
from sendMessages import obviousPrint

def inputFiles(trainingFile, testingFile):
    outputData = []
    with open(trainingFile, 'rU') as trainingInput:
        trainingRows = csv.reader(trainingInput)
        firstRow = 0
        for row in trainingRows:
            if firstRow < 2:
                if firstRow == 0:
                    dataDescription = row
                else: 
                    headerRow = row
                firstRow = firstRow + 1
            else:
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

    return [dataDescription, headerRow, trainingLength, outputData]
