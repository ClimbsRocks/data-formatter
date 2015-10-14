from sklearn.feature_selection import RFECV


def select(X, y):

    # TODO: define extimator
        # pass in scoring, based on that estimator
        # fit
        # in separate steps, transform x and y, just to be super clear
    featureSelector = RFECV(estimator, step=1, cv=5)

