
var expect = require('chai').expect;
var mocha = require('mocha');
var startPyTest = require('../startPyTest');
var fileConcatting = require('./fileConcatting');
var sumById = require('./sumById');

// this block will contain all the tests for the entire data-formatter package
describe('datasets with multiple rows for each ID', function() {

  global.pyControllerWmt = startPyTest('wmt');

  // // this timeout should be long enough to handle tests on a variety of machines
  this.timeout(360000);

  fileConcatting();

  sumById();

  // imputingMissingValues();

  // dictVectorizing();

  // featureSelecting();   

  // neuralNetwork(); 
  
  // brainjsTest();

  // fileNames();

});
