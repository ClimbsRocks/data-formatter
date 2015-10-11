var expect = require('chai').expect;
var mocha = require('mocha');
var path = require('path');
var testFolder = path.dirname(__filename);
var fs = require('fs');
var child_process = require('child_process');

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
      var pyController = child_process.fork(path.resolve(testFolder,'..','pyController.py'));
      pyController.on('message', function(message) {
        // message is the message object coming to us from the Python process
        // we are expecting to get back an array of the concatted results
        if(message.type === 'concat.py') {
          expect(message.body.length).to.equal(251503);
          expect(message.body.trainingLength).to.equal(150000);
          done();
        }
      
      });
    });

    // should return the number of rows, and the concatted list
    // test both parts to make sure they are what we expect

  });




});
