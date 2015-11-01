var expect = require('chai').expect;
var mocha = require('mocha');
var startPyTest = require('./startPyTest');
var killChildProcess = require('./killChildProcess');

module.exports = function() {

  describe('sumByID', function() {
    before(function(done) {
      console.time('sumByID time');
      // var pyController = startPyTest();


      pyController.on('message', function(message) {
        if(message.type === 'sumById.py') {
          // killChildProcess(pyController.childProcess);
          results = message.text;
          sumColumns( results[0] );
          console.timeEnd('sumByID time');
          done();
        }
      });
    });

    it('should not change datasets where IDs are only present in one row', function() {

    });

    it('should turn each ID into a single row of data', function() {
      var idSummaryObj = {};
      var idIndex = headerRow.indexOf('id');

      function summarizeIDColumn() {
        for (var i = 0; i < results.length; i++) {
          var id = results[i][idIndex];
          if( idSummaryObj[id] !== undefined) {
            return false;
          } else {
            idSummaryObj[id] = 1;
          }
        }
        return true;
      }

    });



    it('should return a list of dictionaries', function() {

    });

    it('should have columns for each category', function() {
      // TODO: simply get the total number of expected columns
        // number of unique categories within each column, summed together
      // this test might be redundant with dictVectorizer, so we might not write it out
    });

    it('should sum up results by id for each category', function() {
      // TODO: get the expected sum of each aggregated column by calculating it manually
        // compare the observed sums to those to make sure it's calculating correctly!
    });


    it('should keep track of which IDs are part of the training set, and which are in the testing set', function() {
      // have a list of known IDs for each and check against them

    });

    it('should return new idColumn and outputColumn lists that match up to the order of X', function() {
      // check some IDs, and test against their known output value
      // also check lengths of these lists
    });

    
  });


};
