var expect = require('chai').expect;
var mocha = require('mocha');
var startPyTest = require('./startPyTest');
var killChildProcess = require('./killChildProcess');

module.exports = function() {
  describe('Feature Selection', function() {
    // 100 minutes
    this.timeout(6000000);

    var allData = [];

    before(function(done) {
      var pyController = startPyTest();

      pyController.on('message', function(message) {

        if(message.type === 'featureSelecting.py') {
          for (var i = 0; i < message.text.length; i++) {
            allData.push(message.text[i]);
          }
          if (allData.length > 250000) {
            killChildProcess(pyController.childProcess);
            done();
          }
        }
      });
    });

    // it should apply to both our training and testing data separately
      // expect all columns to have the same length
    it('should be applied to both our training and test data sets', function(done) {
      var expectedLength = allData[0].length;
      console.log('the length of each row after feature selection is:',expectedLength);
      
      function checkAllRows(matrix) {
        for (var i = 0; i < matrix.length; i++) {
          if ( matrix[i].length !== expectedLength ) {
            return false;
          }
        }
        return true;
      }

      expect(checkAllRows(allData)).to.be.true;
      done();
      
    });


    // it should have fewer columns than before
    it('should should have fewer columns than before feature selection, but the same number of observations', function(done) {
      expect(allData.length).to.equal(251503);
      expect(allData[0]).to.have.length.below(100);
      done();
    });

    it('should include columns that we know to be important', function(done) {

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
    });

  after(function() {
    allData = [];
  });

  });
};
