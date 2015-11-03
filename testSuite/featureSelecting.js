var expect = require('chai').expect;
var mocha = require('mocha');

module.exports = function() {
  describe('Feature Selection', function() {

    var allData = [];

    before(function(done) {
      console.time('feature selecting time');

      pyController.on('message', function(message) {

        if(message.type === 'featureSelecting.py') {
          // for our neural net check later on.
          global.expectedInputLength = message.text[0].length;
          for (var i = 0; i < message.text.length; i++) {
            allData.push(message.text[i]);
          }
          message.text = null;
          if (allData.length > 250000) {
            console.timeEnd('feature selecting time');
            done();
          }
        } 
      });
    });

    it('should be applied to both our training and test data sets', function(done) {
      var expectedLength = allData[0].length;
      console.log('the length of each row after feature selection is:',expectedLength);
      
      // expect all columns to have the same length
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


    it('should should have fewer columns than before feature selection, but the same number of observations', function(done) {
      expect(allData.length).to.equal(251503);
      // it is fairly consistently picking 66-68 features, but I want to leave a bit of room for adjustment
      expect(allData[0]).to.have.length.within(60,75);
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
