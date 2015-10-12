var expect = require('chai').expect;
var mocha = require('mocha');
var startPyController = require('./startPyController');
var minMaxScaling = require('./minMaxScaling');
var fileConcatting = require('./fileConcatting');
var imputingMissingValues = require('./imputingMissingValues');

// this block will contain all the tests for the entire data-formatter package
describe('data-formatter', function() {
  this.timeout(10000);

  // fileConcatting();

  imputingMissingValues();

  // minMaxScaling();
  
  // grab the first row above the header separately, to know which column is used for what
  // only normalize numerical columns
  // write results to file



});
