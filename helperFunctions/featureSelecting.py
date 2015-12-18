import time
import json

from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.feature_selection import RFECV
import numpy as np

from sendMessages import printParent
from sendMessages import messageParent
from sendMessages import obviousPrint

# this is purely a helper function for select. it should not be used outside of this file
# find the maximally useful feature value and compare everything else to that
def cleanDataset(X, coefficients, thresholdDivisor, headerRow, dataDescription):

    # the forest will tell us the feature_importances_ of each of the features it was trained on
    # we want to grab only those column indices that pass the featureImportanceThreshold passed in to us
    absCoefficients = [abs(x) for x in coefficients]

    maxCoefficient = np.amax(absCoefficients)

    threshold = maxCoefficient / thresholdDivisor

    columnIndicesThatPass = [ idx for idx, x in enumerate( absCoefficients ) if x > threshold ]

    # use column slicing to grab only those columns that passed the previous step
    cleanedX = X.tocsc()[ :, columnIndicesThatPass]
    del X
    cleanedX = cleanedX.tocsr()

    # create the new header row that contains only the column names that passed the test
    printingOutput = []
    filteredHeaderRow = []
    filteredDataDescription = []

    featureImportancesList = coefficients.tolist()
    for idx, importance in enumerate( featureImportancesList ):

        if abs(featureImportancesList[idx]) > threshold :
            printingOutput.append( [ headerRow[idx], round( importance, 4) ])
            filteredHeaderRow.append( headerRow[idx] )
            filteredDataDescription.append( dataDescription[idx] )

    # print the features that passed out to the console for the user to see. 
    printingOutput = sorted(printingOutput, key=lambda x: x[1], reverse=True)

    return cleanedX, filteredHeaderRow, printingOutput, dataDescription

# this is the function that runs some relatively straightforward feature selection
# it uses a random forest, so it understands non-linear relationships and should work well for most datasets
# featureImportanceThreshold is measured relative to the most important feature
# so if you pass in 100 for featureImportanceThreshold, the only features to be selected are the ones that are at least 1/100th as useful as the most important feature
def prune(  X, y, trainingLength, featureImportanceThreshold, headerRow, dataDescription, test, problemType ):
    rfStartTime = time.time()

    # train a random forest
    if problemType == 'category':
        classifier = RandomForestClassifier( n_jobs=-1, n_estimators=20 )
    else:
        classifier = RandomForestRegressor( n_jobs=-1, n_estimators=20 )
    classifier.fit( X[ 0 : trainingLength ], y[ 0 : trainingLength ] )

    X, filteredHeaderRow, printingOutput, filteredDataDescription = cleanDataset(X, classifier.feature_importances_, featureImportanceThreshold, headerRow, dataDescription )
    

    if( not test ):
        printParent('here are the features that were kept, sorted by their feature importance')
        printParent(printingOutput)

    printParent('total time for the pruning part of feature selection, in minutes:')
    # this will get us execution time in minutes, to one decimal place
    printParent( round( (time.time() - rfStartTime)/60, 1 ) )


    return [ X, filteredHeaderRow, filteredDataDescription ]



# this is the main public interface
def select( X, y, trainingLength, featureImportanceThreshold, headerRow, test, problemType ):
    # after dictVectorizing.py, we do not have a dataDescription row, nor do we need one. 
    # however, we've modularized prune so that prune expects a dataDescription row
    # here, we are simply creating a dummy dataDescription row that we will not use except to avoid an error in prune
    dataDescription = ['dummyValue' for x in range(len(headerRow)) ]

    # first, train linearly to remove all the completely useless features
        # this lets us send fewer features into our random forest (or eventaully RFECV), which leads to dramatically faster training times (~ 2-3x improvement)
    # repeat this process twice with different feature thresholds. 
    # first four orders of magnitude less than the most important feature, then two orders of magnitude less
    # hopefully by removing the features that are pure noise, we can all the signal to be found more reliably, and certainly more quickly.
    # if problemType == 'category':
    #     estimator = LogisticRegression(n_jobs=-1)
    # else:
    #     estimator = LinearRegression(n_jobs=-1)

    # estimator.fit( X[ 0 : trainingLength ], y[ 0 : trainingLength ] )

    # try:
    #     coefList = estimator.coef_[0]
    #     len(coefList)
    # except:
    #     coefList = estimator.coef_


    # # remove everything that is at least 4 orders of magnitude shy of the best feature
    # X, headerRow, printingOutput, dataDescription = cleanDataset(X, coefList, 10000, headerRow, dataDescription) 

    # printParent('here are the features that were kept by the first round of regression, sorted by their feature importance')
    # printParent(printingOutput)


    rfStartTime = time.time()

    # train a random forest
    if problemType == 'category':
        classifier = RandomForestClassifier( n_jobs=-1, n_estimators=20 )
    else:
        classifier = RandomForestRegressor( n_jobs=-1, n_estimators=20 )
    classifier.fit( X[ 0 : trainingLength ], y[ 0 : trainingLength ] )

    # remove features that are at least 3 orders of magnitude shy of our most important feature
    X, filteredHeaderRow, printingOutput, dataDescription = cleanDataset(X, classifier.feature_importances_, 1000, headerRow, dataDescription )
    

    if( not test ):
        printParent('here are the features that were kept, sorted by their feature importance')
        printParent(printingOutput)

    printParent('total time for the random forest part of feature selection, in minutes:')
    # this will get us execution time in minutes, to one decimal place
    printParent( round( (time.time() - rfStartTime)/60, 1 ) )


    return X, filteredHeaderRow 
