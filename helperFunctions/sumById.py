import listToDict
import json

# some functions to help with logging
from helperFunctions.sendMessages import printParent
from helperFunctions.sendMessages import messageParent
from helperFunctions.sendMessages import obviousPrint


def sum( dataDescription, X, headerRow, idColumn, trainingLength, outputColumn):
    if checkForDupes(idColumn, trainingLength):
        printParent('We have found multiple rows with the same ID in them.')
        printParent('We are going to assume that all rows with the same ID in them should be summed up intelligently')
        printParent('This will tranform your dataset from being "long" to being "wide".')
        printParent('If this is not what you intended, please submit an issue and/or a Pull Request explaining your sitaution!')
        # TODO: we now have two different return formats: dictionaries, and lists
        # probably easiest to convert X to dictionaries here regardless of whether it has dupes or not
        # hmmm, imputing missing values would likely be less useful for these cases
            # it's more likely that we would have a separate file entirely for the metadata associated with each row (name, age, gender if our repeated ID is a customerID)
            # let's ignore this for now (MVP!), and then think later about imputing missing values on only the non-joined data, then joining in that data later. that would likely be much more space efficient than joining in that data up front
        return groupByID(dataDescription, X, headerRow, idColumn, trainingLength, outputColumn)
        

    else:
        return [listToDict.all( X, headerRow ), idColumn, trainingLength, outputColumn]

# check to see if we have duplicate IDs in this data set
def checkForDupes( idColumn, trainingLength ):
    idCounts = {}
    for rowIndex, ID in enumerate(idColumn):
        try: 
            if idCounts[ID] == 1 and rowIndex < trainingLength:
                # if we can access this property in idCounts, that means we already have a value there, and can return true!
                return True
        except:
            idCounts[ID] = 1

    return False

def groupByID(dataDescription, X, headerRow, idColumn, trainingLength, outputColumn):
    # TODO: take in the output column as well, add it to each rowObj, and then split back out again following the exact same process we are for the idColumn
    # FUTURE: handle data where the IDs are not sorted
        # We could easily just save this into a giant dictionary, instead of a results list
        # The key would be the ID, and the value would be this rowObj
        # Then we could just create it if it doesn't exist, and add to it if it does exist


    # FUTURE: support multiple continuous values for each row (number of items purchased, and total $ sales, for example)
    valueIndex = dataDescription.index('continuous')
    valueHeader = headerRow[ valueIndex ]

    results = {}
    trainingIDs = {}
    newTrainingLength = 0
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

            # if we have to create a new rowObj, that means that we have not encountered this ID before. 
            # not encountering this ID before, and being in a position within our X dataset that is less than the training length, means that this is a new, unique row summary that belongs to our trainingLength

            if rowIndex < trainingLength:
                newTrainingLength += 1
                trainingIDs[rowID] = True
                rowObj['output'] = outputColumn[rowIndex]
        # There is going to be one value for each row (e.g. number of items sold)
        rowValue = row[ valueIndex ]
        for columnIndex, value in enumerate(row):
            # Then, for each categorical value (department, sub-department, etc.), sum up that rowValue
            # Thus, if we make multiple purchases in the biking section, we will have all of that summed up for this ID (either customer or trip or anything else we are given as an ID)
            if dataDescription[columnIndex] == 'categorical':
                columnHeader = headerRow[ columnIndex ]
                try:
                    rowObj[ columnHeader + value + valueHeader ] += rowValue
                    # how many different times this ID has had this value for this column
                        # e.g., how many times the sub-department "Road Bikes" has popped up for this ID
                    rowObj[ columnHeader + value + valueHeader + 'count' ] += rowValue
                except:
                    # for each column that is categorical, add a property to the rowObj, if it does not exist already 
                    # add the continuous value for that row to the value for this property 
                    rowObj[ columnHeader + str(value) + valueHeader ] = rowValue
                    rowObj[ columnHeader + str(value) + valueHeader + 'count' ] = rowValue
                    # total categories this ID will eventually hold
                    rowObj['categoryCount'] += 1

                    # total categories- for this column- this ID will eventually hold
                        # e.g., if we have a column dedicated to the sub-departments of that store, how many different sub-departments (Road Bikes, Mountain Bikes, and Rock Climbing) this ID will hold
                    try:
                        rowObj[columnHeader + 'count'] += 1
                    except:
                        rowObj[columnHeader + 'count'] = 1



                # FUTURE: support having multiple continuous values added for each ID (count and price, for example)
                # create counts of all these variables
                    # number of rows
                    # number of rows for each categorical value (dairy, for example)

    listResults = results.values()
    idColumn = []

    # TODO: 
        # create a list of IDs that are in the training set
        # once we have turned back into a list again, iterate through each object
        # based on it's ID, put it into either a training or testing dataset
        # then at the end, concat the training and testing datasets together again. 
        # 

    # since we have no idea what order the rowDicts will be in once we've put them into listResults, we must go through and carefully separate out the training and testing datasets
    # part of that separation includes creating a new idColumn, since we now have fewer rows, and a new outputColumn, for the same reason.
    trainingData = []
    trainingIDColumn = []
    testingData = []
    testingIDColumn = []
    outputColumn = []
    for rowDict in listResults:
        rowID = rowDict.pop('id', None)
        try:
            if trainingIDs[str(rowID)] == True:
                trainingData.append(rowDict)
                trainingIDColumn.append( rowID )
                outputColumn.append( rowDict.pop('output', None) )
            else:
                testingData.append( rowDict )
                testingIDColumn.append( rowID )
        except: 
            testingData.append( rowDict )
            testingIDColumn.append( rowID )
    
    listResults = trainingData + testingData
    idColumn = trainingIDColumn + testingIDColumn
    return [listResults, idColumn, newTrainingLength, outputColumn]
