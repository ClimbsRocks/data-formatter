import os
import csv
import os.path as path
import numpy as np

from scipy.sparse import csr_matrix

from sendMessages import printParent
from sendMessages import messageParent
from sendMessages import obviousPrint


# shoutout to the original author:
# http://stackoverflow.com/questions/8955448/save-load-scipy-sparse-csr-matrix-in-portable-data-format
def save_sparse_csr(filename,array):
    indices = [int(x) for x in array.indices]
    np.savez(filename,data=array.data ,indices=array.indices, indptr=array.indptr, shape=array.shape )


def writeMetadata(y, idColumn, args, headerRow, validationSplitColumn, hasCustomValidationSplit):

    # these are the file names (with full file paths) that we will be writing to
    y_train = path.join( args['outputFolder'], 'y_train_' + args['trainingPrettyName'] + '.npz' )
    id_train = path.join( args['outputFolder'], 'id_train_' + args['trainingPrettyName'] + '.npz' )
    id_test = path.join( args['outputFolder'], 'id_test_' + args['testingPrettyName'] + args['trainingPrettyName'] + '.npz' )
    validation_split_column = path.join( args['outputFolder'], 'validation_split_column_' + args['trainingPrettyName'] + '.npz' )

    trainingLength = args['trainingLength']

    # convert all our data to np arrays, and break apart based on whether it's in the training data or not
    idTrainData = np.array( idColumn[ 0 : trainingLength ] )
    idTestData = np.array( idColumn[ trainingLength : ] )
    y = np.array( y ) 
    validationSplitColumnData = np.array( validationSplitColumn )

    # if our values are not already stored as numbers, convert them to numbers
    try: 
        ySparse = csr_matrix(y)
    except:
        yInt = [float(i) for i in y[0:trainingLength]]
        ySparse = csr_matrix( yInt )

    try:
        idTrainSparse = csr_matrix(idTrainData)
    except:
        idTrainInt = [float(i) for i in idTrainData]
        idTrainSparse = csr_matrix( idTrainInt )

    try:
        idTestSparse = csr_matrix(idTestData)
    except:
        idTestInt = [float(i) for i in idTestData]
        idTestSparse = csr_matrix( idTestInt )

    try:
        validationSplitSparse = csr_matrix(validationSplitColumnData)
    except:
        validationSplitInt = [float(i) for i in validationSplitColumnData]
        validationSplitSparse = csr_matrix( validationSplitInt )

    save_sparse_csr(y_train, ySparse )
    save_sparse_csr(id_train, idTrainSparse )
    save_sparse_csr(id_test, idTestSparse )
    save_sparse_csr(validation_split_column, validationSplitSparse )

    
    fileNames = {
        'y_train': y_train,
        'id_train': id_train,
        'id_test': id_test,
        'idHeader': args['idHeader'],
        'outputHeader': args['outputHeader'],
        'validation_split_column': validation_split_column,
        'hasCustomValidationSplit': hasCustomValidationSplit
    }
    messageParent( fileNames, 'fileNames' )
    

def writeMetadataDense(y, idColumn, args, headerRow ):
    # grab the name of the training and testing files from the full path to those datasets

    # save the file names into variables- we will use them to create the file and in the fileNames hash messaged out to the parent.
    y_train= path.join( args['outputFolder'], 'y_train_' + args['trainingPrettyName'] + '.csv' )
    id_train= path.join( args['outputFolder'], 'id_train_' + args['trainingPrettyName'] + '.csv' )
    id_test= path.join( args['outputFolder'], 'id_test_' + args['testingPrettyName'] + args['trainingPrettyName'] + '.csv' )

    with open( y_train, 'w+') as outputFile:
        csvOutputFile = csv.writer(outputFile)

        # write the pretty name for the header row to the output file
        csvOutputFile.writerow( [args[ 'outputHeader' ]] )

        # grab only the rows that were part of our training file from the combined dataset
        for rowIdx, row in enumerate(y):
            if( rowIdx < args['trainingLength'] ):
                csvOutputFile.writerow( [row] )

    with open( id_train, 'w+') as outputFile:
        csvOutputFile = csv.writer(outputFile)

        # write the pretty name for the header row to the output file
        csvOutputFile.writerow( [args[ 'idHeader' ]] )

        # grab only the rows that were part of our training file from the combined dataset
        for rowIdx, row in enumerate(idColumn):
            if( rowIdx < args['trainingLength'] ):
                csvOutputFile.writerow( [row] )

    with open( id_test, 'w+') as outputFile:
        csvOutputFile = csv.writer(outputFile)

        # write the pretty name for the header row to the output file
        csvOutputFile.writerow( [args[ 'idHeader' ]] )

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


def writeDataDense(X, args, headerRow, nn ):

    # grab the name of the training and testing files from the full path to those datasets
    trainingFileName = args['trainingPrettyName'] + '.csv'
    testingFileName = args['testingPrettyName'] + args['trainingPrettyName'] + '.csv'

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

def writeDataSparse(X, args, headerRow, nn ):

    # grab the name of the training and testing files from the full path to those datasets
    trainingFileName = args['trainingPrettyName'] + '.npz'
    testingFileName = args['testingPrettyName'] + args['trainingPrettyName'] + '.npz'

    if type(nn) is not bool:
        trainingFileName = 'nn_' + trainingFileName
        testingFileName = 'nn_' + testingFileName
        yFileName = 'y_train_' + 'nn_' +  args['trainingPrettyName'] + '.npz'
        y_train = path.join( args['outputFolder'], yFileName )

        y = np.array( nn ) 
        y = [float(i) for i in y]
        

        # if our values are not already stored as numbers, convert them to numbers
        try: 
            ySparse = csr_matrix(y)
            printParent('successfully turned y into a sparse matrix!')
        except:
            yInt = [float(i) for i in y[0:trainingLength]]
            ySparse = csr_matrix( yInt )

        save_sparse_csr(y_train, ySparse )

    # save the file names into variables- we will use them to create the file and in the fileNames hash messaged out to the parent.
    X_train= path.join( args['outputFolder'],  'X_train_' + trainingFileName )
    X_test= path.join( args['outputFolder'], 'X_test_' + testingFileName )

    # scipy sparse matrices need a list of indices to slice
    # http://stackoverflow.com/questions/13352280/slicing-sparse-matrices-in-scipy-which-types-work-best
    trainRange = range(args['trainingLength'])
    testRange = range(args['trainingLength'], args['trainingLength'] + args['testingLength'])

    save_sparse_csr(X_train, X[trainRange,:])
    save_sparse_csr(X_test, X[testRange])

    if type(nn) is not bool:
        fileNames = {
            'X_train_nn': X_train,
            'X_test_nn': X_test,
            'y_train_nn': y_train
        }
    else:
        fileNames = {
            'X_train': X_train,
            'X_test': X_test
        }
    messageParent( fileNames, 'fileNames' )
