var expect = require('chai').expect;
var mocha = require('mocha');
var startPyController = require('./startPyController');

// this block will contain all the tests for the entire data-formatter package
describe('data-formatter', function() {

  // this describe block will contain all the tests for our fileConcatting module
  describe('fileConcatting', function() {

    // if we write the results to disk, mae sure to erase them so we are starting from fresh results
    // before(function() {
    //   fs.unlinkSync(path.join(testFolder,'concattedtrainKaggleGiveMeSomeCredit.csv'));
    // });

    // this it statement describes the test. this is maybe analogous to the prompt of the question if thinking back to a university exam. 
    // by defining done as a parameter for the callback function here, we are saying this test be an asynchronous function. 
    // mocha will allow this test to run up until we invoke done(), or until the test times out.
    it('should concatenate the test data and the training data together into one large data set', function(done) {
      var pyController = startPyController();

      pyController.on('message', function(message) {
        // message is the message object coming to us from the Python process
        // we are expecting to get back an array of the concatted results
        if(message.type === 'concat.py') {
          // 1 header row in training data
          // 150,000 data rows in training data
          // 101,503 data rows in testing data
          expect(message.text[1].length).to.equal(251504);
          done();
        }
      
      });
    });

    it('should communicate back the number of rows in the training dataset, including the header row', function(done) {
      var pyController = startPyController();

      pyController.on('message', function(message) {
        // the first item in the array returned to us should be the length of the training data
        if(message.type === 'concat.py') {
          expect(message.text[0]).to.equal(150001);
          done();
        }
      
      });
    });

  });

  describe('min-max-normalizing', function() {

    it('should return only values between 0 and 1', function(done) {
      var pyController = startPyController();

      pyController.on('message', function(message) {
        if(message.type === 'normalization.py') {

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

          expect(checkAllCorrectRanges(message.text)).to.be(true);
          done();
        }
      
      });
    });

    it('should min-max normalize each column individually', function(done) {
      var pyController = startPyController();

      pyController.on('message', function(message) {
        if(message.type === 'normalization.py') {
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

          expect(checkAllCorrectRanges(message.text)).to.be(true);
          done();
        }
      
      });
    });


  });




});
