var expect = require('chai').expect;
var mocha = require('mocha');

module.exports = function() {

  // TODO: add in a check for a specific row we know to be correct. 
    // this both checks to make sure things are happening to that row as we expect, and ensures that the ID column is still properly attached, if we perform this lookup by ID, ideally near the end of the dataset. 

  describe('imputing missing values', function() {

    var results;
    var columnSums = [];

    function sumColumns(matrix) {
      var sumObj = {};
      for (var i = 0; i < matrix[0].length; i++) {
        sumObj[i] = 0;
      }
      for( var j = 0; j < matrix.length; j++) {
        for( var k = 0; k < matrix[i].length; k++) {
          var parsedVal = parseInt( matrix[j][k], 10);
          if( !isNaN( parsedVal ) ) {
            sumObj[k] += parsedVal;
          }
        }
      }
      for( var colIndex in sumObj ) {
        columnSums.push( sumObj[colIndex] );
      }
    };

    before(function(done) {
      console.time('imputing missing values time');

      pyController.on('message', function(message) {
        if(message.type === 'imputingMissingValues.py') {
          results = message.text;
          sumColumns( results[0] );
          console.timeEnd('imputing missing values time');
          done();
        }
      });
    });


    it('should keep track of the total number of missing data points for each row', function() {
      expectedSum = 49834 + 6550;
      expect( columnSums ).to.contain(expectedSum);
    });

    it('should create a boolean flag for rows that had missing data for a particular column', function() {
      var expectedSums = [49834, 6550];
      expect( columnSums ).to.contain(expectedSums[0]);
      expect( columnSums ).to.contain(expectedSums[1]);
    });

    it('should leave one copy of the original data untouched', function() {
      var expectedSums = [1360220735];
      expect( columnSums ).to.contain(expectedSums[0]);
    });

    it('should remove unique values from the dataset', function() {
      var expectedSums = [186557];
      expect( columnSums ).to.contain(expectedSums[0]);
    });

    it('should create two new columns for each column with missing values in it, and one summary column for total missing values', function() {
      // previously computed correct result
      expect( results[0][0].length ).to.equal(15);
    });

    it('should not change the length of the matrix', function(done) {
      expect(results[0].length).to.equal(251503)
      done();
    });

    it('should insert the median value of the column for missing continuous values', function(done) {
      // previously computed value
      expect(columnSums).to.contain(1629324335)
      done();
    });

    it('should insert the most-commonly-appearing value of the column for missing categorical values', function(done) {
      var countNumDependentsIsZero = 0;

      for (var i = 0; i < results[0].length; i++) {
        if(results[0][i][11] === '0') {
          countNumDependentsIsZero++;
        }
      }
      // previously computed value
      expect(countNumDependentsIsZero).to.equal(152070)
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

      sumOfIdColumn = null;
      sumOfOutputColumn = null;
      allOutputValuesBlank = null;
      done();
    });

    after(function() {
      results[0] = null;
      results[1] = null;
      results[2] = null;
      results = null;
      columnSums = [];
    });

  });
  
};
