# going to have to think through how to handle the id and output columns. 
    # they might need to be split out separately, and then added back in?
    
from sklearn.feature_extraction import DictVectorizer
from sendMessages import printParent
from sendMessages import messageParent
from sendMessages import obviousPrint


vectorizer = DictVectorizer()

def vectorize(listOfDicts):
    listOfDicts = vectorizer.fit_transform(listOfDicts).toarray()
    printParent( 'vocabulary_' )
    printParent( vectorizer.vocabulary_ )
    printParent( 'feature_names_' )
    printParent( vectorizer.feature_names_ )
    return [ listOfDicts, vectorizer.feature_names_, vectorizer.vocabulary_ ]

