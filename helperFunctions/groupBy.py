from sendMessages import printParent
from sendMessages import obviousPrint
from itertools import chain, combinations

def compute(X, groupByIndices, dataDescription, headerRow, outputColumn ):

    # precompute the powerSet of groupByIndices
    # straight from the python docs: https://docs.python.org/2/library/itertools.html#recipes
    def powerset(iterable):
        # "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
        s = list(iterable)
        return chain.from_iterable(combinations(s, r) for r in range(len(s)+1))

    allCombinations = list(powerset(groupByIndices))
    # the first item in here is just the empty (blank) set, so let's remove that
    allCombinations.pop(0)

    obviousPrint('allCombinations',allCombinations)
    # and for each one, make sure we have a pretty version of that combination we can add to the headerRow
        # e.g. salesBystore, salesBystoreByDayOfWeek, etc.


    summary = {}

    # calculate what each of those indices mean for this row
    # combination is going to be a list of indices
    # we must grab the values at those indices for this row
        # e.g. storeId2DayOfWeek5Holiday0
    def specificCombinationCalculator(row, indices):
        specificCombo = ''
        for indicesIdx, groupByIndex in enumerate(indices):
            try:
                val = str(row[groupByIndex])
            except:
                val = row[groupByIndex]
            specificCombo += val

            # separate each value with the word 'By', as in 'salesBystore'
            if indicesIdx < len(indices) - 1:
                specificCombo += 'By'


    # iterate through all the rows in our dataset (X)
    for rowID, row in enumerate(X):

        # we have already precomputed all the possible combinations of the indices in groupByIndices
        # we want to perform this summarization on each of those combinations
        for combination in allCombinations:

            # what values do those indices translate to for this specific row?
            rowSpecificCombination = specificCombinationCalculator( row, combination )

            # add this row's output value to this particular row's combination in summary
            # each rowSpecificCombination is going to be an array, which makes mode and average and numOccurrences all super easy to calculate
            try:
                summary[ rowSpecificCombination ].append( outputColumn[ rowID ] )
            except:
                summary[ rowSpecificCombination ] = [ outputColumn[ rowID ] ]



    # repeat the process!
        # except this time, instead of summarizing, we want to either average or median or min or max or range or all of the above, for all of the combos seen in this row
            # i vote for all of the above, and then we'll just have to put more attention into feature selection
    # iterate through X again
    for row in X:
        # iterate through all the possible combinations of groupBy features we calculated earlier
        for combination in allCombinations:
            row.append( summary[combination] )
            headerRow.append( combinationNames[combination] )
            # each of these calculated combinations must be a number
            # this will have to be updated once we have multi-label or multi-category predictions
            dataDescription.append( 'continuous' )
