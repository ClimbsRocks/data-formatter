from sklearn import preprocessing
import numpy as np
from sendMessages import printParent
from sendMessages import messageParent
from sendMessages import obviousPrint

min_max_scaler = preprocessing.MinMaxScaler(feature_range=(-1, 1), copy=False)

# Note: we're assuming that binarization of categorical data has already happened, and we don't need to do a check for categorical data here. 
def normalize( X ):
    X = min_max_scaler.fit_transform(X)
    return X
