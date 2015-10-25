import writeToFile
import os
import os.path as path
import csv
import json
import writeToFile
from sklearn import preprocessing
from sendMessages import printParent
from sendMessages import messageParent
from sendMessages import obviousPrint

# brainjs prefers values in the range of (0,1), while scikit-neuralnetwork can handle them in the range of (-1,1)
# we need to re-normalize to a range of (0,1)
min_max_scaler = preprocessing.MinMaxScaler(feature_range=(0, 1), copy=False)

def format( X, y, idColumn, args ):
    X = min_max_scaler.fit_transform( X ).tolist()

    brainArr = []
    for rowIndex, row in enumerate(X):

        # brainJS expects a very particular format for each row:
            # an object with input and output properties, each of which is an array
        rowObj = {}

        # we might need to wrap output in a list if the output is a single number, like we have. 
        rowObj['output'] = []

        # if a y value exists for this rowIndex, grab it!
        # otherwise, it's likely because the user did not pass in a column for y values for the output dataset, so we'll set it equal to the empty string instead
        try:
            # grab the output value from the y dataset saved earlier
            yRow = y[ rowIndex ]
        except:
            yRow = ""

        # designed to handle the possibility of multiple output columns
        if( isinstance( yRow, list )):
            rowObj['output'].extend( yRow )
        else:
            # the output value is expected to be a list, so if y values are not lists, then we need to wrap the y value in a list
            rowObj['output'].append( yRow )

        rowObj[ 'id' ] = idColumn[ rowIndex ]

        for idx, val in enumerate(row):
            # python saves floats in their binary representation, which gets written to file in scientific notation
            # this scientific notation is not necessarily json compatible
            # so we format these values as a string
            # unfortunately, these strings will only have 6 decimal places after the 0. this should not be a major limitation, as that still allows 6 orders of magnitude of differentiation. it would be a rather surprising neural network who could draw meaningful distinctions between values that are 7 orders of magnitude different from the max value vs values that are 6 orders of magnitude different from the max value. 
            # in our case, they'll both just get saved as 0. 
            row[idx] = '{:f}'.format(val)
            
        rowObj['input'] = row
        brainArr.append( rowObj )

    trainingFileName = path.split( args['trainingData'] )[ -1 ]
    testingFileName = path.split( args['testingData'] )[ -1 ]

    brainJS_train = path.join( args['outputFolder'], 'brainJS_train_' + trainingFileName )
    brainJS_test = path.join( args['outputFolder'], 'brainJS_test_' + testingFileName )

    with open( brainJS_train, 'w+') as outputFile:
        csvOutputFile = csv.writer(outputFile)
        for rowIndex, row in enumerate(brainArr):
            if( rowIndex < args['trainingLength'] ):
                # csvWriter.writerow expects each row to be a list
                # since our rows are actually just dictionaries, we need to wrap it in a list each time so the writer knows this is a single row
                csvOutputFile.writerow( [ json.dumps( row ) ] )

    with open( brainJS_test, 'w+') as outputFile:
        csvOutputFile = csv.writer(outputFile)
        for rowIndex, row in enumerate(brainArr):
            if( rowIndex >= args['trainingLength'] ):
                csvOutputFile.writerow( [ row ] )

    fileNames = {
        'brainJS_train': brainJS_train,
        'brainJS_test': brainJS_test
    }
    messageParent( fileNames, 'fileNames' )

    return brainArr
