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
