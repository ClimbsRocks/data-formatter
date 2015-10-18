var fs = require('fs');
var path = require('path');

var mkdirp = require('mkdirp');

var startPyChild = require('./startPyChild.js');

var cwd = process.cwd();

module.exports= function( args, callback ) {
  // the following is a way-past-MVP idea that probably makes more sense for users to do themselves. 
  // TODO: allow the user to pass in a flag for "decideCategoricalOrContinuous"
    // do the data formatting process twice:
      // once with the inputs as the user has them laid out
      // and once where we force anything that can be a float into a float, regardless of whether the user classified it as a categorical variable or not. 
    // then go through, train a small ensemble, and see which data set does better

  if( args.test === undefined ) {
    args.test = false;
  }

  var invokingFolder = path.dirname( module.parent.filename );

  if( args.outputFolder === undefined ) {
    args.outputFolder = path.join( invokingFolder, 'data-formatterResults' );
  }

  // make sure the output folder exists. if not, create it.
  mkdirp( args.outputFolder, function(err) {
    if(err) {
      console.error(err);
    }
    startPyChild( args, callback );
  });
  
  // TODO:
    // figure out where this file is being invoked from
      // module.parent.filename: https://nodejs.org/api/modules.html#modules_module_parent
      // http://stackoverflow.com/questions/20292278/node-get-path-of-the-requiring-parent-file
    // take in flag for neural network, and handle differently than our default assumption of scikit learn and brainjs
    // take in testingData path
      // make testingData optional?
};
