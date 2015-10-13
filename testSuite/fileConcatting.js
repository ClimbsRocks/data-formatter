var expect = require('chai').expect;
var mocha = require('mocha');
var startPyController = require('./startPyController');
var killChildProcess = require('./killChildProcess');

module.exports = function() {
  // this describe block will contain all the tests for our fileConcatting module
  describe('fileConcatting', function() {
    // this operation can be slow, so give it some time to process:

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
          killChildProcess(pyController.childProcess);
          // 150,000 data rows in training data
          // 101,503 data rows in testing data
          expect(message.text[3].length).to.equal(251503);
          done();
        }
      
      });
    });

    it('should communicate back the number of rows in the training dataset, excluding the header row', function(done) {
      var pyController = startPyController();

      pyController.on('message', function(message) {
        // the first item in the array returned to us should be the length of the training data
        if(message.type === 'concat.py') {
          var killChildProcess = require('./killChildProcess');
          killChildProcess(pyController.childProcess);
          expect(message.text[2]).to.equal(150000);
          done();
        }
      
      });
    });

    it('should save the header row separately', function(done) {
      var pyController = startPyController();

      pyController.on('message', function(message) {
        // the first item in the array returned to us should be the length of the training data
        if(message.type === 'concat.py') {
          killChildProcess(pyController.childProcess);
          expect(message.text[0]).to.deep.equal(['id','output','numerical','numerical','numerical','numerical','numerical','numerical','numerical','numerical','numerical','numerical']);
          done();
        }
      
      });
    });

    it('should save the header row separately', function(done) {
      var pyController = startPyController();

      pyController.on('message', function(message) {
        // the first item in the array returned to us should be the length of the training data
        if(message.type === 'concat.py') {
          killChildProcess(pyController.childProcess);
          expect(message.text[1]).to.deep.equal(["id", "seriousdlqin2yrs", "revolvingutilizationofunsecuredlines", "age", "numberoftime30-59dayspastduenotworse", "debtratio", "monthlyincome", "numberofopencreditlinesandloans", "numberoftimes90dayslate", "numberrealestateloansorlines", "numberoftime60-89dayspastduenotworse", "numberofdependents"]);
          done();
        }
      
      });
    });


  });
};
