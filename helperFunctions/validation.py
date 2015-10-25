from sendMessages import printParent
from sendMessages import messageParent
from sendMessages import obviousPrint

def dataDescription(arr):
    expectedValues = {
        'id': False,
        'output': False
    }
    allowableValues = ['id','output','continuous','categorical']

    for name in arr:
        try:
            allowableValues.index(name)
            expectedValues[name] = True
        except:
            printParent('Warning, we have received a value in the first row that is not valid:')
            printParent(name)
            printParent('Please remember that the first row must contain information describing that column of data')
            printParent('Acceptable values are: "ID", "Output", "Continuous", and "Categorical"')
            raise
    if( not expectedValues['id'] ):
        printParent('Warning, there is no column with an "ID" label in the first row')
        raise TypeError('dataDescription row incomplete')
    if( not expectedValues['output'] ):
        printParent('Warning, there is no column with an "Output" label in the first row')
        raise TypeError('dataDescription row incomplete')

def rowLength( row, expectedRowLength, rowCount ):
    if len( row ) != expectedRowLength:
        printParent( 'This row did not have the same number of columns as the dataDescription row.')
        printParent( row )
        printParent( 'This is row number:')
        printParent( rowCount )
        printParent( 'Please make sure that all rows have the same number of columns, even if those values are blank')
        printParent( 'And it might be worth double checking that your dataDescription row has an accurate description for each column in the dataset')

def testingHeaderRow( row, expectedRowLength ):
    if len( row ) != expectedRowLength:
        printParent('len(row)')
        printParent(len(row))
        printParent('len( outputData[ 0 ]')
        printParent(len( outputData[ 0 ] ) )
        printParent('we noticed that the testing and training datasets have different numbers of columns')
        printParent('we are going to assume that the "Output" column(s) is(are) simply not included for the testing dataset.')
        return False
    return True

def testingRowLength( row, expectedRowLength, rowCount ):
    if len( row ) != expectedRowLength:
        printParent( 'This row did not have the same number of columns as the testing dataset header row.')
        printParent( row )
        printParent( 'Within the testing dataset, this is row number:')
        printParent( rowCount )
        printParent( 'Please make sure that all rows have the same number of columns, even if those values are blank')

