import listToDict
import json

# some functions to help with logging
from helperFunctions.sendMessages import printParent
from helperFunctions.sendMessages import messageParent
from helperFunctions.sendMessages import obviousPrint


def sum( dataDescription, X, headerRow, idColumn, trainingLength):
    if checkForDupes(idColumn):
        # TODO: we now have two different return formats: dictionaries, and lists
        # probably easiest to convert X to dictionaries here regardless of whether it has dupes or not
        # hmmm, imputing missing values would likely be less useful for these cases
            # it's more likely that we would have a separate file entirely for the metadata associated with each row (name, age, gender if our repeated ID is a customerID)
            # let's ignore this for now (MVP!), and then think later about imputing missing values on only the non-joined data, then joining in that data later. that would likely be much more space efficient than joining in that data up front
        # return groupByID(dataDescription, X, headerRow, idColumn)
        return [listToDict.all( X, headerRow ), idColumn]
        

    else:
        return [listToDict.all( X, headerRow ), idColumn]

# check to see if we have duplicate IDs in this data set
def checkForDupes( idColumn ):
    idCounts = {}
    for rowIndex, ID in enumerate(idColumn):
        try: 
            if idCounts[ID] == 1 and rowIndex < trainingLength:
                # if we can access this property in idCounts, that means we already have a value there, and can return true!
                return True
        except:
            idCounts[ID] = 1
    return False

def groupByID(dataDescription, X, headerRow, idColumn):
    # FUTURE: handle data where the IDs are not sorted
        # We could easily just save this into a giant dictionary, instead of a results list
        # The key would be the ID, and the value would be this rowObj
        # Then we could just create it if it doesn't exist, and add to it if it does exist


    # FUTURE: support multiple continuous values for each row (number of items purchased, and total $ sales, for example)
    valueIndex = dataDescription.index('continuous')
    valueHeader = headerRow[ valueIndex ]

    results = {}
    ### TODO:
    # iterate through list
    for rowIndex, row in enumerate(X):
        rowID = idColumn[rowIndex]

        # create a rowObj for each rowID, if we don't have one for this rowID already saved in our results dictionary
        try:
            rowObj = results[rowID]
            rowObj['rowCount'] += 1
        except:
            results[rowID] = {}
            rowObj = results[rowID]
            # the number of rows this ID will appear in
            rowObj['rowCount'] = 1
            # the number of different categories this row will hold overall
            rowObj['categoryCount'] = 0
            # this ensures we will always have the ID value attached to the summarized results for this row, even after we turn the results dictionary into a list
            # we take this column back out again after dictVectorizer
            rowObj['id'] = rowID

        # There is going to be one value for each row (e.g. number of items sold)
        rowValue = row[ valueIndex ]
        for columnIndex, value in enumerate(row):
            # Then, for each categorical value (department, sub-department, etc.), sum up that rowValue
            # Thus, if we make multiple purchases in the biking section, we will have all of that summed up for this ID (either customer or trip or anything else we are given as an ID)
            if dataDescription[columnIndex] == 'categorical':
                columnHeader = headerRow[ columnIndex ]
                try:
                    rowObj[ columnHeader + valueHeader ] += rowValue
                    # how many different times this ID has had this value for this column
                        # e.g., how many times the sub-department "Road Bikes" has popped up for this ID
                    rowObj[ columnHeader + valueHeader + 'count' ] += rowValue
                except:
                    # for each column that is categorical, add a property to the rowObj, if it does not exist already 
                    # add the continuous value for that row to the value for this property 
                    rowObj[ columnHeader + valueHeader ] = rowValue
                    rowObj[ columnHeader + valueHeader + 'count' ] = rowValue
                    # total categories this ID will eventually hold
                    rowObj['categoryCount'] += 1
                    # total categories- for this column- this ID will eventually hold
                        # e.g., how many different sub-departments (Road Bikes, Mountain Bikes, and Rock Climbing) this ID will hold
                    try:
                        rowObj[columnHeader + 'count'] += 1
                    except:
                        rowObj[columnHeader + 'count'] = 1



                # FUTURE: support having multiple continuous values added for each ID (count and price, for example)
                # create counts of all these variables
                    # number of rows
                    # number of rows for each categorical value (dairy, for example)

    # TODO TODO: figure out the format of what we need to return
        # Figure out if we can/should do this after removeUniques
        # modify our header row
            # This should be relatively easy, since we don't have any ID or output columns to worry about here, and we're summing up all the continuous columns
            # our column headers now should just be all the keys of our row dictionaries, which will be turned into lists with dictVectorizer

    listResults = results.values()
    idColumn = []
    for rowDict in listResults:
        idColumn.append( rowDict.pop('ID', None) )
    return [listResults, idColumn]
