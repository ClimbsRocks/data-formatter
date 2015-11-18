var expect = require('chai').expect;
var mocha = require('mocha');
var startPyTest = require('../startPyTest');
var joiningData = require('./joiningData');
var fileNames = require('./fileNames');

// this block will contain all the tests for the entire data-formatter package
describe('joining external data into our training and testing files', function() {

  global.pyControllerRossman = startPyTest('rossman');

  // // this timeout should be long enough to handle tests on a variety of machines
  this.timeout(360000);

  joiningData();


  // fileNames();

});
