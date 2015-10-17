var cwd = process.cwd();
var startPyChild = require('./startPyChild.js');

module.exports= function(args) {
  // the following is a way-past-MVP idea that probably makes more sense for users to do themselves. 
  // TODO: allow the user to pass in a flag for "decideCategoricalOrContinuous"
    // do the data formatting process twice:
      // once with the inputs as the user has them laid out
      // and once where we force anything that can be a float into a float, regardless of whether the user classified it as a categorical variable or not. 
    // then go through, train a small ensemble, and see which data set does better

  // TODO:
    // figure out where this file is being invoked from
    // take in flag for neural network, and handle differently than our default assumption of scikit learn and brainjs
    // take in trainingData path
    // take in testingData path
      // make testingData optional?
    // take in optional output folder path?
}
