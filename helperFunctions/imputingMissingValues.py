from sklearn import preprocessing
import numpy as np

from sendMessages import printParent
from sendMessages import messageParent
from sendMessages import obviousPrint

import writeToFile

emptyEquivalents = ["na","n/a","none",'',"","undefined","missing","blank","empty", None]

# standardizes all missing values to ""
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
                    cleanColumn.append( "" )
                    # and keep track of this column as having msising values
                    columnsWithMissingValues[idx] = True

        elif dataDescription[idx] == "categorical":
            # if it's categorical
            for value in column:
                if str(value).lower() in emptyEquivalents:
                    # replace all values we have defined above as being equivalent to a missing value with the standardized version the inputer will recognize next: np.nan
                    cleanColumn.append( "" )
                    # and keep track of this column as having msising values
                    columnsWithMissingValues[idx] = True
                
                else:
                    cleanColumn.append(value)
        cleanedColumnMatrix.append( cleanColumn )

    return [ cleanedColumnMatrix, columnsWithMissingValues ]


def calculateReplacementValues( columnMatrix, columnsWithMissingValues, dataDescription ):

    # fillInVals will have keys for each column index, and values for what the filled in value should be
        # this way we only need to check continuous or categorical once
    fillInVals = {}
    # for colIndex, column in enumerate(columnMatrix):
        # do this only for columns with missing values
    for colIndex in columnsWithMissingValues:
        try:
            # we have a string in our columnsWithMissingValues obj (countOfMissingValues), so we need to try to convert it into an int to make sure we're actually on a numerical key representing a column number
            colIndex = int( colIndex )
            if dataDescription[ colIndex ] == 'continuous':
            # Manually calculating the median value
            # the numpy way of doing this assumes that None is a number and includes it when calculating the median value
            # whereas we want the median of all the values other than None. 
                # copy the list
                copiedList = list( columnMatrix[ colIndex ])
                # sort the list
                copiedList.sort()
                # find the index of None
                for rowIndex, value in enumerate(copiedList):
                    if value == "":
                        noneIndex = rowIndex
                        break
                        # TODO: delete the copied list
                # divide that number in half (make it an int)
                medianIndex = int( noneIndex / 2 )
                # access that position in the copied & sorted list
                medianVal = copiedList[ medianIndex ]
                # store that number into fillInVals
                fillInVals[ colIndex ] = medianVal
                # TODO: delete that sorted/copied list

            elif dataDescription[ colIndex ] == 'categorical':
                column = columnMatrix[ colIndex ]
                # the mode value
                fillInVals[ colIndex ] = max(set(column), key=column.count)
        except: 
            printParent('we failed to create a fillInVals value for this key')
            printParent(colIndex)
            pass

    # remove all values of None from fillInVals
    # this way we will only create imputed columns if we can replace missing values in that column with something useful
    fillInVals = { k: v for k, v in fillInVals.items() if v is not None}

    return fillInVals


def createImputedColumns( columnMatrix, dataDescription, fillInVals, headerRow ):
    # colMap will hold information on where to find the imputed and boolean flag coluns for each column with missing values in the initial dataset
    colMap = {}

    # we want to keep track of the total number of imputed values for each row
    # but it only makes sense to have a total column if we have more than 1 column with missing values
    # we can probably get rid of this with robust feature selection
    if( len( fillInVals.keys() ) > 1 ):
        # create a new empty list that is filled with blank values (None) that is the length of a standard column
        emptyList = [ 0 ] * len( columnMatrix[0] )
        columnMatrix.append( emptyList )
        # keep track of this new column in our headerRow and our dataDescription row
        dataDescription.append( 'Continuous' )
        headerRow.append( 'countOfMissingValues' )
        # keep track of where this new column is
        colMap[ 'countOfMissingValues' ] = len(headerRow) - 1
    
    for colIndex in fillInVals:
        colIndex = int(colIndex)
        # create a copy of the existing column and append it to the end. this way we can modify one column, but leave the original column untouched
        # this allows us many more options, and then choose among them empirically using the feature selection module
        newColumn = list( columnMatrix[ colIndex ])
        columnMatrix.append( newColumn )

        # include prettyNames for dataDescription and header row
        dataDescription.append( dataDescription[colIndex] ) 
        headerRow.append( 'imputedValues' + headerRow[ colIndex ] )

        # we now have a map between the original (untouched) column index, and the new cloned (with imputed values) column index
        colMap[ colIndex ] = len( headerRow ) -1

        # create a new empty column to hold information on whether this row has an imputed value for the current column
        emptyList = [ 0 ] * len( columnMatrix[0] )
        columnMatrix.append( emptyList )
        # keep track of this new column in our headerRow and our dataDescription row
        dataDescription.append( 'Continuous' )
        headerRow.append( 'missing' + headerRow[ colIndex ] )

    return [ columnMatrix, dataDescription, colMap, headerRow ]


