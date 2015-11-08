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
                    dataDescriptionRaw = [x.lower() for x in row]
                    hasID, testHeaderValidationLength = validation.dataDescription( dataDescriptionRaw )

                    # the user told us whether this is 'output regression' or 'output category'
                    # we need to split out the problem type (regression or category), and leave only 'output'
                    dataDescription = []
                    for columnType in dataDescriptionRaw:
                        if columnType[0:6] == 'output':
                            dataDescription.append('output')
                            problemType = columnType[7:]
                        else:
                            dataDescription.append(columnType)

                else: 
                    validation.rowLength( row, expectedRowLength, rowCount )
                    headerRow = [x.lower() for x in row]
            else:
                validation.rowLength( row, expectedRowLength, rowCount )
                trimmedRow = []
                if hasID == False:
                    # while we won't be using these IDs, we do need to make sure our idColumn has the right number of rows, so we are putting them in here. 
                    idColumn.append( 'trainID' + str(rowCount) )

                for idx, val in enumerate(row):
                    if dataDescription[idx] == 'id':
                        idColumn.append(val)
                    elif dataDescription[idx] == 'output':
                        outputColumn.append(val)
                    elif dataDescription[idx] == 'ignore':
                        # some columns contain data we do not want to use. It seems trivial to remove these from our dataset here, rather than forcing them to try to open the dataset up in some other program to attempt to delete the column. 
                        pass
                    else:
                        trimmedRow.append(val)

                outputData.append(trimmedRow)
            # keep track of which row we are on for error logging purposes
            rowCount += 1

        # keep track of how long our training data set is so we can split back out again later
        trainingLength = len(outputData)

    with open(testingFile, 'rU') as testingInput:
        # detect the dialect of the csv file
        dialect = csv.Sniffer().sniff(testingInput.read(1024))
        testingInput.seek(0)

        testingRows = csv.reader(testingInput, dialect)
        testingRowCount = 0

        # if the user passes in their own dataDescription row for the testing set, use it!
        # but by default, we will use the standard dataDescription row from the training data
        testingDataDescription = dataDescription

        # set missingOutputIndex equal to infinity to start with
        missingOutputIndex = float('inf')

        for row in testingRows:
            if testingRowCount == 0:
                if validation.isTestingDataDescription(row):
                    # if we have a dataDescription row for our testing dataset, use it! and acknowledge that the next row is our standard header row
                    testingRowCount -= 1
                    testingDataDescription = [x.lower() for x in row]
                else:
                    testingHeader = row
                    # check to see if we find the words "continuous" or "categorical" in this row
                        # if we do, then set testingDataDescription equal to this row
                        # if we don't, we can proceed as normal.
                        # define testingDataDescription above as being equal to normal dataDescription by default.
                        # check to make sure that with all the IGNOREs considered, we have the right number of columns

                    # check to see that we have the same number of columns in the testing set as the training set
                    colsValidated = validation.testingHeaderRow( row, expectedRowLength, headerRow )
                    if colsValidated == False:
                        # if not, assume that the missing column is the output column, and store that index position
                        missingOutputIndex = dataDescription.index('output')
                    # skip the first row
                    expectedTestingRowLength = len( row )
            else:
                # build up each row in the testing dataset
                validation.testingRowLength( row, expectedTestingRowLength, testingRowCount )
                trimmedRow = []
                for idx, val in enumerate(row):
                    if testingDataDescription[idx] == 'id':
                        idColumn.append(val)
                    elif testingDataDescription[idx] == 'output':
                        outputColumn.append(val)
                    elif testingDataDescription[idx] == 'ignore':
                        pass
                    else:
                        trimmedRow.append(val)
                # NOTE: we are appending both the training and the testing data into one dataset
                # this ensures we will be processing them consistently
                    # if we treated them separately, it could cause an issue if we have a feature present in the testing data but not the training data, for example
                outputData.append(trimmedRow)
            testingRowCount += 1

    try:
        idHeader = headerRow[ dataDescription.index('id') ]
    except:
        idHeader = testingHeader[ testingDataDescription.index('id') ]
    return [dataDescription, headerRow, trainingLength, outputData, idColumn, outputColumn, idHeader, problemType]
