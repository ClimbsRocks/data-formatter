var expect = require('chai').expect;
var mocha = require('mocha');
var startPyTest = require('./startPyTest');
var killChildProcess = require('./killChildProcess');

module.exports = function() {
  describe('neural network formatting', function() {

    var results;

    before(function(done) {
      console.time('Neural Network time');

      pyController.on('message', function(message) {
        if(message.type === 'minMax.py') {
          results = message.text;
          console.timeEnd('Neural Network time');
          done();
        } 
      });
    });


    it('should have an array length equal to number chosen in featureSelection', function() {
      function checkInputLength(arr) {
        for( var i = 0; i < results.length; i++) {
          if( results[i].length !== expectedInputLength ) {
            console.log(results[i].length);
            console.log(expectedInputLength);
            console.log('i', i, 'results[i]', results[i] );
            return false;
          }
        }
        return true;
      }

      expect( checkInputLength(results) ).to.be.true;
    });


    it('should return only input values between -1 and 1', function() {
      // check each number in each row of the array to make sure it is between 0 and 1, inclusive
      function checkAllCorrectRanges (matrix) {
        for (var i = 0; i < matrix.length; i++) {
          for (var j = 0; j < matrix[i].length; j++) {
            if( matrix[i][j] < -1 || matrix[i][j] > 1 ) {
              console.log('i', i, 'results[i]', results[i] );
              return false;
            }
          }
        }
        return true;
      }

      expect( checkAllCorrectRanges( results )).to.be.true;
    });

    // attempt to delete results
    after(function() {
      results = [];
    });

  });
  
};
