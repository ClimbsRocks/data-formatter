var expect = require('chai').expect;
var mocha = require('mocha');
var startPyController = require('./startPyController');

module.exports = function() {
  // this describe block will contain all the tests for our fileConcatting module
  describe('fileConcatting', function() {
    // this operation can be slow, so give it some time to process:
    this.timeout(5000);

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
          pyController.childProcess.kill();
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
        // the first item in the array returned to us should be the length of the training data
        if(message.type === 'concat.py') {
          pyController.childProcess.kill();
          expect(message.text[0]).to.equal(150001);
          done();
        }
      
      });
    });

  });
};
