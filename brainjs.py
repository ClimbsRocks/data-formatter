import minMax
import writeToFile
import os
import os.path as path
import csv
from sendMessages import printParent
from sendMessages import messageParent
from sendMessages import obviousPrint

def format( X, y, idColumn ):
    X = minMax.normalize( X )

    brainArr = []
    for rowIndex, row in enumerate(X):
        rowObj = {}
        # we might need to wrap output in an array if the output is a single number, like we have. 
            # input is an array, so 
        try:
            len( y[ rowIndex ])
            rowObj['output'] = y[ rowIndex ]
        except:
            # the output value is expected to be an array, so if y values are not arrays (they have no len() ability), then we need to wrap the y value in an array
            rowObj['output'] = [ y[ rowIndex ] ]
        rowObj[ 'id' ] = idColumn[ rowIndex ]
            
        rowObj['input'] = row
        brainArr.append( rowObj )

    # with open( path.join( os.getcwd(), 'brainJSData.csv' ), 'w+') as outputFile:
    #     csvOutputFile = csv.writer(outputFile)
    #     csvOutputFile.writerows( brainArr )
    #     printParent('we have written your fully transformed data to a file at:')
    #     printParent( path.join( os.getcwd(), 'brainJSData.csv' ) )

    return brainArr
        # get the feature name from the header row
        # set that equal to the column value
        # 
