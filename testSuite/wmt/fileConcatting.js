var expect = require('chai').expect;
var mocha = require('mocha');
var startPyTest = require('./startPyTest');
var killChildProcess = require('./killChildProcess');

module.exports = function() {


  // this describe block will contain all the tests for our fileConcatting module
  describe('fileConcatting', function() {
    // this operation can be slow, so give it some time to process:

    var results;

    before(function(done) {
      console.time('file concatting time');
      // var pyController = startPyTest();

      pyController.on('message', function(message) {
        // message is the message object coming to us from the Python process
        // we are expecting to get back an array of the concatted results
        if(message.type === 'concat.py') {
          // killChildProcess(pyController.childProcess);
          results = message.text;
          console.timeEnd('file concatting time');
          done();
        }  
      });

    });

    it('should delete columns with a dataDescription header of "IGNORE"', function() {
      expect( results[0].length ).to.equal(4);
      expect( results[1].length ).to.equal(4);
      expect( results[3].length ).to.equal(4);
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
