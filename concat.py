import csv
from sendMessages import printParent
from sendMessages import messageParent
from sendMessages import obviousPrint


def inputFiles(trainingFile, testingFile):
    # we will break out separately the ID column, the output column, and then the rest of the data
    outputData = []
    idColumn = []
    outputColumn = []

    with open(trainingFile, 'rU') as trainingInput:
        # detect the "dialect" of this type of csv file
        dialect = csv.Sniffer().sniff(trainingInput.read(1024))
        trainingInput.seek(0)
        trainingRows = csv.reader(trainingInput, dialect)

        firstRow = 0
        for row in trainingRows:
            if firstRow < 2:
                # grab the dataDescription row and the header row, and make them both lowercase
                if firstRow == 0:
                    dataDescription = [x.lower() for x in row]
                else: 
                    headerRow = [x.lower() for x in row]
                firstRow = firstRow + 1
            else:
                trimmedRow = []
                for idx, val in enumerate(row):
                    if dataDescription[idx] == 'id':
                        idColumn.append(val)
                    elif dataDescription[idx] == 'output':
                        outputColumn.append(val)
                    else:
                        trimmedRow.append(val)

                outputData.append(trimmedRow)
        trainingLength = len(outputData)

    with open(testingFile, 'rU') as testingInput:
        # detect the dialect of the csv file
        dialect = csv.Sniffer().sniff(testingInput.read(1024))
        testingInput.seek(0)

        testingRows = csv.reader(testingInput, dialect)
        firstRow = True
        for row in testingRows:
            if firstRow:
                # skip the first row
                firstRow = False
            else:
                trimmedRow = []
                for idx, val in enumerate(row):
                    if dataDescription[idx] == 'id':
                        idColumn.append(val)
                    elif dataDescription[idx] == 'output':
                        outputColumn.append(val)
                    else:
                        trimmedRow.append(val)
                # NOTE: we are appending both the training and the testing data into one dataset
                # this ensures we will be processing them consistently
                    # if we treated them separately, it could cause an issue if we have a feature present in the testing data but not the training data, for example
                outputData.append(trimmedRow)

    return [dataDescription, headerRow, trainingLength, outputData, idColumn, outputColumn]
