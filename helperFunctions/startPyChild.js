var path = require('path');
var dfDirectory = path.dirname(__filename);
var child_process = require('child_process');
var PythonShell = require('python-shell');

var fileNames = {
  // this will be filled with messages returned to us by the python scripts
};


var makePyOptions = function() {
  var pyOptions = {
    mode: 'json',
    scriptPath: path.resolve(dfDirectory),
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
    } else if( message.type === 'fileNames' ) {
      for( var key in message.text ) {
        fileNames[key] = message.text[key];
      }
    } 
    // this seems to help a lot with having node's garbage collection kick in quickly.
    message.text = null;
  });
};

module.exports = function( argsObject, callback ) {

  var pyOptions = makePyOptions( JSON.stringify( argsObject ) );

  var pyController = PythonShell.run('../mainPythonProcess.py', pyOptions, function(err) {
    // exit code null means we killed the python child process intentionally
    if(err && err.exitCode !== null) {
      console.log('heard an error!');
      try {
        console.error(JSON.parse(err));
      } catch(parseError) {
        console.error(err);
      }
    } else {
      process.emit('finishedFormatting');
      if (typeof callback === 'function' ) {
        callback(fileNames);
      }
    }

    
  });

  attachListeners(pyController);
  return pyController;
};
