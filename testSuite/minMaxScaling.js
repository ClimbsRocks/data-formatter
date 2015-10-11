var expect = require('chai').expect;
var mocha = require('mocha');
var startPyController = require('./startPyController');

module.exports = function() {
  describe('min-max-normalizing', function() {
    this.timeout(5000);

    it('should return only values between 0 and 1', function(done) {
      var pyController = startPyController();

      pyController.on('message', function(message) {
        if(message.type === 'minMax.py') {

          // check each number in each row of the array to make sure it is between 0 and 1, inclusive
          function checkAllCorrectRanges (arr) {
            for (var i = 0; i < arr.length; i++) {
              for (var j = 0; j < arr[i].length; j++) {
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

    it('should min-max normalize each column individually', function(done) {
      var pyController = startPyController();

      pyController.on('message', function(message) {
        if(message.type === 'minMax.py') {
          function checkOneCorrectColumn (arr) {
            var min = -Infinity;
            var max = Infinity;
            for (var i = 0; i < arr.length; i++) {

              // check the value is not outside the range of 0,1
              if(arr[i] < 0 || arr[i] > 1) {
                return false;
              }

              // keep track of min and max values seen
              if (arr[i] < min) {
                min = arr[i];
              }
              if (arr[i] > max) {
                max = arr[i];
              }
            }

            // make sure each column is min-max-normalized individually. that means each column should have it's own 0 and 1 values (allowing for some potential rounding inconsistencies)
            return min < 0.01 && max > 0.99;
          }

          // TODO: split the data out into columns
          function checkAllCorrectRanges(arr) {
            for (var i = 0; i < arr.length; i++) {
              if (!checkOneCorrectColumn(arr[i]) ) {
                return false;
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
