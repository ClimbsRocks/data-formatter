from sklearn import preprocessing
import numpy as np

from sendMessages import printParent
from sendMessages import messageParent
from sendMessages import obviousPrint

imputer = preprocessing.Imputer(missing_values="NaN", strategy='median', verbose=10)
# TODO: ignore casing
emptyEquivalents = ["NA","N/A","None","","undefined","missing","blank","empty", None]

# standardize all missing values to None
# removes all strings (values that can't be converted to a flot) from "Numerical" columns
# removes all values in the emptyEquivalents array from categorical columns
# doesn't touch ID or Output columns
def standardizeMissingValues(dataDescription, matrix ):
    cleanedMatrix = []

    # split data into columns
    columns = zip(*matrix)
    # iterate through the columns. for each one:
    for idx, column in enumerate(columns):
        cleanColumn = []

        # check and see if it is a numerical field
        if dataDescription[idx] == "numerical":

            for num in column:
                try:
                    # if it is numerical, try to convert each field to a float
                    cleanColumn.append( float( num ) )
                except:

                    # remove all non-numerical values
                    # NOTE: passing in None breaks Imputer in the next step. Passing in float('nan') works with Imputer
                    cleanColumn.append( float('nan') )
            # make sure this array is stored as a np array with data type float64- essential for the next series of transforms. 
            cleanColumn = np.array( cleanColumn, dtype='float64' )
        # elif dataDescription[idx] == "categorical":
        #     for value in column:
        #         if value in emptyEquivalents:
        #             cleanColumn.append( 'nan' )
        #         else:
        #             cleanColumn.append(value)
        else:
            cleanColumn = column
        
        cleanedMatrix.append( cleanColumn )
    return cleanedMatrix


def impute(dataDescription, matrix ):
    resultMatrix = []
    for idx, column in enumerate(matrix):
        printParent(idx)

        if dataDescription[idx] == "numerical":
            column = imputer.fit_transform(column, y=None)
        resultMatrix.append(column)

    return resultMatrix

def cleanAll(dataDescription, matrix ):
    cleanedMatrix = standardizeMissingValues(dataDescription, matrix)
    results = impute(dataDescription, cleanedMatrix )
    return results
