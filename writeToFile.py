import os
import csv
import os.path as path

from sendMessages import printParent
from sendMessages import messageParent
from sendMessages import obviousPrint

# Pre: make a folder in Node.js, and pass in that file path. That is an intermediate folder. 
# A. grab name of training data file
# B. 
# 1. write ID column to it's own file
# 2. write y column(s) to it's own file
# 3. write X to it's own file
# 

def writeFile(data):
    # we will take in the invocation directory as an argument from Node.js. for now, just use os.getcwd()
    with open( path.join( os.getcwd(), 'testWrittenData.csv' ), 'w+') as outputFile:
        csvOutputFile = csv.writer(outputFile)
        csvOutputFile.writerows(data)
        printParent('we have written your fully transformed data to a file at:')
        printParent( path.join( os.getcwd(), 'testWrittenData.csv' ) )



