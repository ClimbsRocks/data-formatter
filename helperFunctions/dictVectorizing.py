from sklearn.feature_extraction import DictVectorizer
from sendMessages import printParent
from sendMessages import messageParent
from sendMessages import obviousPrint


vectorizer = DictVectorizer()

def vectorize(listOfDicts):
    printParent('about to dict vectorize the data')
    # listOfDicts = vectorizer.fit_transform(listOfDicts).toarray()
    listOfDicts = vectorizer.fit_transform(listOfDicts)
    return [ listOfDicts, vectorizer.feature_names_, vectorizer.vocabulary_ ]

