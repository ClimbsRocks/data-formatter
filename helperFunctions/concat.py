import csv
import os
import validation
import ntpath
from sendMessages import printParent
from sendMessages import messageParent
from sendMessages import obviousPrint

def removeHeaderRows(fileName):
    cleanedFileName = 'temp' + ntpath.basename(fileName)
    with open(fileName,'rU') as f:
        with open(cleanedFileName,'w+') as f1:
            rowCount = 0
            for row in f:
                if rowCount == 0:
                    dataDescription = row.rstrip('\r\n').split(",")
                    rowCount += 1
                else:
                    f1.write(row)
    # os.remove(cleanedFileName)
    return cleanedFileName, dataDescription



def inputFiles(trainingFile, testingFile):

    # we have two "header" rows before the data actually starts, which will throw off our csv parser
    trainingFile, dataDescriptionLine = removeHeaderRows(trainingFile)
    testingFile, testingDataDescriptionLine = removeHeaderRows(testingFile)


    # grab the dataDescription row and make it lowercase
    expectedRowLength = len( dataDescriptionLine )
    dataDescriptionRaw = [x.lower() for x in dataDescriptionLine]
    hasID, testHeaderValidationLength, hasCustomValidationSplit = validation.dataDescription( dataDescriptionRaw )

    # the user told us whether this is 'output regression' or 'output category'
    # we need to split out the problem type (regression, category, or multi-category), and leave only 'output'
    dataDescription = []
    for columnType in dataDescriptionRaw:
        if columnType[0:6] == 'output':
            dataDescription.append('output')
            problemType = columnType[7:]
        elif columnType[0:8] == 'groupby ':
            dataDescription.append( columnType[8:] )
        else:
            dataDescription.append(columnType)


    testingDataDescription = [x.lower() for x in testingDataDescriptionLine]


    # we will break out separately the ID column, the output column, and then the rest of the data
    outputData = []
    idColumn = []
    validationSplitColumn = []
    outputColumn = []

    with open(trainingFile, 'rU') as trainingInput:
        # detect the "dialect" of this type of csv file
        try:
            dialect = csv.Sniffer().sniff(trainingInput.read(1024))
        except:
            dialect = 'excel'
        trainingInput.seek(0)
        trainingRows = csv.reader(trainingInput, dialect)

        rowCount = 0
        for row in trainingRows:
            # grab the header row and make it lowercase
            if rowCount == 0:
                validation.rowLength( row, expectedRowLength, rowCount )
                headerRow = [x.lower() for x in row]

            else:
                validation.rowLength( row, expectedRowLength, rowCount )
                trimmedRow = []
                if hasID == False:
                    # while we won't be using these IDs, we do need to make sure our idColumn has the right number of rows, so we are putting them in here. 
                    idColumn.append( int(rowCount + 8000000000) )

                for idx, val in enumerate(row):
                    if dataDescription[idx] == 'id':
                        idColumn.append(val)
                    elif dataDescription[idx] == 'validation split':
                        validationSplitColumn.append(val)
                    elif dataDescription[idx] == 'output':
                        # TODO: add in some error handling around making sure everything in the outputColumn is the same type.
                        try:
                            outputColumn.append(float(val))
                        except:
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


    # TODO TODO TODO: properly handle paring off the top line from our testing csv file

    with open(testingFile, 'rU') as testingInput:
        # detect the dialect of the csv file
        try:
            dialect = csv.Sniffer().sniff(testingInput.read(1024))
        except:
            dialect = 'excel'
        testingInput.seek(0)

        testingRows = csv.reader(testingInput, dialect)
        testingRowCount = 0


        # set missingOutputIndex equal to infinity to start with
        missingOutputIndex = float('inf')

        for row in testingRows:
            if testingRowCount == 0:
                testingHeader = [x.lower() for x in row]
                

                # check to make sure that with all the IGNOREs considered, we have the right number of columns
                colsValidated = validation.testingHeaderRow( row, expectedRowLength, headerRow )
                if colsValidated == False:
                    # if not, assume that the missing column is the output column, and store that index position
                    missingOutputIndex = dataDescription.index('output')
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


    os.remove(trainingFile)
    os.remove(testingFile)


    try:
        idHeader = headerRow[ dataDescription.index('id') ]
    except:
        idHeader = testingHeader[ testingDataDescription.index('id') ]

    return dataDescription, headerRow, trainingLength, outputData, idColumn, outputColumn, idHeader, problemType, dataDescriptionRaw, hasCustomValidationSplit, validationSplitColumn
