import csv
from sendMessages import printParent
from sendMessages import messageParent
from sendMessages import obviousPrint

def inputFiles(trainingFile, testingFile):
    printParent('inside inputFiles')
    printParent(trainingFile)
    trainingRows = csv.reader(trainingFile)
    for row in trainingRows:
        printParent(row)
