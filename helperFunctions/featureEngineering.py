from dateutil.parser import parse
from sendMessages import printParent
from sklearn.feature_extraction.text import TfidfVectorizer

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
            rawString = row[nlpColumnIndex]
            cleanedString = unicode(rawString, errors='replace')
            corpus.append(cleanedString)

            # right now the value stored at the nlpColumnIndex is the entire text string
            # go through and overwrite that with a simple number representing the number of characters in that string. We will have the fuller representation of the string (using bag of words or tf-idf) stored elsewhere in this row
            row[nlpColumnIndex] = len(row[nlpColumnIndex])
            X[rowIdx] = row
        dataDescription[nlpColumnIndex] = 'continuous'
        headerRow[nlpColumnIndex] = 'lengthOf' + headerRow[nlpColumnIndex]

        # TODO: properly set the parameters here. how many words do we want to include, etc.
        # if we face a decoding error, ignore it
        # strip the accents from words to make them more consistent
        # if amalyzer='char', each word feature will be made up of character n-grams. this means 'calling' and 'called' will be more similar, because they share the characters 'c','a','l',and 'l'. if words, they would be considered two completely unrelated entities
        # if analyzer='word', each word feature will simply be the count of times that word appears in this document
        # remove english "stop words": words like 'the','it','a' that appear so frequently as to be pretty useless in creating distinguishing documents. research has shown that for most corpora, removing stop words speeds up calculation time and increases accuracy (removes noise)
        # convert all charactes to lowercase before tokenizing
        # only include the most frequently occurring 'max_features' features when building the vocabulary. In other words, if we have 80,000 unique words that appear throughout our corpus, but max_features is only 5,000, we will only include the most popular 5,000 words in the final features. This reduces noise, memory, and computation time, at the risk of ignoring useful data.

        vectorizer = TfidfVectorizer(decode_error='ignore', strip_accents='unicode', analyzer='word', stop_words='english', lowercase=True, max_features=5000)
        corpus = vectorizer.fit_transform(corpus)

        # TODO:
            # Before writing vectorizer to file, remove the stop_words attribute. Otherwise, it will take up totally unnecessary space
            # vectorizer.stop_words = None

        # TODO: get the feature names
        nlpHeaderRow = vectorizer.get_feature_names()
        nlpHeaderRow = ['_nlp' + x for x in nlpHeaderRow]
        nlpDataDescription = ['continuous' for x in nlpHeaderRow]


    return X, corpus, nlpDataDescription, nlpHeaderRow

