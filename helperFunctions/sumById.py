def sum( dataDescription, X, headerRow, args):
    if checkForDupes(X):
        groupByID(dataDescription, X, headerRow, args)
    else:
        return [dataDescription, X, headerRow, args]

# check to see if we have duplicate IDs in this data set
def checkForDupes( dataDescription, X):
    idIndex = dataDescription.index('id')
    idCounts = {}
    for row in X:
        rowID = row[idIndex]
        try: 
            if idCounts[rowID] == 1:
                # if we can access this property in idCounts, that means we already have a value there, and can return true!
                return True
        except:
            idCounts[rowID] = 1
            pass
    return False

def groupByID(dataDescription, X, headerRow, args):
    ### TODO:
    iterate through list
        create a rowObj for each rowID 
        iterate through row
            for each column that is categorical, add a property to the rowObj, if it does not exist already 
                headerRowName + value name
                add the continuous value for that row to the value for this property 
                # FUTURE: support having multiple continuous values added for each ID (count and price, for example)
                # create counts of all these variables
                    # number of rows
                    # number of rows for each categorical value (dairy, for example)
        check the next row, to see if the id is the same
            if it is, repeat the process with all the columns in that row, in the same rowObj
            if it is not, push the existing rowObj into our results array, and create a new rowObj, starting the process all over again



    ###
