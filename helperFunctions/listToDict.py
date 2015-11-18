from sendMessages import printParent

def all(matrix, headerRow):
    listOfDicts = []
    for row in matrix:
        rowDict = {}
        for idx, val in enumerate(row):
            rowDict[ headerRow[idx] ] = val
        listOfDicts.append( rowDict )
    return listOfDicts
