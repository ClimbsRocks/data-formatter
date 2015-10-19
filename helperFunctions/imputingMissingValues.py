from sklearn import preprocessing
import numpy as np

from sendMessages import printParent
from sendMessages import messageParent
from sendMessages import obviousPrint

imputer = preprocessing.Imputer(missing_values="NaN", strategy='median', verbose=10)
# TODO: ignore casing
emptyEquivalents = ["na","n/a","none",'',"undefined","missing","blank","empty", None]

# standardize all missing values to None
# removes all strings (values that can't be converted to a flot) from "Numerical" columns
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
            for value in column:
                if str(value).lower() in emptyEquivalents:
                    cleanColumn.append( np.nan )
                else:
                    cleanColumn.append(value)


        # elif dataDescription[idx] == "id":
        #     for value in column:

        #         if str(value).lower() in emptyEquivalents:
        #             printParent('warning, you are missing values in your ID column')
        #     # we will warn them but allow them to continue
        #     cleanColumn = column

        # elif dataDescription[idx] == "output":
        #     cleanColumn
        #     for rowIdx, value in enumerate(column):

        #         # if this row is in our training data, and we have missing values, warn the user
        #         if str(value).lower() in emptyEquivalents and rowIdx < trainingLength:
        #             printParent('warning, you are missing values in your training Output column')
        #             # prevent the imputer from trying to impute this value. We will let the user or the classifier rectify this issue later down the road. 
        #             cleanColumn.append("DO_NOT_ACCIDENTALLY_FILL_ME_IN")

        #         # check to make sure that all the prediction cells are blank for the testing data
        #         elif rowIdx > trainingLength:
        #             if str(value).lower() not in emptyEquivalents:
        #                 printParent('warning, have values in the Output field of your testing data. We are removing them now, but you might want to consider using this as your training data next time')
        #             # making super sure that we do not accidentally impute values for the output column in the testing data
        #             cleanColumn.append("DO_NOT_ACCIDENTALLY_FILL_ME_IN")

        #         else:
        #             cleanColumn.append(value)


        
        cleanedMatrix.append( cleanColumn )
    return cleanedMatrix


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
                [ X[c].value_counts().index[0]
                if X[c].dtype == np.dtype('O') else X[c].median() for c in X ],
                index=X.columns
            )

            return self

        def transform(self, X, y=None):
            return X.fillna(self.fill)

    X = pd.DataFrame(rowMatrix)
    X = DataFrameImputer().fit_transform(X)

    # convert from pands DataFrame back to a standard python list
    X = X.values.tolist()

    return X





def cleanAll(dataDescription, trainingLength, matrix ):
    cleanedMatrix = standardizeMissingValues(dataDescription, trainingLength, matrix)
    # results = impute(dataDescription, cleanedMatrix )
    results = stackOverflowImpute(dataDescription, cleanedMatrix)
    return results
