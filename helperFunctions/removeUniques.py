from sendMessages import printParent
from sendMessages import messageParent
from sendMessages import obviousPrint
emptyEquivalents = ["na","n/a","none",'',"","undefined","missing","blank","empty", None]

def remove( rowMatrix, dataDescription, headerRow ):
    columnsToDelete = {}
    columnMatrix = zip(*rowMatrix)
    for colIndex, column in enumerate( columnMatrix ):
        # it is perfectly fine for continuous columns to have unique values
        # it is only for categorical data that unique values become uninteresting
        if dataDescription[ colIndex ] == 'categorical':

            # count the values in this column
            columnCounts = {}
            for rowValue in column:
                try:
                    columnCounts[ rowValue ] += 1
                except:
                    columnCounts[ rowValue ] = 1

            keepColumn
            # now go through and remove values that appear only once
            for rowIndex, rowValue in enumerate( column ):
                if columnCounts[ rowValue ] == 1:
                    column[ rowIndex ] = None

                # make sure that this column has any useful values (i.e., has duplicated values that are not in emptyEquivalents)
                else:
                    try:
                        # if this value is in emptyEquivalents, we are not interested in it
                        emptyEquivalents.index( rowValue )
                    except:
                        # if this value has a count of more than 1 and is not in emptyEquivalents, we can keep this column!
                        keepColumn = True

            if not keepColumn:
                # flag this as a column to delete since we didn't find a single useful value in it (such as a column of raw addresses or raw names- data like that is only useful for feature engineering, not raw by itself)
                columnsToDelete[ colIndex ] = colIndex

    for colIndex in columnsToDelete:
        del columnMatrix[ colIndex ]
        del headerRow[ colIndex ]
        del dataDescription[ colIndex ]
                # TODO: Delete this column
                # delete this entry from headerRow
                # delete this entry from dataDescription
    X = zip(*columnMatrix)
    return [X, dataDescription, headerRow]
