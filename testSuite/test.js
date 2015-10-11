var expect = require('chai').expect;
var mocha = require('mocha');
var path = require('path');
var testFolder = path.dirname(__filename);
var fs = require('fs');
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

var startPyController = function() {
  var pyOptions = makePyOptions(path.join(testFolder, 'trainKaggleGiveMeSomeCredit.csv'), path.join(testFolder, 'testKaggleGiveMeSomeCredit.csv'), 'test');

  var pyController = PythonShell.run('pyController.py', pyOptions, function(err) {
    if(err) {
      console.log('heard an error!');
      console.error(err);
      console.log('above is the error');
    }
  });

  attachListeners(pyController);
  return pyController;
}

process.emit('message',"this is my test message for mocha that is not valid");

// this block will contain all the tests for the entire data-formatter package
describe('data-formatter', function() {

  // this describe block will contain all the tests for our fileConcatting module
  describe('fileConcatting', function() {

    // if we write the results to disk, mae sure to erase them so we are starting from fresh results
    // before(function() {
    //   fs.unlinkSync(path.join(testFolder,'concattedtrainKaggleGiveMeSomeCredit.csv'));
    // });

    // this it statement describes the test. this is maybe analogous to the prompt of the question if thinking back to a university exam. 
    // by defining done as a parameter for the callback function here, we are saying this test be an asynchronous function. 
    // mocha will allow this test to run up until we invoke done(), or until the test times out.
    it('should concatenate the test data and the training data together into one large data set', function(done) {
      var pyController = startPyController();

      pyController.on('message', function(message) {
        // message is the message object coming to us from the Python process
        // we are expecting to get back an array of the concatted results
        if(message.type === 'concat.py') {
          // 1 header row in training data
          // 150,000 data rows in training data
          // 101,503 data rows in testing data
          expect(message.text[1].length).to.equal(251504);
          done();
        }
      
      });
    });

    it('should communicate back the number of rows in the training dataset, including the header row', function(done) {
      var pyController = startPyController();

      pyController.on('message', function(message) {
        // message is the message object coming to us from the Python process
        // we are expecting to get back an array of the concatted results
        if(message.type === 'concat.py') {
          // 1 header row in training data
          // 150,000 data rows in training data
          // 101,503 data rows in testing data
          expect(message.text[0]).to.equal(150001);
          done();
        }
      
      });
    });

    // should return the number of rows, and the concatted list
    // test both parts to make sure they are what we expect

  });




});
