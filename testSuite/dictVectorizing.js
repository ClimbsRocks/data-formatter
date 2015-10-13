var expect = require('chai').expect;
var mocha = require('mocha');
var startPyController = require('./startPyController');
var killChildProcess = require('./killChildProcess');

module.exports = function() {
  describe('dictVectorizing', function() {

    // it should leave continuous columns alone
      // it should have a column that sums up to what one of the continuous columns sums up to now
    // it should have a column that sums up to the countif of a categorical column's 1 value
    // there should be at least X many columns
    // should be performed on the entire dataset at once to ensure consistency


    // Complete.
    // actually, at this point, do we want to consider taking out ID and Output? 
    // we will need them to be their own vectors for the RFECV anyways
    // and it would let us clean up the code inside imputing a bit.
    // we could still have the user send it over inside other properties on message, such as ID and Output, just to continue to check they're not being modified. 
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

    // WIP
    it('should return only values of 0 and 1 for categorical columns', function(done) {
      var pyController = startPyController();

      pyController.on('message', function(message) {
        if(message.type === 'concat.py') {
          dataDescription = message.text[0];
        }


        if(message.type === 'minMax.py') {
          killChildProcess(pyController.childProcess);

          // check each number in each row of the array to make sure it is between 0 and 1, inclusive
          function checkAllCorrectRanges (arr) {
            for (var i = 0; i < arr.length; i++) {
              for (var j = 2; j < arr[i].length; j++) {
                // TODO: this will not work, since we will now have many more columns than we initially had in the input dataset
                if(dataDescription[j] === 'categorical' && (arr[i][j] < 0 || arr[i][j] > 1) ) {
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

    // Complete
    it('should include continuous columns unmodified', function(done) {
      var pyController = startPyController();

      pyController.on('message', function(message) {
        if(message.type === 'concat.py') {
          dataDescription = message.text[0];
        }


        if(message.type === 'minMax.py') {
          killChildProcess(pyController.childProcess);
          var sumOfColumns = {};
          for (var i = 0; i < message.text[0].length; i++) {
            sumOfColumns[i] = 0;
          }


          // check each number in each row of the array to make sure it is between 0 and 1, inclusive
          function checkAllCorrectRanges (arr) {
            for (var i = 0; i < arr.length; i++) {
              for (var j = 0; j < arr[i].length; j++) {
                sumOfColumns[j] = arr[i][j];
              }
            }
          }
          checkAllCorrectRanges(message.text);

          // these are known sums of the combined dataset's continuous columns
          expect(sumOfColumns).to.contain(13163590);
          expect(sumOfColumns).to.contain(1360220735);
          expect(sumOfColumns).to.contain(1446246.668);
          expect(sumOfColumns).to.contain(87916009.34);
          done();
        }
      
      });
    });




  });
  
};
