import os
import csv
import os.path as path

from sendMessages import printParent
from sendMessages import messageParent
from sendMessages import obviousPrint

def writeFile(data):
    printParent('os.getcwd() is:')
    printParent( os.getcwd() )
    with open( path.join( os.getcwd(), 'testWrittenData.csv' ), 'w+') as outputFile:
        csvOutputFile = csv.writer(outputFile)
        csvOutputFile.writerows(data)
        printParent('wrote the file!')
        printParent( path.join( os.getcwd(), 'testWrittenData.csv' ) )



