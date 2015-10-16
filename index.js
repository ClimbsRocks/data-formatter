var cwd = process.cwd();
var startPyChild = require('./startPyChild.js');

module.exports= function(args) {
  // TODO: allow the user to pass in a flag for "decideCategoricalOrContinuous"
    // do the data formatting process twice:
      // once with the inputs as the user has them laid out
      // and once where we force anything that can be a float into a float, regardless of whether the user classified it as a categorical variable or not. 
    // then go through, train a small ensemble, and see which data set does better

}
