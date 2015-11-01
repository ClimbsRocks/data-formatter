var path = require('path');
var testFolder = path.dirname(__filename);
var child_process = require('child_process');
var PythonShell = require('python-shell');


var makePyOptions = function() {
  var pyOptions = {
    mode: 'json',
    scriptPath: path.resolve(testFolder,'..'),
    args: []
  };
  for (var i = 0; i < arguments.length; i++) {
    pyOptions.args.push(arguments[i]);
  }
  return pyOptions;
};

var attachListeners = function(pyShell) {
  pyShell.on('message', function(message) {
    if(message.type === 'console.log') {
      console.log('message from Python:',message.text);
    }
  });
};

module.exports = function(dataSetName) {

  // by intentionally leaving the outputFolder field blank, we are implicitly adding in a test to make sure we are creating a directory at the right location (data-formatter should automatically detect which folder it is bieng invoked from, and create a directory there if one does not exist already)
  var args = {
    outputFolder: path.join(testFolder, 'formattedResults'),
    verbose: 0,
    test: true
  };
  if( dataSetName === 'giveCredit' ) {
    args['trainingData'] = path.join(testFolder, 'trainKaggleGiveMeSomeCredit.csv');
    args['testingData'] = path.join(testFolder, 'testKaggleGiveMeSomeCredit.csv');
    args['trainingPrettyName'] = 'giveCredittrain';
    args['testingPrettyName'] = 'giveCredittest';
  } else if (dataSetName === 'wmt') {
    args['trainingData'] = path.join(testFolder, 'wmt/train.csv');
    args['testingData'] = path.join(testFolder, 'wmt/test.csv');
    args['trainingPrettyName'] = 'wmtTrain';
    args['testingPrettyName'] = 'wmtTest';
  }
  var pyOptions = makePyOptions( JSON.stringify( args ) );

  var pyController = PythonShell.run('mainPythonProcess.py', pyOptions, function(err) {
    if(err) {
      // exit code null means we killed the python child process intentionally
      if(err.exitCode !== null) {
        console.log('heard an error!');
        console.error(err);
      }
    }
  });

  attachListeners(pyController);
  return pyController;
};
