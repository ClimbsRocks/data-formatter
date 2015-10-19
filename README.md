# data-formatter
> take in a .csv file and format it to be ready for machine learning in scikit-learn, or a neural network like brain.js

This library is designed to work with ppComplete, but is so broadly useful that I wanted to make it easily available.

## Installation:
```
npm install data-formatter
```

## What it does
`data-formatter` is designed to take care of the chores of machine learning to let you focus on the fun stuff! 

### Some key benefits:
  - It goes through your dataset, and automatically formats it to work with `scikit-learn`, `scikit-neuralnetwork` and `brainjs`.
  - This lets you free up more of your time to create cool new features from the data, and not have to worry about repeating the sometimes arduous process of formatting it for a specific machine learning algorithm. 
  - `data-formatter` formats both your training and your testing data in one fell swoop, so you never need to worry about re-formatting your data, or having incompatible features, once you start making predictions. 
  - This library does some basic feature selection for you, meaning you can throw in a bunch of columns of data that you think are useless, and it will automatically filter out those that don't matter, while focusing in on the truly predictive features. 
  - The library will automatically handle categorical data, so you can pass in a column that holds city names, and it will encode these in a way the machine learning algorithms will understand. 
  - This library will min-max normalize all values for neural networks, to fit their expected API of having only values between -1 and 1 (or 0 and 1 for brain.js).
  - `data-formatter` will go through and replace missing values for you! Missing values in Continuous data columns will get replaced by the median value. Missing data points in Categorical data columns will get replaced by the mode of that column (most frequently occurring value). 

#### Novice?
Does some of that make your head spin? Have no idea what one (or more) of those bullet points means? No worries, that's the entire point of letting a library do this work for you! 

#### Expert?
Did any of the above get your heart racing and make you want to dive in to customize for your own project or kaggle competition? Awesome, follow along with `pyController.py` and customize to your heart's content, while still having in place a structure to automate the process for you!

## How to Use:
1. Add a dataDescription row to the top of your training data (more info in a following section)
2. Require the module:
`var df = require('data-formatter');`
3. Invoke with an object that has `trainingData` and `testingData` properties, and an optional callback:
```
df({
  trainingData: full/absolute/path/to/training/data.csv,
  testingData:  full/absolute/path/to/testing/data.csv
}, callbackFunc);
````
The optional callback will be called once all data formatting has completed.

### Format of Input File:

1. .csv file
2. The first row holds information describing each column. Specifically, it *must* specify:
  - "ID", the column that holds the IDs
  - "Output", the column that holds the variable we are trying to predict for the test dataset, and train on for the training data set
  All other columns must be labeled as holding either Categorical or Numerical data:
  - "Categorical": all columns holding strings are categorical. Similarly, if you have saved someone's occupation as a number (1 for engineer, 2 for carpenter, 3 for processional cyclist, etc.), that column must be labeled "Categorical". 
  - "Continuous": any column that should hold only continuous numbers. Any non-numerical values in these columns will be assumed to be missing values, and will be replaced by the median value for that column.
3. Next row (the second row) must be a header row containing the names of each column.
4. Make sure there are no empty rows!
5. Make sure each row has the same number of columns (even if those columns are blank, they must exist).
6. Make sure any strings are formatted using UTF-8 (don't worry about this one unless you get an odd error message).

## API Documentation:

#### an `args` object with the following properties:

###### `trainingData`
A full, absolute path to a .csv file. See above for more info on adding an additional dataDescription row to the .csv file itself above the header row.

###### `testingData`
The testing data. This file is assumed to only have a header row, not a dataDescription row. The columns *must* be in the same order as they are for the `trainingData` file. This is almost always the case anyways. 

###### `outputFolder` [OPTIONAL]
This property of the `args` object is optaional. If included, all formatted files will be written to this folder. This folder will be created if it does not exist already. 
DEFAULT: If a value is not passed in, this will default to creating a folder called `data-formatterResults` in whichever directory this library is invoked in. This is designed to make files easy to find if, say, you invoke this library from a directory where you are already working on a machine learning project. 

#### `callback` [OPTIONAL]
After the args object, you may choose to pass in a callback function that will be invoked once training is done. This parameter is optional. If provided, the callback function will be invoked with an object containing the file paths to all of the formatted data files created. 


### Format of Output Files:
The formatted data will be broken out into a number of different files, to be compatible with scikit-learn's API:
- `X_train_`: All of the X (non-output-column) features in the training set
- `X_test_`: All of the X features in the testing (predicting) set
- `y_train_`: All of the output columns for the training set. By definition, the testing/predicting data set has no output columns (they have to be predicted!).
- `id_train_`: The ID column for the rows in the training data set. This prevents the ID column from being included as a feature when training a machine learning algorithm. 
- `id_test_`: The ID column for the rows in the testing data set. 
- `X_train_nn_`: All of the X features in the training data set, min-max normalized to have only values between -1 and 1.
- `X_test_nn_`: All of the X features in the testing data set, min-max normalized to have only values between -1 and 1. 


### Other Random Info

#### ppComplete
If you find this library useful, you might want to check out [ppComplete](https://github.com/ClimbsRocks/ppComplete), which helps reduce the drudge work of other parts of the machine learning process!

#### Contributing- yes please!
There are few things that make me as happy as reading through Pull Requests over a morning espresso :)

#### Starring- yes please!
I've had a great time building this out so far. If you find it useful too, let me know by starring it!

#### More information on Categorical data:
All columns holding strings are categorical. Similarly, if you have saved someone's occupation as a number (1 for engineer, 2 for carpenter, 3 for processional cyclist, etc.), that column must be labeled "Categorical". Otherwise, the algorithm won't know any better and will simply think the data says the rows with 3 have 3x the occupation as the rows with 1, rather than simply encoding which category that row belongs in. All non-continuous numbers generally count as categorical data. The easy way to check this is that they will frequently be described as "number of", as in "number of children", "number of trophies", "number of kaggle competitions entered". These are ordinal categories (meaning that having entered 3 kaggle competitions has a relative relationship to having entered 2 kaggle competitions), but they are still categorical data. 
