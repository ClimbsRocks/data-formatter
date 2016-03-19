from sendMessages import printParent
from sendMessages import messageParent
from sendMessages import obviousPrint

def dataDescription(arr):
    expectedTestRowLength = 0
    expectedValues = {
        'id': False,
        'output category': False,
        'output regression': False,
        'output multi-category': False,
        'nlp': False,
        'validation split': False
    }
    allowableValues = ['id','output category','output multi-category','output regression','continuous','categorical','date','ignore','validation split','nlp']


    for colIndex, name in enumerate(arr):

        # remove groupBy from in front of any other dataDescription words it might be paired with
        if name[0:8] == 'groupby ':
            name = name[8:]

        try:
            if name == 'output multicategory' or name == 'output multi category':
                name = 'output multi-category'
            allowableValues.index(name)
            expectedValues[name] = True
            # sometimes we will include columns in our training dataset that we will not include in our testing dataset. we want to allow for that
            # we already have logic in place for handling missing output values in our testing dataset. 
            if name not in ['ignore', 'validation split']:
                expectedTestRowLength += 1

        except:
            printParent('*********************************************************************')
            printParent('')
            printParent('Warning, we have received a value in the first row that is not valid:')
            printParent(name)
            printParent('Please remember that the first row must contain information describing that column of data')
            printParent('Acceptable values are: "ID", "Output Category", "Output Multi-Category", "Output Regression", "Continuous", "Categorical", "Date", "IGNORE", "Validation Split", and "NLP", though they are not case sensitive.')
            printParent('')
            printParent('The column index of this unexpected value is:')
            printParent(colIndex)
            printParent('The entire row that we received is:')
            printParent(str(arr))
            printParent('*********************************************************************')
            printParent('This is an error that prevents the rest of the prorgram from running. Please fix and run machineJS again.')
            printParent('')
            printParent('')
            printParent('')
            printParent('')
            raise
    if( not expectedValues['output category'] and not expectedValues['output regression'] and not expectedValues['output multi-category']):
        printParent('Warning, there is no column with an "Output" label in the first row')
        raise TypeError('dataDescription row incomplete')

    if( not expectedValues['id'] ):
        printParent('Warning, there is no column with an "ID" label in the first row')
        printParent('Not having an ID column is ok, as long as this is intentional.')
        # our testing dataset must have an id in it, so if our training data does not have an id column, we would expect our testing data to have one more column
        expectedTestRowLength += 1
        return False, expectedTestRowLength, expectedValues['validation split']
        raise TypeError('dataDescription row incomplete')

    # returning True means that we do have all the pieces we need to continue as normal
    return True, expectedTestRowLength, expectedValues['validation split']

def joinDataDescription(dataDescription):
    allowableValues = ['id','continuous','groupby continuous','categorical','groupby categorical','date','groupby date','ignore', 'validation split', 'nlp']

    for name in dataDescription:
        try:
            allowableValues.index(name)

        except:
            printParent('*********************************************************************')
            printParent('\n')
            printParent('Warning, we have received a value in the dataDescription row that is not valid:')
            printParent(name)
            printParent('The entire dataDescription row is:')
            printParent(dataDescription)
            printParent('Please remember that the first row must contain information describing that column of data')
            printParent('Acceptable values are: "ID", "Continuous", "Categorical", "Date", "IGNORE", "Validation Split", and "NLP", though they are not case sensitive')
            printParent('\n')
            printParent('*********************************************************************')
            printParent('This is an error that prevents the rest of the prorgram from running. Please fix and run machineJS again.')
            printParent('\n')
            printParent('\n')
            printParent('\n')
            printParent('\n')

            raise
    

def checkColumnCounts(row, expectedRowLength):
    # the testing data must have an ID, so we are not checking for that
    # don't count (ignore, even!) the ignore columns
    rowLength = len(row)
    ignoredColumns = [x for x in row if x =='ignore']
    rowLength -= len(ignoredColumns)
    if rowLength == expectedRowLength:
        return True
    else:
        return False

def rowLength( row, expectedRowLength, rowCount ):
    if len( row ) != expectedRowLength:
        printParent( 'This row did not have the same number of columns as the dataDescription row.')
        printParent( row )
        printParent( 'This is row number:')
        printParent( rowCount )
        printParent( 'Please make sure that all rows have the same number of columns, even if those values are blank')
        printParent( 'And it might be worth double checking that your dataDescription row has an accurate description for each column in the dataset')

def testingHeaderRow( row, expectedRowLength, trainingHeader ):
    if len( row ) != expectedRowLength:
        printParent('We noticed that the testing and training datasets have different numbers of columns.')
        printParent('We are going to assume that the "Output" column is simply not included for the testing dataset.')
        printParent( 'Here is the header row for the training data set:')
        printParent( trainingHeader )
        printParent( 'And here is the header row for your testing dataset:')
        row = [x.lower() for x in row]
        printParent( row )
        return False
    return True

def testingRowLength( row, expectedRowLength, rowCount ):
    if len( row ) != expectedRowLength:
        printParent( 'This row did not have the same number of columns as the testing dataset header row.')
        printParent( row )
        printParent( 'Within the testing dataset, this is row number:')
        printParent( rowCount )
        printParent( 'Please make sure that all rows have the same number of columns, even if those values are blank')

