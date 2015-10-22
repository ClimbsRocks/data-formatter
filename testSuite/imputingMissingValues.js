var expect = require('chai').expect;
var mocha = require('mocha');
var startPyTest = require('./startPyTest');
var killChildProcess = require('./killChildProcess');

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
          sumObj[k] += matrix[j][k];
        }
      }
      for( var colIndex in sumObj ) {
        columnSums.push( sumObj[colIndex] );
      }
    };

    before(function(done) {
      console.time('imputing missing values time');
      var pyController = startPyTest();


      pyController.on('message', function(message) {
        if(message.type === 'imputingMissingValues.py') {
          killChildProcess(pyController.childProcess);
          results = message.text;
          sumColumns( results[0] );
          console.timeEnd('imputing missing values time');
          done();
        }
      });
    });


    // should keep track of the total number of missing data points for each row
    it('should keep track of the total number of missing data points for each row', function() {
      expectedSum = 49834 + 6550;
      expect( columnSums ).to.contain(expectedSum);
      // TODO: sum up columns
    });

    // should keep track of each row that had a missing data point for that row
    it('should create a boolean flag for rows that had missing data for a particular column', function() {
      // TODO: sum up columns
      var expectedSums = [49834, 6550];
      expect( columnSums ).to.contain(expectedSum[0]);
      expect( columnSums ).to.contain(expectedSum[1]);
    });

  

  // should leave one copy of the original data untouched, with np.nan values for the missing values
    it('should leave one copy of the original data untouched', function() {
      var expectedSums = [1360220735, 186653];
      expect( columnSums ).to.contain(expectedSum[0]);
      expect( columnSums ).to.contain(expectedSum[1]);
      // TODO: sum up columns
    });

  // should create two new columns for every column with missing values
    it('should create two new columns for each column with missing values in it, and one summary column for total missing values', function() {
      // previously computed correct result
      expect( results[0][0].length ).to.equal(15);
    });

    var emptyEquivalents = ["na","n/a","none","","undefined","missing","blank","empty", undefined, NaN];

    it('should not change the length or width of the matrix', function(done) {

      expect(results[0].length).to.equal(251503)
      expect(results[0][0].length).to.equal(10)
      done();
    });

    // // should impute missing values on the other copy
    // it('should insert a value for all completely blank values', function(done) {
    //   // check every single value in the returned array to make sure it does not include any of the values listed above
    //   function checkAllCorrectRanges (arr) {
    //     // iterates through array
    //     for (var i = 0; i < arr.length; i++) {
    //       // iterates through each row. does not check ID or Output columns
    //       // TODO: don't check the untouched columns
    //       for (var j = 0; j < arr[i].length; j++) {
    //         if( emptyEquivalents.indexOf( arr[i][j] ) !== -1 ) {
    //           console.log(arr[i]);
    //           return false;
    //         }
    //       }
    //     }
    //     return true;
    //   }

    //   expect(checkAllCorrectRanges(results[0])).to.be.true;
    //   done();
    // });



    it('should insert the median value of the column for missing continuous values', function(done) {
      // var sumOfMonthlyIncomeColumn = 0;

      // // TODO: calculate sum of all columns
      //   // compare against expected results with imputing
      // for (var i = 0; i < results[0].length; i++) {
      //   sumOfMonthlyIncomeColumn += parseFloat( results[0][i][4], 10) ;
      // }

      // previously computed value
      // right now the answer matches exactly, but i want to leave some wiggle room if we adjust our methodology at all. 

      expect(columnSums).to.contain(1629324335)
      // expect(sumOfMonthlyIncomeColumn).to.be.within(1629324335 * .98, 1629324335 * 1.02);
      done();
    });



    it('should insert the most-commonly-appearing value of the column for missing categorical values', function(done) {
      // var countNumDependentsIsZero = 0;

      // // TODO: simply check sums again
      // for (var i = 0; i < results[0].length; i++) {
      //   if(results[0][i][9] === '0') {
      //     countNumDependentsIsZero++;
      //   }
      // }
      // // previously computed value
      // expect(countNumDependentsIsZero).to.equal(152070)
      expect(columnSums).to.contain(152070)
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

    after(function() {
      results = [];
    });

  });
  
};
