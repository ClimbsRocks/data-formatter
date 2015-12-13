from sendMessages import printParent
from sendMessages import messageParent
from sendMessages import obviousPrint

def clean(X):
    columnCounts = {}
    for rowObj in X:
        for key in rowObj:
            try:
                columnCounts[key] += 1
            except:
                columnCounts[key] = 1
    return X
