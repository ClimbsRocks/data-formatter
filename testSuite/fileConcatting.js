var expect = require('chai').expect;
var mocha = require('mocha');

module.exports = function() {


  // this describe block will contain all the tests for our fileConcatting module
  describe('fileConcatting', function() {

    var results;

    before(function(done) {
      console.time('file concatting time');

      pyController.on('message', function(message) {
        // message is the message object coming to us from the Python process
        if(message.type === 'concat.py') {
          results = message.text;
          console.timeEnd('file concatting time');
          done();
        }  
      });

    });

    // this it statement describes the test. this is maybe analogous to the prompt of the question if thinking back to a university exam. 
    // by defining done as a parameter for the callback function here, we are saying this test be an asynchronous function. 
    // mocha will allow this test to run up until we invoke done(), or until the test times out.
    it('should concatenate the test data and the training data together into one large data set', function(done) {
      // 150,000 data rows in training data
      // 101,503 data rows in testing data
      expect(results[3].length).to.equal(251503);
      done();
    });

    it('should communicate back the number of rows in the training dataset, excluding the header row', function(done) {
        expect(results[2]).to.equal(150000);
        done();
    });

    it('should save the data description row separately', function(done) {
      expect(results[0]).to.deep.equal(["continuous","continuous","categorical","continuous","continuous","categorical","categorical","categorical","categorical","categorical"]);
      done();
    });

    it('should save the header row separately', function(done) {
      expect(results[1]).to.deep.equal(["revolvingutilizationofunsecuredlines", "age", "numberoftime30-59dayspastduenotworse", "debtratio", "monthlyincome", "numberofopencreditlinesandloans", "numberoftimes90dayslate", "numberrealestateloansorlines", "numberoftime60-89dayspastduenotworse", "numberofdependents"]);
      done();
    });


    after(function() {
      results[0] = null;
      results[1] = null;
      results[2] = null;
      results[3] = null;
      results = null;
    });

  });
};
