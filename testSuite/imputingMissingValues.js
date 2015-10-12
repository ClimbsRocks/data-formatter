var expect = require('chai').expect;
var mocha = require('mocha');
var startPyController = require('./startPyController');

module.exports = function() {
  describe('imputing missing values', function() {

    it('should insert the median value for all completely blank values', function(done) {
      var pyController = startPyController();

      pyController.on('message', function(message) {
        if(message.type === 'imputingMissingValues.py') {
          pyController.childProcess.kill();

          // check each number in each row of the array to make sure it is between 0 and 1, inclusive
          function checkAllCorrectRanges (arr) {
            for (var i = 0; i < arr.length; i++) {
              for (var j = 0; j < arr[i].length; j++) {
                if(arr[i][j] === "") {
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



  });
  
};
