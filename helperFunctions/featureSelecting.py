from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_selection import RFECV
import numpy as np

from sendMessages import printParent
from sendMessages import messageParent
from sendMessages import obviousPrint

def select( X, y, trainingLength, featureImportanceThreshold, headerRow, test ):

    # train a random forest
    classifier = RandomForestClassifier( n_jobs=-1, n_estimators=30 )
    classifier.fit( X[ 0 : trainingLength ], y[ 0 : trainingLength ] )

    # that forest will tell us the feature_importances_ of each of the features it was trained on
    # we want to grab only those column indices that pass the featureImportanceThreshold passed in to us
    columnIndicesThatPass = [idx for idx, x in enumerate( classifier.feature_importances_ ) if x > featureImportanceThreshold]

    # use numpy to grab only those columns that passed the previous step
    # cleanedX = np.array( X )[ :, columnIndicesThatPass ]
    cleanedX = X.tocsc()[:, columnIndicesThatPass]

    # create the new header row that contains only the column names that passed the test
    printingOutput = []
    filteredHeaderRow = []

    featureImportancesList = classifier.feature_importances_.tolist()
    # printParent(featureImportancesList)
    for idx, importance in enumerate( featureImportancesList ):
        # printParent(idx)
        if featureImportancesList[idx] > featureImportanceThreshold :
            printingOutput.append( [ headerRow[idx], round( importance, 4) ])
            filteredHeaderRow.append( headerRow[idx] )

    # print the features that passed out to the console for the user to see. 
    printingOutput = sorted(printingOutput, key=lambda x: x[1], reverse=True)
    if( not test ):
        printParent('here are the features that were kept, sorted by their feature importance')
        printParent(printingOutput)

    X = cleanedX

    return [ X, filteredHeaderRow ]

def rfecvSelection( X, y, trainingLength, featureImportanceThreshold, headerRow, test ):
    lr = LogisticRegression()
    rfecv = RFECV(estimator = lr, step=3)
    rfecv.fit(X, y)
    X = rfecv.transform(X)
    return X


    # post MVP ideas:
        # re-implement recursive feature selection
        # train using other models (or maybe even several of them in conjunction with each other?)
            # randomized linear regression
            # lasso
            # anything that's stable
            # search through results ranking array backwards
                # find the first feature that is at that ranking or lower for both/all estimators 
                    # so if a RF ranks a feature 128, and lasso ranks it 154, we will start at the end (worst performing), check to see if that feature is present at that rank or lower in the other array, and then repeat. 
            # almost certainly not as good as cross-validation, but might work well considering we'll be training ensembles
            # hopefully this way we can train on classifiers that allow n_jobs=-1!
            # all of this would likely be done within RFE. 
        # wait a minute, RFECV might let us pass in our own estimators! If so, we could just do all the above (ensembling together different classifiers), within that estimator that we're allowed to pass in! 
            # and we can obviously pick estimators that will allow us to pass in continuous features
            # yeah, that should totally be possible
            # first, i'd have to learn how to create my own custom estimator 


    # right now, RFECV assumes categorical data
    # another option to our current implementation:
        # assume all continuous data is good, separate out those columns, only run RFECV on categorical columns, add continuous columns back in
