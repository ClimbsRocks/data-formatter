var expect = require('chai').expect;
var mocha = require('mocha');
var startPyController = require('./startPyController');
var killChildProcess = require('./killChildProcess');

module.exports = function() {
  describe('min-max-normalizing', function() {

    this.timeout(20000);
    it('should return only values between 0 and 1', function(done) {
      var pyController = startPyController();

      pyController.on('message', function(message) {
        if(message.type === 'minMax.py') {
          killChildProcess(pyController.childProcess);

          // check each number in each row of the array to make sure it is between 0 and 1, inclusive
          function checkAllCorrectRanges (arr) {
            for (var i = 0; i < arr.length; i++) {
              for (var j = 2; j < arr[i].length; j++) {
                if(arr[i][j] < 0 || arr[i][j] > 1) {
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


    it('should not modify the ID or Output columns at all', function(done) {
      var pyController = startPyController();

      pyController.on('message', function(message) {
        if(message.type === 'imputingMissingValues.py') {
          killChildProcess(pyController.childProcess);
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


    // as long as we are using scikit-learn's MinMaxScaler, this is built in. 
    // if we ever use another method of min-max scaling, we will need to fix up and include this unfinished test. 
    // it('should min-max normalize each column individually', function(done) {
    //   var pyController = startPyController();

    //   pyController.on('message', function(message) {
    //     if(message.type === 'minMax.py') {
    //       function checkOneCorrectColumn (arr) {
    //         var min = -Infinity;
    //         var max = Infinity;
    //         for (var i = 0; i < arr.length; i++) {

    //           // check the value is not outside the range of 0,1
    //           if(arr[i] < 0 || arr[i] > 1) {
    //             return false;
    //           }

    //           // keep track of min and max values seen
    //           if (arr[i] < min) {
    //             min = arr[i];
    //           }
    //           if (arr[i] > max) {
    //             max = arr[i];
    //           }
    //         }

    //         // make sure each column is min-max-normalized individually. that means each column should have it's own 0 and 1 values (allowing for some potential rounding inconsistencies)
    //         return min < 0.01 && max > 0.99;
    //       }

    //       var transposedArray = message.text.map(function(col, i) { 
    //         return message.text.map(function(row) { 
    //           return row[i] 
    //         });
    //       });

    //       // ignore the first two columns, as they are ID and Output
    //       transposedArray.unshift();
    //       transposedArray.unshift();


    //       // TODO: split the data out into columns
    //       function checkAllCorrectRanges(arr) {
    //         for (var i = 0; i < arr.length; i++) {
    //           if (!checkOneCorrectColumn(arr[i]) ) {
    //             return false;
    //           }
    //         }
    //         return true;
    //       }

    //       expect(checkAllCorrectRanges(transposedArray)).to.be.true;
    //       done();
    //     }
      
    //   });
    // });


  });
  
};
