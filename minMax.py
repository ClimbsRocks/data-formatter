from sklearn import preprocessing
import numpy as np
from sendMessages import printParent
from sendMessages import messageParent
from sendMessages import obviousPrint

min_max_scaler = preprocessing.MinMaxScaler(feature_range=(0, 1), copy=False)

def normalize(dataDescription, matrix):
    columns = zip(*matrix)
    cleanedColumns = []
    for idx, column in enumerate(columns):
        if dataDescription[idx] == 'numerical':
            column = min_max_scaler.fit_transform( column )
            cleanedColumns.append(column)
        else:
            cleanedColumns.append(column)
    rowMatrix = zip(*cleanedColumns)
    return rowMatrix
