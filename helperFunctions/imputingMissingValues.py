from sklearn import preprocessing
import numpy as np

from sendMessages import printParent
from sendMessages import messageParent
from sendMessages import obviousPrint

imputer = preprocessing.Imputer(missing_values="NaN", strategy='median', verbose=10)
emptyEquivalents = ["na","n/a","none",'',"undefined","missing","blank","empty", None]

# standardizes all missing values to None
# removes all strings (values that can't be converted to a float) from "Numerical" columns
# removes all values in the emptyEquivalents array from categorical columns
# doesn't touch ID or Output columns
def standardizeMissingValues(dataDescription, trainingLength, matrix ):
    cleanedMatrix = []

    # split data into columns
    columns = zip(*matrix)
    # iterate through the columns. for each one:
    for idx, column in enumerate(columns):
        cleanColumn = []

        # check and see if it is a continuous field
        if dataDescription[idx] == "continuous":

            for num in column:
                try:
                    # if it is continuous, try to convert each field to a float
                    cleanColumn.append( float( num ) )
                except:
                    # remove all non-numerical values
                    # Note: passing in None breaks Imputer in the next step. Passing in np.nan works with Imputer
                    cleanColumn.append( np.nan )
        elif dataDescription[idx] == "categorical":
            # if it's categorical
            for value in column:
                if str(value).lower() in emptyEquivalents:
                    # replace all values we have defined above as being equivalent to a missing value with the standardized version the inputer will recognize next: np.nan
                    cleanColumn.append( np.nan )
                else:
                    cleanColumn.append(value)

        cleanedMatrix.append( cleanColumn )
    return cleanedMatrix

# This function is just a slightly tweaked version from:
# http://stackoverflow.com/a/25562948
def stackOverflowImpute(dataDescription, matrix):
    rowMatrix = zip(*matrix)

    import pandas as pd
    import numpy as np

    from sklearn.base import TransformerMixin

    class DataFrameImputer(TransformerMixin):

        def __init__(self):
            """Impute missing values.

            Columns of dtype object are imputed with the most frequent value 
            in column.

            Columns of other types are imputed with mean of column.

            """
        def fit(self, X, y=None):

            self.fill = pd.Series(
                # for categorical columns, use the most frequently occurring value for that column
                [ X[c].value_counts().index[0]
                # for continuous columns, use the median value for that column
                if X[c].dtype == np.dtype('O') else X[c].median() for c in X ],
                index=X.columns
            )

            return self

        def transform(self, X, y=None):
            return X.fillna(self.fill)

    # our imputer assumes a format of pandas DataFrames
    X = pd.DataFrame(rowMatrix)
    X = DataFrameImputer().fit_transform(X)

    # convert from pandas DataFrame back to a standard python list
    X = X.values.tolist()

    return X


# cleanAll is the function that will be publicly invoked. 
# cleanAll defers to the standardize and impute functions above
def cleanAll(dataDescription, trainingLength, matrix ):
    cleanedMatrix = standardizeMissingValues(dataDescription, trainingLength, matrix)
    results = stackOverflowImpute(dataDescription, cleanedMatrix)
    return results
