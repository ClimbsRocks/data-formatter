var expect = require('chai').expect;
var mocha = require('mocha');
var startPyTest = require('./startPyTest');
var minMaxScaling = require('./minMaxScaling');
var fileConcatting = require('./fileConcatting');
var imputingMissingValues = require('./imputingMissingValues');
var dictVectorizing = require('./dictVectorizing');
var featureSelecting = require('./featureSelecting');

// this block will contain all the tests for the entire data-formatter package
describe('data-formatter', function() {
  this.timeout(60000);

  // fileConcatting();

  // imputingMissingValues();

  // dictVectorizing();

  featureSelecting();


  // rfecv (feature selection)
    // might have to do this on the titanic dataset if give me some credit doesn't cooperate. 
    // should have fewer columns than before! but still have a reasonable range of columns. so maybe something like within(.75 * prevColumnCount, .85*prevColumnCount). i'm guessing our current features will be mostly useful, so we will probably not see a dramatic reduction. 
      // for something like the titanic dataset though, we'd probably see a HUGE reduction if we passed in all the raw data. 
      

  // minMaxScaling();

  // dictVectorizer for categorical data
  
  // write results to file

  // make it work from the command line and from module.exports



});
