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
    # we should be handling the min-max normalization in an earlier step
    # X = minMax.normalize( X ).tolist()

    brainArr = []
    for rowIndex, row in enumerate(X):
        rowObj = {}
        # we might need to wrap output in a list if the output is a single number, like we have. 
            # input is a list, so 
        rowObj['output'] = []
        yRow = y[ rowIndex ]
        if( isinstance( yRow, list )):
            rowObj['output'].extend( yRow )
        else:
            # the output value is expected to be a list, so if y values are not lists, then we need to wrap the y value in a list
            rowObj['output'].append( yRow )
        rowObj[ 'id' ] = idColumn[ rowIndex ]
            
        rowObj['input'] = row
        brainArr.append( rowObj )

    trainingFileName = path.split( args['trainingData'] )[ -1 ]
    testingFileName = path.split( args['testingData'] )[ -1 ]

    with open( path.join( args['outputFolder'], 'brainJS' + trainingFileName ), 'w+') as outputFile:
        csvOutputFile = csv.writer(outputFile)
        for rowIndex, row in enumerate(brainArr):
            if( rowIndex < args['trainingLength'] ):
                csvOutputFile.writerow( [ row ] )

    with open( path.join( args['outputFolder'], 'brainJS' + testingFileName ), 'w+') as outputFile:
        csvOutputFile = csv.writer(outputFile)
        for rowIndex, row in enumerate(brainArr):
            if( rowIndex >= args['trainingLength'] ):
                csvOutputFile.writerow( [ row ] )

    printParent('we have written your fully transformed brainJS data to a file at:')
    printParent( args['outputFolder'] )

    return brainArr
