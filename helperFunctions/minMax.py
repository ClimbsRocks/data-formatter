import itertools
from sklearn import preprocessing
import numpy as np
from sendMessages import printParent
from sendMessages import messageParent
from sendMessages import obviousPrint

max_abs_scaler = preprocessing.MaxAbsScaler()

# Note: we're assuming that binarization of categorical data has already happened, and we don't need to do a check for categorical data here. 
def normalize( X, minMax ):
    if minMax:
        min_max_scaler = preprocessing.MinMaxScaler(feature_range=(0, 1), copy=False)
        X = np.array(X)
        X = X.reshape((-1,1))
        # printParent(X.tolist())
        X = min_max_scaler.fit_transform(X)
        # flatten our list. min_max_scaler requires a list where each item is itself a list (a list of nested lists). 
        # However, that's not what our nn's want.
        # X = list(itertools.chain.from_iterable(l)) is a way to turn the list of nested lists back into a single list again. 
        X = list(itertools.chain.from_iterable(X))
        # printParent(X[0:100])
    else:
        X = max_abs_scaler.fit_transform(X)
        # try:
        #     len(X[0])
        #     printParent('could take the length of the first row!')
        #     printParent(len(X[0]))
        #     X = max_abs_scaler.fit_transform(X)
        # except:
        #     # X = np.array(X)
        #     # X = np.reshape(X, -1)
        #     X = max_abs_scaler.fit_transform(X)
    return X
