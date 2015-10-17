import minMax
import writeToFile
import os
import os.path as path
import csv
import json
from sendMessages import printParent
from sendMessages import messageParent
from sendMessages import obviousPrint

def format( X, y, idColumn ):
    X = minMax.normalize( X ).tolist()

    brainArr = []
    for rowIndex, row in enumerate(X):
        rowObj = {}
        # we might need to wrap output in an array if the output is a single number, like we have. 
            # input is an array, so 
        rowObj['output'] = []
        yRow = y[ rowIndex ]
        if( isinstance( yRow, list )):
            rowObj['output'].extend( yRow )
        else:
            # the output value is expected to be an array, so if y values are not arrays (they have no len() ability), then we need to wrap the y value in an array
            rowObj['output'].append( yRow )
        rowObj[ 'id' ] = idColumn[ rowIndex ]
            
        rowObj['input'] = row
        brainArr.append( rowObj )

    with open( path.join( os.getcwd(), 'brainJSData.csv' ), 'w+') as outputFile:
        csvOutputFile = csv.writer(outputFile)
        for row in brainArr:
            csvOutputFile.writerow( [ row ] )
        # csvOutputFile.writerows( brainArr )
        printParent('we have written your fully transformed data to a file at:')
        printParent( path.join( os.getcwd(), 'brainJSData.csv' ) )

    return brainArr
