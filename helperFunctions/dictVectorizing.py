from sklearn.feature_extraction import DictVectorizer
from sendMessages import printParent
from sendMessages import messageParent
from sendMessages import obviousPrint

from scipy.sparse import csr_matrix


vectorizer = DictVectorizer()

def vectorize(listOfDicts):

    # this will return a sparse matrix. however, the process of getting there is somewhat painful, memory wise
    # TODO: consider fitting the vectorizer
        # then, feed 1 item at a time through transform
        # as we do, delete the dict representation of that item
        # this way we are only holding one copy of the data in memory at a time

    # vectorizer.fit(listOfDicts)
    # sparseMatrix = csr_matrix()
        
    sparseMatrix = vectorizer.fit_transform(listOfDicts)
    for dictIdx, rowDict in enumerate(listOfDicts):
        listOfDicts[dictIdx] = None
        del rowDict
    del listOfDicts
    return [ sparseMatrix, vectorizer.feature_names_, vectorizer.vocabulary_ ]
