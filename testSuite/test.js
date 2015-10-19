var expect = require('chai').expect;
var mocha = require('mocha');
var startPyTest = require('./startPyTest');
var fileConcatting = require('./fileConcatting');
var imputingMissingValues = require('./imputingMissingValues');
var dictVectorizing = require('./dictVectorizing');
var featureSelecting = require('./featureSelecting');
var brainjsTest = require('./brainjsTest');
var fileNames = require('./fileNames');
var neuralNetwork = require('./neuralNetwork');

// this block will contain all the tests for the entire data-formatter package
describe('data-formatter', function() {
  // this timeout should be long enough to handle tests on a variety of machines
  this.timeout(240000);

  fileNames();
    
  fileConcatting();

  imputingMissingValues();

  dictVectorizing();

  featureSelecting();   

  neuralNetwork(); 
  
  // brainjsTest();

  // make it work from the command line and from module.exports

});
