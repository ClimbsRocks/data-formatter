from sendMessages import printParent
from sendMessages import obviousPrint
from itertools import chain, combinations

import numpy as np

def compute(X, groupByIndices, dataDescription, headerRow, outputColumn, trainingLength ):

    # precompute the powerSet of groupByIndices
    # straight from the python docs: https://docs.python.org/2/library/itertools.html#recipes
    def powerset(iterable):
        # "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
        s = list(iterable)
        return chain.from_iterable(combinations(s, r) for r in range(len(s)+1))

    allCombinations = list(powerset(groupByIndices))
    # the first item in here is just the empty (blank) set, so let's remove that
    allCombinations.pop(0)

    summary = {}

    # calculate what each of those indices mean for this row
    # combination is going to be a list of indices
    # we must grab the values at those indices for this row
        # e.g. storeId2DayOfWeek5Holiday0
    def specificCombinationCalculator(row, indices):
        specificCombo = 'grouped'
        for indicesIdx, groupByIndex in enumerate(indices):
            # grab the header row (for context), and then the value for this row (e.g. storeID + 158 = 'storeID158')
            try:
                val = headerRow[groupByIndex] + str(row[groupByIndex])
            except:
                val = headerRow[groupByIndex] + row[groupByIndex]
            specificCombo += val

            # separate each value with the word 'By', as in 'salesBystore'
            if indicesIdx < len(indices) - 1:
                specificCombo += 'By'
        return specificCombo


    # iterate through all the rows in our dataset (X)
        # we can only compute the known outcome for the rows in our training dataset, but X right now holds the combined training and testing dataset
        # iterate only through the training data portion
    for rowID, row in enumerate( X ):
        if rowID < trainingLength:
            # we have already precomputed all the possible combinations of the indices in groupByIndices
            # we want to perform this summarization on each of those combinations
            for combination in allCombinations:

                # what values do those indices translate to for this specific row?
                rowSpecificCombination = specificCombinationCalculator( row, combination )

                # add this row's output value to this particular row's combination in summary
                # each rowSpecificCombination is going to be an array, which makes mode and average and numOccurrences all super easy to calculate
                thisRowsYVal = outputColumn[ rowID ]
                try:
                    summary[ rowSpecificCombination ].append( thisRowsYVal )
                except:
                    summary[ rowSpecificCombination ] = [ thisRowsYVal ]


    statsSummary = {}
    for key in summary:
        statsSummary[key] = {
            'average': np.average(summary[key]),
            'median': np.median(summary[key]),
            # 'min': np.nanmin(summary[key]),
            # 'max': np.nanmax(summary[key]),
            # 'range': np.nanmax(summary[key]) - np.nanmin(summary[key]),
            # 'variance': np.var(summary[key])
        }
        summary[key] = None

    # repeat the process!
        # except this time, instead of summarizing, we want to either average or median or min or max or range or all of the above, for all of the combos seen in this row
            # i vote for all of the above, and then we'll just have to put more attention into feature selection
    # iterate through X again
        # this time, make sure to include the calculated value for the training and test dataset (the entire X)
    appendedHeader = False
    for row in X:
        # iterate through all the possible combinations of groupBy features we calculated earlier
        for combination in allCombinations:

            rowSpecificCombination = specificCombinationCalculator( row, combination )

            try:
                rowStats = statsSummary[rowSpecificCombination]
            except:
                # this is for the case where we have combinations of values in our test dataset that we do not have in our train dataset
                # we'll just fill those in with blank values and then let imputer and feature selection take care of the rest
                rowStats = {
                    'average': '',
                    'median': '',
                    # 'min': '',
                    # 'max': '',
                    # 'range': '',
                    # 'variance': ''
                }

            for statName in rowStats:
                row.append(rowStats[statName])

            # if this is our first row, we have to update the header as well, since we are adding in new columns
            if appendedHeader == False:
                baseName = 'grouped'
                for indicesIdx, colIndex in enumerate(combination):
                    # grab the header row (for context)
                    baseName += headerRow[colIndex]

                    # separate each value with the word 'By', as in 'salesBystore'
                    if indicesIdx < len(combination) - 1:
                        baseName += 'By'

                for statName in rowStats:
                    headerRow.append( baseName + statName )
    
                    # each of these calculated combinations must be a number
                    # this will have to be updated once we have multi-label or multi-category predictions
                    dataDescription.append('continuous')


        appendedHeader = True
    
    del summary
    del statsSummary
    return X, dataDescription, headerRow
