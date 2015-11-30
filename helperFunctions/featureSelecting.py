import time

from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.feature_selection import RFECV
import numpy as np

from sendMessages import printParent
from sendMessages import messageParent
from sendMessages import obviousPrint

# this is purely a helper function for select. it should not be used outside of select 
def cleanDataset(X, coefficients, threshold, headerRow):
    # that forest will tell us the feature_importances_ of each of the features it was trained on
    # we want to grab only those column indices that pass the featureImportanceThreshold passed in to us
    columnIndicesThatPass = [idx for idx, x in enumerate( coefficients ) if x > threshold]

    # use numpy to grab only those columns that passed the previous step
    # cleanedX = np.array( X )[ :, columnIndicesThatPass ]
    cleanedX = X.tocsc()[ :, columnIndicesThatPass]
    del X
    cleanedX = cleanedX.tocsr()

    # create the new header row that contains only the column names that passed the test
    printingOutput = []
    filteredHeaderRow = []

    featureImportancesList = coefficients.tolist()
    # printParent(featureImportancesList)
    for idx, importance in enumerate( featureImportancesList ):
        # printParent(idx)
        if featureImportancesList[idx] > threshold :
            printingOutput.append( [ headerRow[idx], round( importance, 4) ])
            filteredHeaderRow.append( headerRow[idx] )

    # print the features that passed out to the console for the user to see. 
    printingOutput = sorted(printingOutput, key=lambda x: x[1], reverse=True)

    return cleanedX, filteredHeaderRow, printingOutput


# this is the main public interface
def select( X, y, trainingLength, featureImportanceThreshold, headerRow, test, problemType ):

    # first, train linearly to remove all the completely useless features
        # this lets us send fewer features into our random forest (or eventaully RFECV), which leads to dramatically faster training times (~ 2-3x improvement)
    # repeat this process twice with different feature thresholds. 
    # first four orders of magnitude less than featureImportanceThreshold, then two orders of magnitude less
    # hopefully by removing the features that are pure noise, we can all the signal to be found more reliably, and certainly more quickly.
    if problemType == 'category':
        estimator = LogisticRegression(n_jobs=-1)
    else:
        estimator = LinearRegression(n_jobs=-1)

    estimator.fit( X[ 0 : trainingLength ], y[ 0 : trainingLength ] )


    # remove everything that is at least four orders of magnitude shy of our featureImportanceThreshold
    X, headerRow, printingOutput = cleanDataset(X, estimator.coef_, featureImportanceThreshold / 10000, headerRow) 

    # first, train linearly to remove all the completely useless features
    if problemType == 'category':
        estimator = LogisticRegression(n_jobs=-1)
    else:
        estimator = LinearRegression(n_jobs=-1)

    estimator.fit( X[ 0 : trainingLength ], y[ 0 : trainingLength ] )


    # remove everything that is at least two orders of magnitude shy of our featureImportanceThreshold
    X, headerRow, printingOutput = cleanDataset(X, estimator.coef_, featureImportanceThreshold / 100, headerRow)

    rfStartTime = time.time()

    # train a random forest
    if problemType == 'category':
        classifier = RandomForestClassifier( n_jobs=-1, n_estimators=30 )
    else:
        classifier = RandomForestRegressor( n_jobs=-1, n_estimators=30 )
    classifier.fit( X[ 0 : trainingLength ], y[ 0 : trainingLength ] )

    X, filteredHeaderRow, printingOutput = cleanDataset(X, classifier.feature_importances_, featureImportanceThreshold, headerRow )
    

    if( not test ):
        printParent('here are the features that were kept, sorted by their feature importance')
        printParent(printingOutput)

    printParent('total time for the random forest part of feature selection:')
    # this will get us execution time in minutes, to one decimal place
    printParent( round( (time.time() - rfStartTime)/60, 1 ) )


    return [ X, filteredHeaderRow ]

# def rfecvSelection( X, y, trainingLength, featureImportanceThreshold, headerRow, test ):
#     lr = LogisticRegression()
#     rfecv = RFECV(estimator = lr, step=3)
#     rfecv.fit(X, y)
#     X = rfecv.transform(X)
#     return X


#     # post MVP ideas:
#         # re-implement recursive feature selection
#         # train using other models (or maybe even several of them in conjunction with each other?)
#             # randomized linear regression
#             # lasso
#             # anything that's stable
#             # search through results ranking array backwards
#                 # find the first feature that is at that ranking or lower for both/all estimators 
#                     # so if a RF ranks a feature 128, and lasso ranks it 154, we will start at the end (worst performing), check to see if that feature is present at that rank or lower in the other array, and then repeat. 
#             # almost certainly not as good as cross-validation, but might work well considering we'll be training ensembles
#             # hopefully this way we can train on classifiers that allow n_jobs=-1!
#             # all of this would likely be done within RFE. 
#         # wait a minute, RFECV might let us pass in our own estimators! If so, we could just do all the above (ensembling together different classifiers), within that estimator that we're allowed to pass in! 
#             # and we can obviously pick estimators that will allow us to pass in continuous features
#             # yeah, that should totally be possible
#             # first, i'd have to learn how to create my own custom estimator 


#     # right now, RFECV assumes categorical data
#     # another option to our current implementation:
#         # assume all continuous data is good, separate out those columns, only run RFECV on categorical columns, add continuous columns back in
