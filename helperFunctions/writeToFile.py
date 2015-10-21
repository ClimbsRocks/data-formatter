import os
import csv
import os.path as path

from sendMessages import printParent
from sendMessages import messageParent
from sendMessages import obviousPrint

# Pre: make a folder in Node.js, and pass in that file path. That is an intermediate folder. 
# A. grab name of training data file
# B. 
# 1. write ID column to it's own file
# 2. write y column(s) to it's own file
# 3. write X training to it's own file
# 4. write X testing to it's own file

def writeMetadata(y, idColumn, args, headerRow ):
    # grab the name of the training and testing files from the full path to those datasets
    trainingFileName = path.split( args['trainingData'] )[ -1 ]
    testingFileName = path.split( args['testingData'] )[ -1 ]

    # save the file names into variables- we will use them to create the file and in the fileNames hash messaged out to the parent.
    y_train= path.join( args['outputFolder'], 'y_train_' + trainingFileName )
    id_train= path.join( args['outputFolder'], 'id_train_' + trainingFileName )
    id_test= path.join( args['outputFolder'], 'id_test_' + testingFileName )

    with open( y_train, 'w+') as outputFile:
        csvOutputFile = csv.writer(outputFile)
        # grab only the rows that were part of our training file from the combined dataset
        for rowIdx, row in enumerate(y):
            if( rowIdx < args['trainingLength'] ):
                csvOutputFile.writerow( [row] )

    with open( id_train, 'w+') as outputFile:
        csvOutputFile = csv.writer(outputFile)
        # grab only the rows that were part of our training file from the combined dataset
        for rowIdx, row in enumerate(idColumn):
            if( rowIdx < args['trainingLength'] ):
                csvOutputFile.writerow( [row] )

    with open( id_test, 'w+') as outputFile:
        csvOutputFile = csv.writer(outputFile)
        # grab only the rows that were part of our testing file from the combined dataset
        for rowIdx, row in enumerate(idColumn):
            if( rowIdx >= args['trainingLength'] ):
                csvOutputFile.writerow( [row] )

    fileNames = {
        'y_train': y_train,
        'id_train': id_train,
        'id_test': id_test
    }
    messageParent( fileNames, 'fileNames' )


def writeData(X, args, headerRow, nn ):

    # grab the name of the training and testing files from the full path to those datasets
    trainingFileName = path.split( args['trainingData'] )[ -1 ]
    testingFileName = path.split( args['testingData'] )[ -1 ]

    if( nn ):
        trainingFileName = 'nn_' + trainingFileName
        testingFileName = 'nn_' + testingFileName

    # save the file names into variables- we will use them to create the file and in the fileNames hash messaged out to the parent.
    X_train= path.join( args['outputFolder'],  'X_train_' + trainingFileName )
    X_test= path.join( args['outputFolder'], 'X_test_' + testingFileName )

    with open( X_train, 'w+') as outputFile:
        csvOutputFile = csv.writer(outputFile)
        csvOutputFile.writerow( headerRow )
        # grab only the rows that were part of our training file from the combined X dataset
        csvOutputFile.writerows( X[ 0 : args['trainingLength'] ])

    with open( X_test, 'w+') as outputFile:
        csvOutputFile = csv.writer(outputFile)
        csvOutputFile.writerow( headerRow )
        # grab the rest of the rows from our X dataset, which comprise the testing dataset
        csvOutputFile.writerows( X[ args['trainingLength'] :  ])


    if( nn ):
        fileNames = {
            'X_train_nn': X_train,
            'X_test_nn': X_test
        }
    else:
        fileNames = {
            'X_train': X_train,
            'X_test': X_test
        }
        
    messageParent( fileNames, 'fileNames' )
