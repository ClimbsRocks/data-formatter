var cwd = process.cwd();
var path = require('path');
var startPyChild = require('./startPyChild.js');

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
    // TODO: make the output folder
    args.outputFolder = path.join( invokingFolder, 'data-formatterResults' );
    fs.stat( args.outputFolder, function(err, stats) {
      if(err) {
        console.error(err);
      }
      if( !stats.isDirectory() ) {
        if( !stats.isFile() ) {
          // the several millisecond hit to performance is not going to be noticeable compared to the minutes or hours this module will take to run, and makes the code much easier to read. 
          fs.mkdirSync(args.outputFolder);
        } else {
          fs.mkdirSync( args.outputFolder + 'Folder' );
        }
      }
      startPyChild( args, callback );
    });
  }
  
  // TODO:
    // figure out where this file is being invoked from
      // module.parent.filename: https://nodejs.org/api/modules.html#modules_module_parent
      // http://stackoverflow.com/questions/20292278/node-get-path-of-the-requiring-parent-file
    // take in flag for neural network, and handle differently than our default assumption of scikit learn and brainjs
    // take in trainingData path
    // take in testingData path
      // make testingData optional?
    // take in optional output folder path?
};
