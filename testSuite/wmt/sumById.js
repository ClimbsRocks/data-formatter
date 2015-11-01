var expect = require('chai').expect;
var mocha = require('mocha');
var startPyTest = require('./startPyTest');
var killChildProcess = require('./killChildProcess');

module.exports = function() {

  describe('sumByID', function() {
    
    var idColumn;
    var outputColumn;
    var X;
    var trainingLength;

    before(function(done) {

      console.time('sumByID time');
      pyController.on('message', function(message) {
        if(message.type === 'sumById.py') {

          idColumn = message.text[1];
          trainingLength = message.text[2];
          outputColumn = message.text[3];
          X = message.text[0];

          console.timeEnd('sumByID time');
          done();
        }
      });
    });

    it('should turn each ID into a single row of data', function() {
      var idSummaryObj = {};
      var idIndex = headerRow.indexOf('id');

      function summarizeIDColumn() {
        for (var i = 0; i < idColumn.length; i++) {
          var id = idColumn[i];
          if( idSummaryObj[id] !== undefined) {
            return false;
          } else {
            idSummaryObj[id] = 1;
          }
        }
        return true;
      }

      expect( summarizeIDColumn( idColumn) ).to.be.true;

    });

    it('should not have id or output column in the rowObj itself, only in their own separate columns', function() {
      function checkForIDAndOutput(results) {
        for( var i = 0; i < results.length; i++) {
          var rowObj = results[i];
          for( var key in rowObj ) {
            if( key === 'id' || key === 'output') {
              return false;
            }
          }
        }
        return true;
      };

      expect( checkForIDAndOutput(results) ).to.be.true;
    });



    it('should return a list of dictionaries', function() {
      function checkForObjects(results) {
        for( var i = 0; i < results.length; i++) {
          if( results[i].prototype.constructor !== Object) {
            return false;
          }
        }
        return true;
      }

      expect( checkForObjects(results) ).to.be.true;

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
