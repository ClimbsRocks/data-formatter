# from sklearn.preprocessing import PolynomialFeatures
# degreeTwoFeatures = PolynomialFeatures(2)
from itertools import chain, combinations
import numpy as np
from sendMessages import printParent, obviousPrint

def addAll(X, headerRow, dataDescription):
    printParent('X.shape at the start of polynomialFeatures.py')
    printParent(X.shape)
    printParent('headerRow at the start of polynomialFeatures.py')
    printParent(headerRow)
    # TODO: check to make sure our data size is small enough to justify this
    # TODO: separate out so this is only the continuous columns
    columnMatrix = zip(*X)
    continuousColumns = []
    categoricalColumns = []

    # separate data into continous columns and categorical columns
    for colIdx, column in enumerate(columnMatrix):
        if dataDescription[colIdx] == 'continuous':
            continuousColumns.append(column)
        else:
            categoricalColumns.append(column)
        # make sure to not leave duplicate data around for long
        columnMatrix[colIdx] = None

    del columnMatrix
    continuousRows = zip(*continuousColumns)
    del continuousColumns

    # precompute the powerSet of groupByIndices
    # straight from the python docs: https://docs.python.org/2/library/itertools.html#recipes
    def powerset(iterable):
        # "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
        s = list(iterable)
        return chain.from_iterable(combinations(s, r) for r in range(len(s)+1))

    indicesForPowerset = range(len(continuousRows))
    allCombinations = list(powerset(indicesForPowerset))
    # the first item in here is just the empty (blank) set, so let's remove that
    allCombinations.pop(0)

    # and for each one, make sure we have a pretty version of that combination we can add to the headerRow
        # e.g. summedHeightAndWeight, dividedEarningsAndDebt, multipliedSquareFeetAndHours, etc.

    # calculate what each of those indices mean for this row
    # combination is going to be a list of indices
    # we must grab the values at those indices for this row
        # e.g. storeId2DayOfWeek5Holiday0
    def specificCombinationCalculator(startingString, indices):
        # startingString is going to be something like "Summed" or "Multiplied" to tell the user how we aggregated data together for this column
        specificCombo = startingString
        for indicesIdx, groupByIndex in enumerate(indices):
            # grab the header row 
            val = headerRow[groupByIndex]
            specificCombo += val

            # separate each value with the word 'By', as in 'salesBystore'
            if indicesIdx < len(indices) - 1:
                specificCombo += 'And'
        return specificCombo
   
    def summedValue(row, indices):
        rowSum = 0
        for idx in indices:
            rowSum += row[idx]
        return rowSum

    def multipliedValue(row, indices):
        rowProduct = 0
        for idx in indices:
            rowProduct *= row[idx]
        return rowProduct

    # this is not ideal as order matters for division
    # say we're trying to get income per capita
    # GDP / population is going to give us a very large number, while population/GDP is going to give us a very small number
    # but it's good enough for MVP!
    def dividedValue(row, indices):
        rowProduct = 0
        for idx in indices:
            rowProduct /= row[idx]
        return rowProduct

    firstRow = true
    for row in continuousRows:
        for indicesList in allCombinations:
            if firstRow:
                # add in a new pretty name to our headerRow
                # having good logging for our users is very important
                headerRow.append('Summed',indicesList)
                headerRow.append('Multiplied',indicesList)
                headerRow.append('Divided',indicesList)

                # tell dataDescription that each of these new columns is continuous
                dataDescription.append('continuous')
                dataDescription.append('continuous')
                dataDescription.append('continuous')
                # TODO: add in new header values using specificCombinationCalculator
            row.append(summedValue(row, indicesList))
            row.append(multipliedValue(row, indicesList))
            row.append(dividedValue(row, indicesList))

    # join together our categorical columns and our new continuous columns!
    newContinuousColumns = zip(*continuousRows)
    categoricalColumns.extend(newContinuousColumns)

    # categoricalColumns is no longer an accurate name for the matrix, so let's change the name
    columnX = categoricalColumns
    del categoricalColumns

    returnX = zip(*columnX)

    # X = degreeTwoFeatures.fit_transform(X)
    printParent('headerRow at the end of polynomialFeatures.py')
    printParent(headerRow)
    printParent('X.shape at the end of polynomialFeatures.py')
    printParent(returnX.shape)
    # TODO: figure out how to modify headerRow and dataDescription
    return returnX, headerRow, dataDescription
