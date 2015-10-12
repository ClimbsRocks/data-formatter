var expect = require('chai').expect;
var mocha = require('mocha');
var startPyController = require('./startPyController');

module.exports = function() {

  describe('imputing missing values', function() {
    var emptyEquivalents = ["na","n/a","none","","undefined","missing","blank","empty", undefined, NaN]

    it('should not change the length or width of the matrix', function(done) {
      var pyController = startPyController();

      pyController.on('message', function(message) {
        if(message.type === 'imputingMissingValues.py') {
          pyController.childProcess.kill();

          expect(message.text.length).to.equal(251503)
          expect(message.text[0].length).to.equal(12)
          done();
        }
      
      });
    });

    it('should insert a value for all completely blank values', function(done) {
      var pyController = startPyController();

      pyController.on('message', function(message) {
        if(message.type === 'imputingMissingValues.py') {
          pyController.childProcess.kill();

          // check every single value in the returned array to make sure it does not include any of the values listed above
          function checkAllCorrectRanges (arr) {
            // iterates through array
            for (var i = 0; i < arr.length; i++) {
              // iterates through each row. does not check ID or Output columns
              for (var j = 2; j < arr[i].length; j++) {
                if( emptyEquivalents.indexOf( arr[i][j] ) !== -1 ) {
                  return false;
                }
              }
            }
            return true;
          }

          expect(checkAllCorrectRanges(message.text)).to.be.true;
          done();
        }
      
      });
    });



    it('should insert the median value of the column for missing values', function(done) {
      var pyController = startPyController();

      pyController.on('message', function(message) {
        if(message.type === 'imputingMissingValues.py') {
          pyController.childProcess.kill();
          var sumOfMonthlyIncomeColumn = 0;


          for (var i = 0; i < message.text.length; i++) {
            sumOfMonthlyIncomeColumn += parseFloat( message.text[i][6], 10) ;
          }

          // previously computed value
          console.log(sumOfMonthlyIncomeColumn);
          // right now the answer matches exactly, but i want to leave some wiggle room if we adjust our methodology at all. 
          expect(sumOfMonthlyIncomeColumn).to.be.within(1629324335 * .98, 1629324335 * 1.02);
          done();
        }
      
      });
    });


    it('should not modify the ID or Output columns at all', function(done) {
      var pyController = startPyController();

      pyController.on('message', function(message) {
        if(message.type === 'imputingMissingValues.py') {
          pyController.childProcess.kill();
          var sumOfIdColumn = 0;
          var sumOfOutputColumn = 0;

          // check every single value in the returned array to make sure it does not include any of the values listed above
          function checkAllCorrectRanges (arr) {

            for (var i = 0; i < arr.length; i++) {
              var outputNum = parseFloat( arr[i][1], 10) ;
              // makes sure we have not calculated any values for our Output column for the prediction set
              if(i >= 150000) {
                outputNum = 0;
                // lazily hardcoding in the value 1 for the output column here. can generalize later. 
                if( arr[i][1] !== "") {
                  return false;
                }
                
              }
              sumOfIdColumn+= parseFloat( arr[i][0], 10 );
              sumOfOutputColumn += outputNum;
            }
            return true;
          }

          expect(checkAllCorrectRanges(message.text)).to.be.true;

          // previously computed values
          expect(sumOfIdColumn).to.equal(16401555256);
          expect(sumOfOutputColumn).to.equal(10026);
          done();
        }
      
      });
    });


  });
  
};
