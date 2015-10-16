var expect = require('chai').expect;
var mocha = require('mocha');
var startPyTest = require('./startPyTest');
var killChildProcess = require('./killChildProcess');

module.exports = function() {
  describe('min-max-normalizing', function() {

    var results;

    before(function(done) {
      console.time('min max normalizing time');
      var pyController = startPyTest();


      pyController.on('message', function(message) {
        if(message.type === 'minMax.py') {
          killChildProcess(pyController.childProcess);
          results = message.text;
          console.timeEnd('min max normalizing time');
          done();
        }
      });
    });


    it('should return only values between 0 and 1', function(done) {
      // check each number in each row of the array to make sure it is between 0 and 1, inclusive
      function checkAllCorrectRanges (arr) {
        for (var i = 0; i < arr.length; i++) {
          for (var j = 2; j < arr[i].length; j++) {
            if( arr[i][j] < 0 || arr[i][j] > 1 ) {
              return false;
            }
          }
        }
        return true;
      }

      expect( checkAllCorrectRanges( results[0] )).to.be.true;
      done();
    });


    it('should not modify the ID or Output columns at all', function(done) {

      var sumOfIdColumn = results[1].reduce(function(acc, current) {
        return acc + parseFloat( current, 10);
      }, 0);

      var sumOfOutputColumn = results[2].slice(0,150000).reduce(function(acc, current) {
        return acc + parseFloat( current, 10) ;
      }, 0);

      var allOutputValuesBlank= results[2].slice(150000).reduce(function(acc, current) {
        return acc && current === "";
      }, true);


      expect(allOutputValuesBlank).to.be.true;

      // previously computed values
      expect(sumOfIdColumn).to.equal(16401555256);
      expect(sumOfOutputColumn).to.equal(10026);
      done();
    });

    // attempt to delete results
    after(function(done) {
      results = [];
    });

    // if we ever use something other than scikit-learn's MinMaxScaler, we will need to check to make sure each column is normalized individually

  });
  
};
