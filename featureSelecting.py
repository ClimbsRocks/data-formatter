from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_selection import RFECV
import numpy as np

from sendMessages import printParent
from sendMessages import messageParent
from sendMessages import obviousPrint

def select( X, y, trainingLength, featureImportanceThreshold, headerRow ):

    classifier = RandomForestClassifier( n_jobs=-1, n_estimators=30 )
    classifier.fit( X[ 0 : trainingLength ], y[ 0 : trainingLength ] )

    columnIndicesThatPass = [idx for idx, x in enumerate( classifier.feature_importances_ ) if x > featureImportanceThreshold]

    cleanedX = np.array( X )[ :, columnIndicesThatPass ]

    printingOutput = []
    filteredHeaderRow = []
    for idx, importance in enumerate( classifier.feature_importances_ ):
        if( classifier.feature_importances_[idx] > featureImportanceThreshold ):
            printingOutput.append( [ headerRow[idx], importance ])
            filteredHeaderRow.append( headerRow[idx] )

    printingOutput = sorted(printingOutput, key=lambda x: x[1], reverse=True)
    printParent('here are the features that were kept, sorted by their feature importance')
    printParent(printingOutput)

    X = cleanedX

    return X


    # MVP: train a RF, take all the features with an importance > .1. 
        # don't worry about recursing, don't worry about other models
        # don't worry about including feature names
        # just train a RF and take all features that have an importance > 0.1
        # this will definitely be refactored over time. 


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
    # two options:
        # 1. assume all continuous data is good, separate out those columns, only run RFECV on categorical columns, add continuous columns back in
        # 2. scrap RFECV (or re-implement my own), and switch over to using random forests
            # you can get the feature importance from a trained random forest
            # from there, just choose all features that have an importance above 0.1, or some other arbitrary number like that
            # we could accompany this with a decent amount of logging (verbose=true)
                # here is the feature importance
                # here are the features that got selected
                # here are the features that got dropped
                # feel free to adjust the feature importance parameter in XYZ file to adjust this
            # we could also do this inside of our own recursive feature elimination (or borrow theirs and see if we can make it work on continuous data)
            # the benefit of doing it this way is we can probably keep the category names in the output relatively easily. 
            # the drawback is, of course, that it would be our implementation, not one that's validated and maintained by sklearn
    
