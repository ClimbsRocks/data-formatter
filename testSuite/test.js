var expect = require('chai').expect;
var mocha = require('mocha');
var startPyController = require('./startPyController');
var minMaxScaling = require('./minMaxScaling');
var fileConcatting = require('./fileConcatting');
var imputingMissingValues = require('./imputingMissingValues');

// this block will contain all the tests for the entire data-formatter package
describe('data-formatter', function() {
  this.timeout(20000);

  fileConcatting();

  imputingMissingValues();

  // dictVectorizer

  // rfecv (feature selection)

  minMaxScaling();

  // dictVectorizer for categorical data
  
  // write results to file

  // make it work from the command line and from module.exports



});
