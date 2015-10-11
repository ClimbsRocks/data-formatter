import json

def printParent(messageText):
    messageObj = {
        'text': messageText,
        'type': 'console.log'
    }
    print json.dumps(messageObj)

def messageParent(messageText, type):
    messageObj = {
        'text': messageText,
        'type': type
    }
    print json.dumps(messageObj)

def obviousPrint(label, obj):
    printParent('#######################################################################################################################')
    printParent(label)
    printParent('#######################################################################################################################')
    printParent(obj)
