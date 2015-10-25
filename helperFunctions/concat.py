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

        firstRow = 0
        for row in trainingRows:
            if firstRow < 2:
                # grab the dataDescription row and the header row, and make them both lowercase
                if firstRow == 0:
                    dataDescription = [x.lower() for x in row]
                    validation.dataDescription( dataDescription )
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

        # set missingOutputIndex equal to infinity to start with
        missingOutputIndex = float('inf')

        for row in testingRows:
            if firstRow:
                # check to see that we have the same number of columns in the testing set as the training set
                if len( row ) != len( outputData[ 0 ] ):
                    printParent('we noticed that the testing and training datasets have different numbers of columns')
                    printParent('we are going to assume that the "Output" column(s) is(are) simply not included for the testing dataset.')
                    # if not, assume that the missing column is the output column, and store that index position
                    missingOutputIndex = dataDescription.index('output')
                # skip the first row
                firstRow = False
            else:
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

    return [dataDescription, headerRow, trainingLength, outputData, idColumn, outputColumn]
