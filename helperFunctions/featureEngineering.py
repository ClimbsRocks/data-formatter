from dateutil.parser import parse

def dates(X, dataDescription, headerRow):
    try:
        dateColumnIndex = dataDescription.index('date')

        headerRow.append('dayOfWeek')
        dataDescription.append('categorical')
        
        headerRow.append('year')
        dataDescription.append('categorical')
        
        headerRow.append('month')
        dataDescription.append('categorical')
        
        headerRow.append('dayOfMonth')
        dataDescription.append('categorical')
        
        headerRow.append('isWeekend')
        dataDescription.append('categorical')

        headerRow.append('daysSinceMinDate')
        dataDescription.append('numerical')

        # note, the holidays will only apply to US holidays at first.
        # i'd love a PR that expands support to other countries!
        # sweet, holidays shouldn't be too difficult!
            # http://stackoverflow.com/questions/2394235/detecting-a-us-holiday
        # headerRow.append('isFederalHoliday')
        # dataDescription.append('categorical')

        # headerRow.append('isNonFederalHoliday')
        # dataDescription.append('categorical')

        # set our minDate equal to the first date in the dataset as a starting value
        # we will then compare each date against this to find the lowest.
        minDate = parse(X[0][dateColumnIndex])

        for rowIdx, row in enumerate(X):
            # TODO: put each iteration inside it's own try block, so that if we do not have a date for one row, the rest of the rows will be ok, and then we can go through and impute values for the missing date
            # turn the string of the date into a datetime object
            # dateutil.parser.parse will automatically detect the format of the string (or at least attempt to)
            rowDate = parse(row[dateColumnIndex])

            # save that datetime object in place of the original string (temporarily)
            # this will save us having to parse this date again on the second iteration through when we set daysSinceMinDate
            row[dateColumnIndex] = rowDate
            if rowDate < minDate:
                minDate = rowDate

            dayOfWeek = rowDate.weekday()
            row.append( dayOfWeek )
            row.append(rowDate.year)
            row.append(rowDate.day)

            # boolean flag for whether this is a weekend or not
            # note that in Python, the week starts at 0 on Mondays, whereas in JS, the week starts at 0 on Sundays
            if dayOfWeek in [5,6]:
                row.append(True)
            else:
                row.append(False)

            X[rowIdx] = row

        for rowIdx, row in enumerate(X):
            # right now the value stored at the dateColumnIndex is a datetime object from the previous iteration
            # go through and overwrite that with a simple number representing the number of days since the first day in the dataset
            row[dateColumnIndex] = row[dateColumnIndex] - minDate
            X[rowIdx] = row


    except:
        printParent('we were not able to feature engineer the dates')
        pass
    
    return (X, dataDescription)

