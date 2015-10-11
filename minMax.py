from sklearn import preprocessing
import numpy as np

min_max_scaler = preprocessing.MinMaxScaler(feature_range=(0, 1), copy=False)

def normalize(matrix):
    columns = zip(*matrix)
    for column in columns:
        # Future: check to make sure this is a numerical column, not a categorical column
        column = min_max_scaler.fit_transform(np.float32(column))
    return columns
