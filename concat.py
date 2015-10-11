import csv

def inputFiles(trainingFile, testingFile):
    trainingRows = csv.reader(trainingFile)
    for row in trainingRows:
        print row
