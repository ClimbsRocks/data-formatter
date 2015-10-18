import minMax
import writeToFile
import os
import os.path as path
import csv
import json
import writeToFile
from sendMessages import printParent
from sendMessages import messageParent
from sendMessages import obviousPrint

def format( X, y, idColumn, args ):
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

    with open( path.join( args['outputFolder'], 'brainJS' + args['trainingFile'] ), 'w+') as outputFile:
        csvOutputFile = csv.writer(outputFile)
        for rowIndex, row in enumerate(brainArr):
            if( rowIndex < args['trainingLength'] ):
                csvOutputFile.writerow( [ row ] )

    with open( path.join( args['outputFolder'], 'brainJS' + args['testingFile'] ), 'w+') as outputFile:
        csvOutputFile = csv.writer(outputFile)
        for rowIndex, row in enumerate(brainArr):
            if( rowIndex >= args['trainingLength'] ):
                csvOutputFile.writerow( [ row ] )

    printParent('we have written your fully transformed brainJS data to a file at:')
    printParent( args['outputFolder'] )

    return brainArr
