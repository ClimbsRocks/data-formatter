from sendMessages import printParent
from sendMessages import messageParent
from sendMessages import obviousPrint
import validation
import csv

def datasets(X, joinFileName, XHeaderRow, dataDescription, args, groupByIndices, dateIndices):

    # TODO: read in and remove the first row. having two "header" rows appers to be throwing off the sniffer when we have multiple commas in a single column, even if they are quote-enclosed.
    # write all but the first row (or two, possibly) to the temp.csv file.
    # read in that temp.csv file later. 
    # with open(joinFileName, 'rU') as f:
    #     with open(args['outputFolder'] + 'temp.csv','w+') as f1:
    #         f.next() # skip header line
    #         for line in f:
    #             f1.write(line)

    # 1. read in data in joinFileName
    joinDict = {}
    with open(joinFileName, 'rU') as joinFile:
        # detect the "dialect" of this type of csv file
        try:
            dialect = csv.Sniffer().sniff(joinFile.read(2048))
            joinFile.seek(0)
        except:
            dialect = 'excel'
        joinRows = csv.reader(joinFile, dialect)

        rowCount = 0
        joinedValsLength = -1

        for row in joinRows:
            if rowCount < 2:
                # grab the joinDataDescription row and the header row, and make them both lowercase
                if rowCount == 0:
                    expectedRowLength = len( row )
                    # 2. get joinDataDescription row from that file
                    joinDataDescription = [x.lower() for x in row]
                    validation.joinDataDescription(joinDataDescription)

                else: 
                    validation.rowLength( row, expectedRowLength, rowCount )
                    # 3. get header row from that file 
                    headerRow = [x.lower() for x in row]

                    joinOnIdColumn = False
                    # determine joinIndex
                    try:
                        # 4. see if we have an args['on'] property to join the files on
                        joinHeader = args['on'].lower()
                        joinIndex = headerRow.index( joinHeader )
                        xJoinIndex = XHeaderRow.index( joinHeader )
                    except:
                        try:
                            # see if our idColumn is what we're joining on (which seems like it'll happen at some point)
                            joinIndex = headerRow.index( args['idHeader'] )
                            joinOnIdColumn = True
                        except:
                            # 5. see if we have the same headerRow name in both files to join on
                            for x in headerRow:
                                if x in XHeaderRow:
                                    joinHeader = x
                            # joinHeader =  set(headerRow).intersection(XHeaderRow)
                            joinIndex = headerRow.index( joinHeader )
                            xJoinIndex = XHeaderRow.index( joinHeader )
            else:
                validation.rowLength( row, expectedRowLength, rowCount )
                trimmedRow = []
                joinVal = row[joinIndex]

                for idx, val in enumerate(row):
                    if joinDataDescription[idx] != 'id' and joinDataDescription[idx] != 'ignore' and idx != joinIndex:
                        trimmedRow.append(val)
                joinDict[ joinVal ] = trimmedRow
                if len( trimmedRow ) > joinedValsLength:
                    joinedValsLength = len( trimmedRow )

            # keep track of which row we are on for error logging purposes
            rowCount += 1

    newX = []
    # 5. join the files
    blankVals = [None for x in range(0,joinedValsLength)]
    for rowIndex, row in enumerate(X):
        if joinOnIdColumn:
            try:
                joinID = idColumn[rowIndex]
                newVals = joinDict[ joinID ]
                newX.append( row.join(newVals) )
            except:
                # append blank values so all rows still have the same number of columns
                newX.append( row.join(blankVals) )
        else:
            try:
                joinID = row[xJoinIndex]
                newVals = joinDict[ joinID ]
                newX.append( row + newVals )
            except:
                # append blank values so all rows still have the same number of columns
                newX.append( row + blankVals )
        X[rowIndex] = None
        del row

        # just do it myself so we have more control and don't need to convert to dataFrames and back
        # read the join file into a dict
            # the keys for the dict will be the matching column
            # ignore any ignore columns
            # remove any ignored columns from the header row and dataDescription row
        # iterate through X. for each row:
            # append all the values in the joinFile dict for that id

    # append header rows
    for idx, name in enumerate(headerRow):
        if joinDataDescription[idx] != 'id' and joinDataDescription[idx] != 'ignore' and idx != joinIndex:
            XHeaderRow.append(name)

    # append dataDescription rows, and our groupByIndices and dateIndices
    originalDataDescriptionLength = len(dataDescription)
    for idx, name in enumerate(joinDataDescription):
        if name != 'id' and name != 'ignore' and idx != joinIndex:
            if name[0:7] == 'groupby':
                # append only the non groupby part of this name
                dataDescription.append(name[8:])
                groupByIndices.append( idx + originalDataDescriptionLength )
            elif name == 'date':
                dataDescription.append(name)
                dateIndices.append( idx + originalDataDescriptionLength )
            else:
                dataDescription.append(name)

    del X
    return newX, dataDescription, XHeaderRow, groupByIndices, dateIndices