def impute( columnMatrix, dataDescription, colMap, fillInVals ):
    # we have one column dedicated just to holding the count of the total number of missing values for this row
    # however, if we only have one column with missing values, we will not have this countOfMissingValues column
    try:
        countOfMissingValsColIndex = colMap[ 'countOfMissingValues' ]
    except:
        pass

    for colIndex, column in enumerate(columnMatrix):
        if dataDescription[ colIndex ] == 'categorical':
            isCategorical = True
        else:
            isCategorical = False
        # iterate through columns list, starting at the index position of the new columns
        try:
            # check to make sure this colIndex is indeed a cloned column with missing values (not a column holding a boolean flag for whether a missing value was found)
            # find the column where we are going to store the imputed values for this column
            # if this column is not one of the columns we've identified earlier as having missing values, this will throw an error and exit the try statement
            imputedColIndex = colMap[ colIndex ]
            # if so
            for rowIndex, value in enumerate(column):
                # iterate through list, with rowIndex
                # for each item:
                # check for missing values. if they exist:
                if value == "":

                    # there are several components we must balance here:
                        # np.median does not like columns with mixed values (numbers and strings)
                        # the random forest classifier does not appear to like None or nan
                        # and of course, we need to clean the input (no strings in numerical columns, have a reliable missingValues value we can look for, etc.)
                    # we need to remove all np.nan from our input, otherwise the classifier fails later on. 
                    columnMatrix[ colIndex ][ rowIndex ] = "NA"


                    # replace missing value in the imputedColumn we have appended at the right-hand side of the dataset for each column with missing values
                    # replace it for this row that we are iterating over
                    # replace it with the previously calculated value for this column
                    columnMatrix[ imputedColIndex ][ rowIndex ] = fillInVals[ colIndex ]
                    # find the flag column for this column in colMap dictionary
                        # it is just one over from the imputedColumn
                        # set that value equal to 1
                    columnMatrix[ imputedColIndex + 1 ][ rowIndex ] = 1

                    try:
                        # find the column holding the count of all missing values for that row
                            # increment that value by 1
                        columnMatrix[ countOfMissingValsColIndex ][ rowIndex ] += 1
                    except:
                        pass
        except:
            pass
            # if this is not a column we've previously identified as having missing values, do nothing
    return columnMatrix


# cleanAll is the function that will be publicly invoked. 
# cleanAll simply plays controller for the functions defined above
def cleanAll(dataDescription, matrix, headerRow ):

    # standardize missing values to all be None
    # standardizedResults = standardizeMissingValues(dataDescription, matrix)
    cleanedColumnMatrix, columnsWithMissingValues = standardizeMissingValues(dataDescription, matrix)
    # cleanedColumnMatrix = standardizedResults[ 0 ]
    # columnsWithMissingValues = standardizedResults[ 1 ]


    # calculate the replacement values for columns that are missing values
    fillInVals = calculateReplacementValues( cleanedColumnMatrix, columnsWithMissingValues, dataDescription )

    # create the new columns for each column that has a missing value
    # newColumnsResults = createImputedColumns( cleanedColumnMatrix, dataDescription, fillInVals, headerRow )
    cleanedColumnMatrix, dataDescription, columnsWithMissingValues, headerRow = createImputedColumns( cleanedColumnMatrix, dataDescription, fillInVals, headerRow )

    # store results from creating the imputed columns
    # cleanedColumnMatrix = newColumnsResults[ 0 ]
    # dataDescription = newColumnsResults[ 1 ]
    # columnsWithMissingValues = newColumnsResults[ 2 ]
    # headerRow = newColumnsResults[ 3 ]

    # impute the missing values and boolean flags for the newly copied columns
    cleanedColumnMatrix = impute( cleanedColumnMatrix, dataDescription, columnsWithMissingValues, fillInVals )

    # turn back into a row matrix from a column matrix
    cleanedRowMatrix = zip(*cleanedColumnMatrix)

    # return all the new values (X, dataDescription, headerRow)
        # since we are adding on new columns, we have modified the dataDescription and headerRow variables
    return cleanedRowMatrix, dataDescription, headerRow
