var expect = require('chai').expect;
var mocha = require('mocha');

module.exports = function() {
  describe('brain.js formatting', function() {

    var results;

    before(function(done) {
      console.time('brainjs time');

      pyController.on('message', function(message) {
        if(message.type === 'brainjs.py') {
          results = message.text;
          console.timeEnd('brainjs time');
          done();
        } 
      });
    });

    it('should have id, input, and output properties', function() {
      function checkProperties(arr) {
        for( var i = 0; i < results.length; i++) {
          if( results[i].id === undefined || results[i].input === undefined || results[i].output === undefined) {
            console.log('i', i, 'results[i]', results[i] );
            return false;
          }
        }
        return true;
      }

      expect( checkProperties(results) ).to.be.true;
    });

    it('input and output should be arrays', function() {
      function checkPropertyTypes(arr) {
        for( var i = 0; i < results.length; i++) {
          if( !Array.isArray( results[i].input ) || !Array.isArray( results[i].output ) ) {
            console.log('i', i, 'results[i]', results[i] );
            console.log('Array.isArray(results[i].input)')
            console.log(Array.isArray(results[i].input))
            console.log('Array.isArray(results[i].output)')
            console.log(Array.isArray(results[i].output))
            return false;
          }
        }
        return true;
      }

      expect( checkPropertyTypes(results) ).to.be.true;
    });

    it('should have input array length equal to number chosen in featureSelection', function() {
      function checkInputLength(arr) {
        for( var i = 0; i < results.length; i++) {
          if( results[i].input.length !== expectedInputLength ) {
            console.log(results[i].input.length);
            console.log(expectedInputLength);
            console.log('i', i, 'results[i]', results[i] );
            return false;
          }
        }
        return true;
      }

      expect( checkInputLength(results) ).to.be.true;
    });


    it('should return only input values between 0 and 1', function() {
      // check each number in each row of the array to make sure it is between 0 and 1, inclusive
      function checkAllCorrectRanges (arr) {
        for (var i = 0; i < arr.length; i++) {
          for (var j = 0; j < arr[i].input.length; j++) {
            if( arr[i].input[j] < 0 || arr[i].input[j] > 1 ) {
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
      for( var i = 0; i < results.length; i++) {
        results[i] = null;
      }
      results = null;
    });

  });
  
};
