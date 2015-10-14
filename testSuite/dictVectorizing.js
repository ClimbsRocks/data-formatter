var expect = require('chai').expect;
var mocha = require('mocha');
var startPyController = require('./startPyController');
var killChildProcess = require('./killChildProcess');

module.exports = function() {
  describe('dictVectorizing', function() {
    this.timeout(600000);

    it('should be performed on the combined training and testing dataset at the same time to ensure consistency', function(done) {
      // individual row length
      // count of columns with only 0's and 1's
      var pyController = startPyController();

      var allData = [];
      pyController.on('message', function(message) {

        if(message.type === 'dictVectorizing.py') {
          for (var i = 0; i < message.text.length; i++) {
            allData.push(message.text[i]);
          }

          if (allData.length > 250000) {
            expect(allData.length).to.equal(251503);
            done();
          }
        }
      
      });
    });

    // Complete.
    // actually, at this point, do we want to consider taking out ID and Output? 
    // we will need them to be their own vectors for the RFECV anyways
    // and it would let us clean up the code inside imputing a bit.
    // we could still have the user send it over inside other properties on message, such as ID and Output, just to continue to check they're not being modified. 
    // it('should not modify the ID or Output columns at all', function(done) {
    //   var pyController = startPyController();

    //   var allData = [];
    //   var
    //   pyController.on('message', function(message) {
    //     if(message.type === 'dictVectorizing.py') {
    //       allData.push(message.text);

    //       if ( allData.length > 250000 ) {
    //         killChildProcess(pyController.childProcess);
              
    //        var sumOfIdColumn = message.text[1].reduce(function(acc, current) {
    //          return acc + parseFloat( current, 10);
    //        }, 0);

    //        var sumOfOutputColumn = message.text[2].slice(0,150000).reduce(function(acc, current) {
    //          return acc + parseFloat( current, 10) ;
    //        }, 0);

    //        var allOutputValuesBlank= message.text[2].slice(150000).reduce(function(acc, current) {
    //          return acc && current === "";
    //        }, true);


    //        expect(allOutputValuesBlank).to.be.true;

    //        // previously computed values
    //        expect(sumOfIdColumn).to.equal(16401555256);
    //        expect(sumOfOutputColumn).to.equal(10026);
    //        done();

    //       }
    //     }
      
    //   });
    // });


    it('should binarize all categorical values using one-hot encoding', function(done) {
      // individual row length
      // count of columns with only 0's and 1's
      var pyController = startPyController();

      var allData = [];
      pyController.on('message', function(message) {
        if(message.type === 'dictVectorizing.py') {
          for (var i = 0; i < message.text.length; i++) {
            allData.push(message.text[i]);
          }
          if (allData.length > 250000) {
            var binarySummary = {};
            for (var i = 0; i < allData[0].length; i++) {
              binarySummary[i] = true;
            }
            function checkForBinaries(arr) {
              for (var i = 0; i < arr.length; i++) {
                for (var j = 0; j < arr[i].length; j++) {
                  if(arr[i][j] !== 0 && arr[i][j] !== 1) {
                    binarySummary[j] = false;
                  }
                }
              }
            }

            checkForBinaries(allData);

            var countOfBinaryColumns = 0;
            for (var colIndex in binarySummary) {
              if(binarySummary[colIndex] === true) {
                countOfBinaryColumns++;
              }
            }
            // these are known sums of the combined dataset's continuous columns
            // expect(message.text[0].length).to.equal(158);
            expect(countOfBinaryColumns).to.equal(154);
            done();
          }

        }
      
      });
    });

    // // Complete
    it('should include continuous columns unmodified', function(done) {
      var pyController = startPyController();

      var allData = [];
      pyController.on('message', function(message) {

        if(message.type === 'dictVectorizing.py') {
          for (var i = 0; i < message.text.length; i++) {
            allData.push(message.text[i]);
          }
          // allData.concat(JSON.parse(message.text));

          if ( allData.length > 250000 ) {
            killChildProcess(pyController.childProcess);

            // set up sumOfColumns so we don't deal with undefined values later on
            var sumOfColumns = {};
            for (var i = 0; i < allData[0].length; i++) {
              sumOfColumns[i] = 0;
            }

            function sumAllColumns (arr) {
              for (var i = 0; i < arr.length; i++) {
                for (var j = 0; j < arr[i].length; j++) {
                  sumOfColumns[j] += arr[i][j];
                }
              }
            }

            sumAllColumns(allData);

            var sums = [];
            for (var columnIndex in sumOfColumns) {
              // rounding to avoid differences in handling floating point numbers
              sums.push( Math.round(sumOfColumns[ columnIndex ]) );
            }

            // these are known sums of the combined dataset's continuous columns
            expect(sums).to.contain( 13163590 );
            expect(sums).to.contain( 1629324335 );
            expect(sums).to.contain( Math.round(1446246.668) );
            expect(sums).to.contain( Math.round(87916009.34) );
            done();
          }
        }
      
      });
    });


  });
  
};
