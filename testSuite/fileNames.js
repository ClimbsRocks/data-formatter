var expect = require('chai').expect;
var mocha = require('mocha');
var sinon = require('sinon');
var startPyTest = require('./startPyTest');
var killChildProcess = require('./killChildProcess');
var df = require('../index.js');

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

  describe('fileNames', function() {

    var spy = sinon.spy();

    before(function(done) {
      console.time('callback invocation time');
      var dfArgs = {
        outputFolder: path.join( testFolder, 'formattedResults'),
        trainingData: path.join(testFolder, 'trainKaggleGiveMeSomeCredit.csv'),
        testingData: path.join(testFolder, 'testKaggleGiveMeSomeCredit.csv'),
        test: true
      };

      df( dfArgs, spy );
      console.timeEnd('callback invocation time');
    });

    it('should invoke the callback function', function(done) {
      expect(spy).to.have.been.called;
    });

    it('should invoke the callback function with the fileNames obj', function(done) {
      var expectedProperties = ['X_train','X_test','y_train','id_train','id_test'];
      function checkProps() {
        for( var i = 0; i < expectedProperties.length; i++) {
          var propName = expectedProperties[i];
          if( spy.args[ propName ] === undefined ) {
            return false;
          }
        }
        return true;
      }
      expect(checkProps()).to.be.true;
    });

  });
  
};
