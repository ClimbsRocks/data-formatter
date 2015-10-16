import os
import csv
import os.path as path

from sendMessages import printParent
from sendMessages import messageParent
from sendMessages import obviousPrint

def writeFile(data):
    with open( path.join( os.getcwd(), 'testWrittenData.csv' ), 'w+') as outputFile:
        csvOutputFile = csv.writer(outputFile)
        csvOutputFile.writerows(data)
        printParent('we have written your fully transformed data to a file at:')
        printParent( path.join( os.getcwd(), 'testWrittenData.csv' ) )



