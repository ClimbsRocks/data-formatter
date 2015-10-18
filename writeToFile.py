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

def writeFile(X, y, idColumn, args ):
    # grab the name of the training and testing files from the full path to those datasets
    trainingFileName = path.split( args['trainingData'] )[ -1 ]
    testingFileName = path.split( args['testingData'] )[ -1 ]
    # we will take in the invocation directory as an argument from Node.js. for now, just use os.getcwd()
    with open( path.join( args['outputFolder'], trainingFileName ), 'w+') as outputFile:
        csvOutputFile = csv.writer(outputFile)
        # grab only the rows that were part of our training file from the combined X dataset
        csvOutputFile.writerows( X[ 0 : args['trainingLength'] ])

    with open( path.join( args['outputFolder'], 'y' + trainingFileName ), 'w+') as outputFile:
        csvOutputFile = csv.writer(outputFile)
        # grab only the rows that were part of our training file from the combined X dataset
        csvOutputFile.writerows( y[ 0 : args['trainingLength'] ])

    with open( path.join( args['outputFolder'], testingFileName ), 'w+') as outputFile:
        csvOutputFile = csv.writer(outputFile)
        # grab the rest of the rows from our X dataset, which comprise the testing dataset
        csvOutputFile.writerows( X[ args['trainingLength'] :  ])





        printParent('we have written your fully transformed data to a file at:')
        printParent( path.join( os.getcwd(), 'testWrittenData.csv' ) )



