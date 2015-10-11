import json

def printParent(input):
    messageObj = {
        'body': input,
        'type': 'console.log'
    }
    print json.dumps(messageObj)

def messageParent(input, type):
    messageObj = {
        'body': input,
        'type': type
    }
    print json.dumps(messageObj)

def obviousPrint(label, obj):
    printParent('#######################################################################################################################')
    printParent(label)
    printParent('#######################################################################################################################')
    printParent(obj)
