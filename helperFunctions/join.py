from sendMessages import printParent
from sendMessages import messageParent
from sendMessages import obviousPrint
import validation

def datasets(X, joinFileName, XHeaderRow, dataDescription, args):

    # 1. read in data in joinFileName
    joinDict = {}
    with open(joinFileName, 'rU') as joinFile:
        # detect the "dialect" of this type of csv file
        dialect = csv.Sniffer().sniff(joinFile.read(1024))
        joinFile.seek(0)
        joinRows = csv.reader(joinFile, dialect)

        rowCount = 0

        for row in joinRows:
            if rowCount < 2:
                # grab the dataDescription row and the header row, and make them both lowercase
                if rowCount == 0:
                    expectedRowLength = len( row )
                    # 2. get header row from that file
                    dataDescription = [x.lower() for x in row]
                    validation.joinDataDescription(dataDescription)

                else: 
                    validation.rowLength( row, expectedRowLength, rowCount )
                    # 3. get dataDescription row from that file 
                    headerRow = [x.lower() for x in row]

                    joinOnIdColumn = False
                    # determine joinIndex
                    try:
                        # 4. see if we have an args['on'] property to join the files on
                        joinHeader = args['on'].lower()
                    except:
                        try:
                            # see if our idColumn is what we're joining on (which seems like it'll happen at some point)
                            joinIndex = headerRow.index( args['idHeader'] )
                            joinOnIdColumn = True
                        except:
                            # 5. see if we have the same headerRow name in both files to join on
                            joinHeader =  set(headerRow).intersection(XHeaderRow)
                            joinIndex = headerRow.index( joinHeader )
            else:
                validation.rowLength( row, expectedRowLength, rowCount )
                trimmedRow = []
                joinVal = row[joinIndex]

                for idx, val in enumerate(row):
                    if dataDescription[idx] != 'id' and dataDescription[idx] != 'ignore':
                        trimmedRow.append(val)
                joinDict[ joinVal ] = trimmedRow

            # keep track of which row we are on for error logging purposes
            rowCount += 1


    # 5. join the files
        # just do it myself so we have more control and don't need to convert to dataFrames and back
        # read the join file into a dict
            # the keys for the dict will be the matching column
            # ignore any ignore columns
            # remove any ignored columns from the header row and dataDescription row
        # iterate through X. for each row:
            # append all the values in the joinFile dict for that id

    # append header rows
    # append dataDescription rows
    # return everything
