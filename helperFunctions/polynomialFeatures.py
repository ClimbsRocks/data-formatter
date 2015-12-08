from sklearn.preprocessing import PolynomialFeatures
degreeTwoFeatures = PolynomialFeatures(2)

from sendMessages import printParent, obviousPrint

def addAll(X, headerRow, dataDescription):
    # TODO: check to make sure our data size is small enough to justify this
    X = degreeTwoFeatures.fit_transform(X)
    printParent('X.shape inside polynomialFeatures.py')
    printParent(X.shape)
    # TODO: figure out how to modify headerRow and dataDescription
    return X, headerRow, dataDescription
