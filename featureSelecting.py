from sklearn.linear_model import LogisticRegression
from sklearn.feature_selection import RFECV

from sendMessages import printParent
from sendMessages import messageParent
from sendMessages import obviousPrint

def select(X, y):
    printParent('just entered featureSelecting.py')

    # TODO: in scikit-learn 0.17 they have made random forests available to use for RFECV. Once that has come out, use random forests (training across all cores!), and add a note about how you must use version 0.17. 
        # ideally, we would fail gracefully back into logistic regression
    estimator = LogisticRegression()

    # TODO: pass in scoring, based on that estimator
    # TODO: make step smaller, and cv possibly larger, depending on how much time we want to spend running through this. 
    featureSelector = RFECV(estimator=estimator, step=3, cv=3, verbose=0)

    # future optimization: this is creating a copy (slice) of the list from 0 up to but not including index position 150000
        # see what the most effective way is to do this without duplicating. 
        # though if it's making a shallow copy, i'm not sure if this list type is passed by reference in python or not...
    printParent('about to run RFECV')
    transformedX = featureSelector.fit_transform(X[0:150000],y[0:150000]).tolist()

    testData = featureSelector.transform(X[150000:]).tolist()

    # append both results together and overwrite the original X with the results
    X = transformedX
    for row in testData:
        transformedX.append(row)

    return X
