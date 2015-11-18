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

        headerRow.append('daysSinceFirstDay')
        dataDescription.append('numerical')

        # note, the holidays will only apply to US holidays at first.
        # i'd love a PR that expands support to other countries!
        # headerRow.append('isFederalHoliday')
        # dataDescription.append('categorical')

        # headerRow.append('isNonFederalHoliday')
        # dataDescription.append('categorical')

        for rowIdx, row in enumerate(X):
            # turn the string of the date into a datetime object
            # dateutil.parser.parse will automatically detect the format of the string (or at least attempt to)
            rowDate = parse(row[dateColumnIndex])
            
            

    except:
        pass
    
    return (X, dataDescription)

