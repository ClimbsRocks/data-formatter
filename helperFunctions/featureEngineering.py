from dateutil.parser import parse
from sendMessages import printParent

def dates(X, dataDescription, headerRow):
    hasDateColumn = False
    try:
        dateColumnIndex = dataDescription.index('date')
        hasDateColumn = True
    except:
        printParent('we were not able to feature engineer the dates')
        pass

    if hasDateColumn:
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

        # the machine learning algorithms won't know how to intrepret a datetime object
        # so we will instead replace the datetime object with a measure of how many days this row has been since the minimum date in the dataset. 
        headerRow[dateColumnIndex] = 'daysSinceMinDate'
        dataDescription[dateColumnIndex] = 'continuous'

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

            # turn all of these integers into strings, because they are going to be handled as categorical values.
            # data-formatter assumes categorical values are strings for things like using as the key in dictionaries
            dayOfWeek = rowDate.weekday()
            row.append( str(dayOfWeek) )
            row.append(str(rowDate.year))
            row.append(str(rowDate.month))
            row.append(str(rowDate.day))

            # (stringified) boolean flag for whether this is a weekend or not
            # note that in Python, the week starts at 0 on Mondays, whereas in JS, the week starts at 0 on Sundays
            if dayOfWeek in [5,6]:
                row.append(str(True))
            else:
                row.append(str(False))

            X[rowIdx] = row

        for rowIdx, row in enumerate(X):
            # right now the value stored at the dateColumnIndex is a datetime object from the previous iteration
            # go through and overwrite that with a simple number representing the number of days since the first day in the dataset
            row[dateColumnIndex] = (row[dateColumnIndex] - minDate).days
            X[rowIdx] = row

        printParent('successfully ran featureEngineering.dates!')

    return X, dataDescription, headerRow

def nlp(X, dataDescription, headerRow):
        hasnlpColumn = False
    try:
        nlpColumnIndex = dataDescription.index('nlp')
        hasnlpColumn = True
    except:
        printParent('we did not find any nlp column to perform feature engineering on')
        pass

    if hasnlpColumn:
        # TODO: use TfidfVectorizer
            # iterate through each row, grabbing the nlp column
            # run this entire collected corpus through TfidfVectorizer, store into tfVectorized
            # figure out what to add to the headerRow and dataDescription row
                # one option is to add the actual word, if we can get that (we should be able to). it appears to exist in get_feature_names()
                # we might decide that we want to keep all the nlp words, in which case we'd want to prefix all these columns in dataDescription and headerRow with "nlp"
            # don't actually add tfVectorized to X yet. X is still dense, while tfVectorized is sparse. 
                # simply pass tfVectorized (along with what should be added to headerRow and dataDescription) back.
                # then stack it horizontally to X once we turn X into a sparse matrix later on. 
                # no need to disrupt the entire rest of the process by converting everything to sparse right now
        
        corpus = []

        for rowIdx, row in enumerate(X):

            corpus.append(row[nlpColumnIndex])

            # right now the value stored at the nlpColumnIndex is the entire text string
            # go through and overwrite that with a simple number representing the number of characters in that string. We will have the fuller representation of the string (using bag of words or tf-idf) stored elsewhere in this row
            row[nlpColumnIndex] = len(row[nlpColumnIndex])
            X[rowIdx] = row

        # TODO: properly set the parameters here. how many words do we want to include, etc.
        vectorizer = TfidfVectorizer(min_df=1)
        vectorizer.fit_transform(corpus)

        # TODO: get the feature names
    
    
    return X, corpus, nlpDataDescription, nlpHeaderRow

