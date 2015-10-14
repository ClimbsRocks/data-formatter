# going to have to think through how to handle the id and output columns. 
    # they might need to be split out separately, and then added back in?
    
from sklearn.feature_extraction import DictVectorizer

vectorizer = DictVectorizer()

def vectorize(listOfDicts):
    return vectorizer.fit_transform(listOfDicts).toarray()

