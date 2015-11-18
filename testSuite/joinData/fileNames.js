var path = require('path');

var expect = require('chai').expect;
var mocha = require('mocha');
var sinon = require('sinon');

var startPyTest = require('.././startPyTest');
var df = require('../../index.js');

var testFolder = path.dirname(__filename);

module.exports = function() {

  // 1. it should invoke a passed-in callback function when training is finished
    // require index.js
    // pass in args object and a callback function
    // that callback function will already have a spy installed
    // wait for a finishedFormatting message, then wait an extra second, and expect the callback to have been called
  // 2. it should invoke the callback with the fileNames obj
    // similar to above
  // 3. the fileNames obj should have these properties
    // X_train, etc. 

  describe('fileNames', function(done) {


    var spy; //intentionally putting this into a broad scope so that all tests below can reference it.

    before(function(done) {
      console.time('callback invocation time');
  
      function spyFunc() {
        console.timeEnd('callback invocation time');
      };

      spy = sinon.spy( spyFunc );

      var dfArgs = {
        outputFolder: path.join( testFolder, 'formattedResults'),
        trainingData: path.join( testFolder, 'train.csv'),
        testingData: path.join( testFolder, 'test.csv'),
        verbose: 0,
        test: true
      };

      df( dfArgs, spy );

      process.on('finishedFormatting', function() {
        done();
      });
    });

    it('should invoke the callback function', function() {
      expect(spy).to.have.been.called;
    });

    it('should invoke the callback function with the fileNames obj', function() {
      // var expectedPropertiesWithBrainJS = ['X_train','X_test','y_train','id_train','id_test','X_train_nn','X_test_nn','brainJS_train','brainJS_test', 'trainingDataLength'];
      var expectedProperties = ['X_train','X_test','y_train','id_train','id_test','X_train_nn','X_test_nn', 'trainingDataLength','problemType'];
      function checkProps() {
        for( var i = 0; i < expectedProperties.length; i++) {
          var propName = expectedProperties[i];
          // spy.args[0][0] is the first argument passed to the first invocation of the spied-upon function
            // more simply, it's the fileNames obj we want :)
          if( spy.args[0][0][ propName ] === undefined ) {
            console.log('propName that does not exist is:', propName);
            console.log('spy.args:',spy.args[0][0]);
            return false;
          }
        }
        return true;
      }
      expect(checkProps()).to.be.true;
    });

  });
  
};
