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
}

module.exports = function() {
  var args = {
    trainingData: path.join(testFolder, 'trainKaggleGiveMeSomeCredit.csv'),
    testingData: path.join(testFolder, 'testKaggleGiveMeSomeCredit.csv'),
    test: true
  };
  var pyOptions = makePyOptions( JSON.stringify( args ) );
  // var pyOptions = makePyOptions(path.join(testFolder, 'trainKaggleGiveMeSomeCredit.csv'), path.join(testFolder, 'testKaggleGiveMeSomeCredit.csv'), 'test');

  var pyController = PythonShell.run('pyController.py', pyOptions, function(err) {
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
}
