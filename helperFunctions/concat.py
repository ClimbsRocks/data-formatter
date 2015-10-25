import csv
import validation
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

        rowCount = 0
        for row in trainingRows:
            if rowCount < 2:
                # grab the dataDescription row and the header row, and make them both lowercase
                if rowCount == 0:
                    expectedRowLength = len( row )
                    dataDescription = [x.lower() for x in row]
                    validation.dataDescription( dataDescription )
                else: 
                    validation.rowLength( row, expectedRowLength, rowCount )
                    headerRow = [x.lower() for x in row]
            else:
                validation.rowLength( row, expectedRowLength, rowCount )
                trimmedRow = []
                for idx, val in enumerate(row):
                    if dataDescription[idx] == 'id':
                        idColumn.append(val)
                    elif dataDescription[idx] == 'output':
                        outputColumn.append(val)
                    else:
                        trimmedRow.append(val)

                outputData.append(trimmedRow)

            # keep track of which row we are on for error logging purposes
            rowCount = rowCount + 1

        # keep track of how long our training data set is so we can split back out again later
        trainingLength = len(outputData)

    with open(testingFile, 'rU') as testingInput:
        # detect the dialect of the csv file
        dialect = csv.Sniffer().sniff(testingInput.read(1024))
        testingInput.seek(0)

        testingRows = csv.reader(testingInput, dialect)
        testingRowCount = 0

        # set missingOutputIndex equal to infinity to start with
        missingOutputIndex = float('inf')

        for row in testingRows:
            if testingRowCount == 0:

                # check to see that we have the same number of columns in the testing set as the training set
                colsValidated = validation.testingHeaderRow( row, expectedRowLength, headerRow )
                if colsValidated == False:
                    # if not, assume that the missing column is the output column, and store that index position
                    missingOutputIndex = dataDescription.index('output')
                # skip the first row
                expectedTestingRowLength = len( row )
            else:
                validation.testingRowLength( row, expectedTestingRowLength, testingRowCount )
                trimmedRow = []
                for idx, val in enumerate(row):
                    # if this is the missing column that was supposed to be the output column, move the idx variable up by one to account for skipping over that column
                        # the idx variable is only used to look for whether this is the id or output column, and is not used to determine hte value
                    if idx >= missingOutputIndex:
                        idx = idx + 1
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
            testingRowCount += 1

    return [dataDescription, headerRow, trainingLength, outputData, idColumn, outputColumn]
