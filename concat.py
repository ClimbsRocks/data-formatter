import csv
from sendMessages import printParent
from sendMessages import messageParent
from sendMessages import obviousPrint


def inputFiles(trainingFile, testingFile):
    outputData = []
    idColumn = []
    outputColumn = []
    with open(trainingFile, 'rU') as trainingInput:
        trainingRows = csv.reader(trainingInput)
        firstRow = 0
        for row in trainingRows:
            if firstRow < 2:
                if firstRow == 0:
                    dataDescription = [x.lower() for x in row]
                else: 
                    headerRow = [x.lower() for x in row]
                firstRow = firstRow + 1
            else:
                trimmedRow = []
                for idx, val in enumerate(row):
                    if dataDescription[idx] == 'id':
                        # printParent('had an id event!')
                        # printParent(val)
                        idColumn.append(val)
                    elif dataDescription[idx] == 'output':
                        outputColumn.append(val)
                    else:
                        trimmedRow.append(val)

                outputData.append(trimmedRow)
        trainingLength = len(outputData)

    with open(testingFile, 'rU') as testingInput:
        testingRows = csv.reader(testingInput)
        firstRow = True
        for row in testingRows:
            if firstRow:
                firstRow = False
            else:
                trimmedRow = []
                for idx, val in enumerate(row):
                    if dataDescription[idx] == 'id':
                        # printParent('had an id event!')
                        # printParent(val)
                        idColumn.append(val)
                    elif dataDescription[idx] == 'output':
                        outputColumn.append(val)
                    else:
                        trimmedRow.append(val)

                outputData.append(trimmedRow)
    return [dataDescription, headerRow, trainingLength, outputData, idColumn, outputColumn]
