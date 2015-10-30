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
    # FUTURE: handle data where the IDs are not sorted
        # We could easily just save this into a giant dictionary, instead of a results list
        # The key would be the ID, and the value would be this rowObj
        # Then we could just create it if it doesn't exist, and add to it if it does exist

    idIndex = dataDescription.index('id')

    # FUTURE: support multiple continuous values for each row (number of items purchased, and total $ sales, for example)
    valueIndex = dataDescription.index('continuous')
    valueHeader = headerRow[ valueIndex ]

    results = {}
    ### TODO:
    # iterate through list
    for row in X:
        rowID = row[idIndex]

        # create a rowObj for each rowID, if we don't have one for this rowID already saved in our results dictionary
        try:
            rowObj = results[rowID]
            rowObj['rowCount'] += 1
        except:
            results[rowID] = {}
            rowObj = results[rowID]
            rowObj['rowCount'] = 1

        # There is going to be one value for each row (e.g. number of items sold)
        rowValue = row[ valueIndex ]
        for columnIndex in row:
            # Then, for each categorical value (department, sub-department, etc.), sum up that rowValue
            # Thus, if we make multiple purchases in the biking section, we will have all of that summed up for this ID (either customer or trip or anything else we are given as an ID)
            if dataDescription[columnIndex] == 'categorical':
                columnHeader = headerRow[ columnIndex ]
                try:
                    rowObj[ columnHeader + valueHeader ] += rowValue
                    rowObj[ columnHeader + valueHeader + 'count' ] += rowValue
                except:
                    # for each column that is categorical, add a property to the rowObj, if it does not exist already 
                    # add the continuous value for that row to the value for this property 
                    rowObj[ columnHeader + valueHeader ] = rowValue
                    rowObj[ columnHeader + valueHeader + 'count' ] = rowValue


                # FUTURE: support having multiple continuous values added for each ID (count and price, for example)
                # create counts of all these variables
                    # number of rows
                    # number of rows for each categorical value (dairy, for example)
                    
    # TODO TODO: figure out the format of what we need to return
        # Figure out if we can/should do this after removeUniques
        # modify our header row
            # This should be relatively easy, since we don't have any ID or output columns to worry about here, and we're summing up all the continuous columns
            # our column headers now should just be all the keys of our row dictionaries, which will be turned into lists with dictVectorizer
    return results
