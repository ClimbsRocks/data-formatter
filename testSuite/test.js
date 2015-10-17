var expect = require('chai').expect;
var mocha = require('mocha');
var startPyTest = require('./startPyTest');
var fileConcatting = require('./fileConcatting');
var imputingMissingValues = require('./imputingMissingValues');
var dictVectorizing = require('./dictVectorizing');
var featureSelecting = require('./featureSelecting');
var brainjsTest = require('./brainjsTest');

// this block will contain all the tests for the entire data-formatter package
describe('data-formatter', function() {
  this.timeout(600000);

  fileConcatting();

  imputingMissingValues();

  dictVectorizing();

  featureSelecting();      

  brainjsTest();

  // write results to file

  // make it work from the command line and from module.exports

});
