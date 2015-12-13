#!/usr/bin/env node

(function() {

  var fs = require('fs');
  var path = require('path');
  var mkdirp = require('mkdirp');
  var startPyChild = require('./helperFunctions/startPyChild.js');
  var setDefaultValues = require('./helperFunctions/setDefaultValues.js');

  var cwd = process.cwd();

  module.exports= function( args, callback ) {
    // the following is a way-past-MVP idea that probably makes more sense for users to do themselves. 
    // TODO: allow the user to pass in a flag for "decideCategoricalOrContinuous"
      // do the data formatting process twice:
        // once with the inputs as the user has them laid out
        // and once where we force anything that can be a float into a float, regardless of whether the user classified it as a categorical variable or not. 
      // then go through, train a small ensemble, and see which data set does better

    args = setDefaultValues(args);

    // make sure the output folder exists. if not, create it.
    mkdirp( args.outputFolder, function(err) {
      if(err) {
        console.error(err);
      }
      startPyChild( args, callback );
    });
    
  };

  // allow the module to be invoked from the command line
  // since this is all wrapped in an IIFE, this if statement will execute and check if data-formatter was invoked from another module, or without a parent (from the command line)
  if( !module.parent ) {
    var argsObj = {};
    // if we are being invoked from the command line, output the formatted data into this same directory. 
    argsObj.outputFolder = path.join( cwd, 'data-formatterResults');
    argsObj.trainingData = process.argv[2];
    argsObj.testingData = process.argv[3];
    argsObj.verbose = process.argv[4];


    module.exports( argsObj );
  }

})();
