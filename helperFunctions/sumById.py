def sum( dataDescription, X, headerRow, args):
    if checkForDupes(X):
        groupByID()
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
