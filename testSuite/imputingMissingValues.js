var expect = require('chai').expect;
var mocha = require('mocha');
var startPyTest = require('./startPyTest');
var killChildProcess = require('./killChildProcess');

module.exports = function() {

  // TODO: add in a check for a specific row we know to be correct. 
    // this both checks to make sure things are happening to that row as we expect, and ensures that the ID column is still properly attached, if we perform this lookup by ID, ideally near the end of the dataset. 

  describe('imputing missing values', function() {
    var emptyEquivalents = ["na","n/a","none","","undefined","missing","blank","empty", undefined, NaN]

    it('should not change the length or width of the matrix', function(done) {
      var pyController = startPyTest();

      pyController.on('message', function(message) {
        if(message.type === 'imputingMissingValues.py') {
          killChildProcess(pyController.childProcess);

          expect(message.text[0].length).to.equal(251503)
          expect(message.text[0][0].length).to.equal(10)
          done();
        }
      
      });
    });

    it('should insert a value for all completely blank values', function(done) {
      var pyController = startPyTest();

      pyController.on('message', function(message) {
        if(message.type === 'imputingMissingValues.py') {
          killChildProcess(pyController.childProcess);

          // check every single value in the returned array to make sure it does not include any of the values listed above
          function checkAllCorrectRanges (arr) {
            // iterates through array
            for (var i = 0; i < arr.length; i++) {
              // iterates through each row. does not check ID or Output columns
              for (var j = 0; j < arr[i].length; j++) {
                if( emptyEquivalents.indexOf( arr[i][j] ) !== -1 ) {
                  console.log(arr[i]);
                  return false;
                }
              }
            }
            return true;
          }

          expect(checkAllCorrectRanges(message.text[0])).to.be.true;
          done();
        }
      
      });
    });



    it('should insert the median value of the column for missing continuous values', function(done) {
      var pyController = startPyTest();

      pyController.on('message', function(message) {
        if(message.type === 'imputingMissingValues.py') {
          killChildProcess(pyController.childProcess);
          var sumOfMonthlyIncomeColumn = 0;


          for (var i = 0; i < message.text[0].length; i++) {
            sumOfMonthlyIncomeColumn += parseFloat( message.text[0][i][4], 10) ;
          }

          // previously computed value
          // right now the answer matches exactly, but i want to leave some wiggle room if we adjust our methodology at all. 
          expect(sumOfMonthlyIncomeColumn).to.be.within(1629324335 * .98, 1629324335 * 1.02);
          done();
        }
      
      });
    });



    it('should insert the most-commonly-appearing value of the column for missing categorical values', function(done) {
      var pyController = startPyTest();

      pyController.on('message', function(message) {
        if(message.type === 'imputingMissingValues.py') {
          killChildProcess(pyController.childProcess);
          var countNumDependentsIsZero = 0;


          for (var i = 0; i < message.text[0].length; i++) {
            if(message.text[0][i][9] === '0') {
              countNumDependentsIsZero++;
            }
          }

          // previously computed value
          // right now the answer matches exactly, but i want to leave some wiggle room if we adjust our methodology at all. 
          expect(countNumDependentsIsZero).to.equal(152070)
          done();
        }
      
      });
    });


    it('should not modify the ID or Output columns at all', function(done) {
      var pyController = startPyTest();

      pyController.on('message', function(message) {
        if(message.type === 'imputingMissingValues.py') {
          killChildProcess(pyController.childProcess);

          var sumOfIdColumn = message.text[1].reduce(function(acc, current) {
            return acc + parseFloat( current, 10);
          }, 0);

          var sumOfOutputColumn = message.text[2].slice(0,150000).reduce(function(acc, current) {
            return acc + parseFloat( current, 10) ;
          }, 0);

          var allOutputValuesBlank= message.text[2].slice(150000).reduce(function(acc, current) {
            return acc && current === "";
          }, true);


          expect(allOutputValuesBlank).to.be.true;

          // previously computed values
          expect(sumOfIdColumn).to.equal(16401555256);
          expect(sumOfOutputColumn).to.equal(10026);
          done();
        }
      
      });
    });


  });
  
};
