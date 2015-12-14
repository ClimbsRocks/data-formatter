var path = require('path');
module.exports = function(args) {

  if( args.test === undefined ) {
    args.test = false;
  }

  if( args.outputFolder === undefined ) {
    var invokingFolder = path.dirname( module.parent.filename );
    args.outputFolder = path.join( invokingFolder, 'data-formatterResults' );
  }

  // TODO TODO: generalize this so it will work even on long paths that the user sends in
  if( args.trainingPrettyName === undefined ) {
    args.trainingPrettyName = path.basename( args.trainingData ).slice(0,-4);
  }

  // TODO TODO: generalize this so it will work even on long paths that the user sends in
  if( args.testingPrettyName === undefined ) {
    args.testingPrettyName = path.basename( args.testingData ).slice(0,-4);
  }

  if( args.verbose === undefined ) {
    args.verbose = 1;
  }

  // since python will throw a KeyError if we try to access a property that does not exist, set default values for these keys if they are not defined already.
  var propertiesThatPythonExpectsToExist = ['join','on','allFeatureCombinations','keepAllFeatures'];
  for(var i = 0; i < propertiesThatPythonExpectsToExist.length; i++ ) {
    args[propertiesThatPythonExpectsToExist[i]] = args[propertiesThatPythonExpectsToExist[i]] || false;
  }

  return args;
}
