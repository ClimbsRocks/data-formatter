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
    # we will take in the invocation directory as an argument from Node.js. for now, just use os.getcwd()

    # TODO:
        # 1. figure out what we want to call each file, then be super consistent in that name
            # make sure it's called the same thing here, in the fileNames hash, and in ppc
            # take what we're currently passing into the with open() lines and save into variables that follow this naming convention
        # 2. create an obj with those properties
        # 3. send that obj back to parent
    y_train= path.join( args['outputFolder'], 'y_train_' + trainingFileName )
    id_train= path.join( args['outputFolder'], 'id_train_' + trainingFileName )
    id_test= path.join( args['outputFolder'], 'id_test_' + testingFileName )

    with open( y_train, 'w+') as outputFile:
        csvOutputFile = csv.writer(outputFile)
        # grab only the rows that were part of our training file from the combined dataset
        csvOutputFile.writerows( y[ 0 : args['trainingLength'] ])

    with open( id_train, 'w+') as outputFile:
        csvOutputFile = csv.writer(outputFile)
        # grab only the rows that were part of our training file from the combined dataset
        csvOutputFile.writerows( idColumn[ 0 : args['trainingLength'] ])

    with open( id_test, 'w+') as outputFile:
        csvOutputFile = csv.writer(outputFile)
        # grab only the rows that were part of our testing file from the combined dataset
        csvOutputFile.writerows( idColumn[ args['trainingLength']: ])

    fileNames = {
        y_train: y_train,
        id_train: id_train,
        id_test: id_test
    }
    messageParent( fileNames, 'fileNames' )


def writeData(X, args, headerRow ):
    X_train= path.join( args['outputFolder'],  'dfResults' + trainingFileName )
    X_test= path.join( args['outputFolder'], 'dfResults' + testingFileName )

    # grab the name of the training and testing files from the full path to those datasets
    trainingFileName = path.split( args['trainingData'] )[ -1 ]
    testingFileName = path.split( args['testingData'] )[ -1 ]
    # we will take in the invocation directory as an argument from Node.js. for now, just use os.getcwd()
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

    fileNames = {
        X_train: X_train,
        X_test: X_test
    }
    messageParent( fileNames, 'fileNames' )

    printParent('we have written your fully transformed data to a file at:')
    printParent( args['outputFolder'] )
