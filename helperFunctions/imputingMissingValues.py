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
def standardizeMissingValues(dataDescription, matrix ):
    cleanedColumnMatrix = []
    columnsWithMissingValues = {}

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
                    # and keep track of this column as having msising values
                    columnsWithMissingValues[idx] = True

        elif dataDescription[idx] == "categorical":
            # if it's categorical
            for value in column:
                if str(value).lower() in emptyEquivalents:
                    # replace all values we have defined above as being equivalent to a missing value with the standardized version the inputer will recognize next: np.nan
                    cleanColumn.append( np.nan )
                    # and keep track of this column as having msising values
                    columnsWithMissingValues[idx] = True
                
                else:
                    cleanColumn.append(value)

        cleanedColumnMatrix.append( cleanColumn )
    return [ cleanedColumnMatrix, columnsWithMissingValues ]

def createImputedColumns( columnMatrix, dataDescription, columnsWithMissingValues, headerRow ):
    # we want to keep track of the total number of imputed values for each row
    # but it only makes sense to have a total column if we have more than 1 column with missing values
    # we can probably get rid of this with robust feature selection
    if( len( columnsWithMissingValues.keys() ) > 1 ):
        # create a new empty list that is filled with blank values (None) that is the length of a standard column
        emptyList = [ 0 ] * len( columnMatrix[0] )
        columnMatrix.append( emptyList )
        # keep track of this new column in our headerRow and our dataDescription row
        dataDescription.append( 'Continuous' )
        headerRow.append( 'countOfMissingValues' )
    
    for colIndex in columnsWithMissingValues:
        # create a copy of the existing column and append it to the end. this way we can modify one column, but leave the other untouched
        newColumn = list( columnMatrix[ colIndex ])
        columnMatrix.append( newColumn )

        # include prettyNames for dataDescription and header row
        dataDescription.append( dataDescription[colIndex] ) 
        headerRow.append( 'missing' + headerRow[ colIndex ] )

        # create a new empty column to hold information on whether this row has an imputed value for the current column
        emptyList = [ 0 ] * len( columnMatrix[0] )
        columnMatrix.append( emptyList )
        # keep track of this new column in our headerRow and our dataDescription row
        dataDescription.append( 'Continuous' )
        headerRow.append( 'missing' + headerRow[ colIndex ] )

    return [ columnMatrix, dataDescription, columnsWithMissingValues, headerRow ]

# TODO:
    # redefine impute
        # get median value for continuous columns
        # get mode value for categorical columns
        # iterate through columns list, starting at the index position of the new columns
            # check to make sure this colIndex is indeed a cloned column with missing values (not a column holding a boolean flag for whether a missing value was found)
            # if so
                # iterate through list, with rowIndex
                    # for each item:
                        # check for missing values. if they exist:
                            # replace missing value
                            # find the flag column for this column in columnsWithMissingValues dictionary
                                # set that value equal to 1
                            # find the column holding the count of all missing values for that row
                                # increment that value by 1
    # make columnsWithMissingValues into a map-
        # original (untouched) column index is the key
        # cloned (with imputed values) column index is the value
            # we just know that one over from that cloned column is the boolean flag column for that column
        # have another property for totalMissingValuesCount, pointing to whichever columnIndex is appropriate there.

    # return all the new values (X, dataDescription, headerRow)
    # handle all these new return values in mainPythonProcess
    # might have to tweak a test or two further down the line for this new number of columns. 


# This function is just a slightly tweaked version from:
# http://stackoverflow.com/a/25562948
def stackOverflowImpute(dataDescription, columnMatrix):
    rowMatrix = zip(*columnMatrix)

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
def cleanAll(dataDescription, matrix, headerRow ):
    standardizedResults = standardizeMissingValues(dataDescription, matrix)
    cleanedColumnMatrix = standardizedResults[ 0 ]
    columnsWithMissingValues = standardizedResults[ 1 ]

    newColumnsList = createImputedColumns( cleanedColumnMatrix, dataDescription, columnsWithMissingValues, headerRow )

    return cleanedColumnMatrix
    # results = stackOverflowImpute(dataDescription, cleanedColumnMatrix)
    # return results
