var expect = require('chai').expect;
var mocha = require('mocha');
var startPyTest = require('./startPyTest');
var killChildProcess = require('./killChildProcess');

module.exports = function() {
  describe('Feature Selection', function() {
    // 100 minutes
    this.timeout(6000000);

    // it should apply to both our training and testing data separately
      // expect all columns to have the same length
    it('should be applied to both our training and test data sets', function(done) {
      var pyController = startPyTest();

      var allData = [];
      pyController.on('message', function(message) {

        if(message.type === 'featureSelecting.py') {
          for (var i = 0; i < message.text.length; i++) {
            allData.push(message.text[i]);
          }
          if (allData.length > 250000) {
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
          }
        }
      
      });
    });


    // it should have fewer columns than before
    it('should should have fewer columns than before feature selection, but the same number of observations', function(done) {
      var pyController = startPyTest();

      var allData = [];
      pyController.on('message', function(message) {

        if(message.type === 'featureSelecting.py') {
          for (var i = 0; i < message.text.length; i++) {
            allData.push(message.text[i]);
          }

          if (allData.length > 250000) {
            console.log('length of row after first feature selection:',allData[0].length);
            expect(allData.length).to.equal(251503);
            expect(allData[0]).to.have.length.below(158);
            done();
          }
        }
      
      });
    });


    // it should keep some feature that we know to be important
    // it should eliminate some feature that we know to be unimportant
      // we could even consider adding in some noisy data to ensure it gets deleted
        // but then we'd have to possibly modify previous tests


  });
};
