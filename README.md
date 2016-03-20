# data-formatter
> Takes in a .csv file and formats it to be ready for machine learning using scikit-learn or machineJS

## What it does
`data-formatter` is designed to take care of the chores of machine learning to let you focus on the fun stuff! 

## How to label each column:
Each column must have a label. Your options are few- this is designed to be easy!

Column label options:

1. ID
2. Output Regression
3. Output Category (this is the one to use for numer.ai's early competitions)
4. Output Multi-Category
5. Categorical
6. Continuous
7. Ignore
8. Validation Split (used for the validation column from numer.ai, rarely used otherwise)
9. NLP (please remove all commas and quotes from this column)

For more detailed info, see below. 

### Format of Input File:

1. .csv file
2. The first row holds information describing each column. Specifically, it *must* specify:
  - "Output", the column that holds the variable we are trying to predict for the test dataset, and train on for the training data set. You must specify what type of problem it is we're working with. Accepted values are:
    - "Output Regression" for regression problems
    - "Output Category" for classification problems predicting a single yes or no value
    - "Output Multi-Category" if there are multiple categories included in this output column
    - Note: we do not have any plans to support multiple different output columns in the same training dataset. Multiple categories within the same column of training data is a fully supported use case, but multiple output columns is not. 

  All other columns must be labeled as holding either Categorical or Continuous data:
  - "Categorical": all columns holding strings are categorical. Similarly, if you have saved someone's occupation as a number (1 for engineer, 2 for carpenter, 3 for processional cyclist, etc.), that column must be labeled "Categorical". 
  - "Continuous": any column that should hold only continuous numbers. Any non-numerical values in these columns will be assumed to be missing values, and will be replaced by the median value for that column.
  - "IGNORE": any column that should be ignored. Added for convenience for datasets that would be difficult to manipulate/delete columns from otherwise. 
  - "Validation Split": If you would like to use this column to determine which rows to keep in the training data, and which to split out into the validation data. This is primarily useful for competitors working on the Numer.ai dataset, and should be the header for the "validation" column provided in their first few data sets. 
  - "ID": A column that holds the IDs for each row. Required for the test dataset, not required for the training data
  - "NLP": A column holding text data, such as emails, text messages, medical records, tweets, etc. NOTE: Make sure that all commas and quotes are removed from this column. Most csv parsers assume strictly structured input, while raw text input can be rather messy. 
3. Next row (the second row) must be a header row containing the names of each column.
4. Make sure there are no empty rows!
5. Make sure each row has the same number of columns (even if those columns are blank, they must exist).
6. Make sure any strings are formatted using UTF-8 (don't worry about this one unless you get an odd error message).


## Installation:
This comes pre-bundled with `machineJS`. To use it for other projects: 

To include as a dependency for a specific repo:
```
npm install data-formatter
```

To use from the command line anywhere in your system:
```
npm install -g data-formatter
```


### Some key benefits:

  - It goes through your dataset, and automatically formats it to work with `scikit-learn`, `scikit-neuralnetwork` and `brainjs`.
  - This lets you free up more of your time to create cool new features from the data, and not have to worry about repeating the sometimes arduous process of formatting it for a specific machine learning algorithm. 
  - `data-formatter` formats both your training and your testing data in one fell swoop, so you never need to worry about re-formatting your data, or having incompatible features, once you start making predictions. 
  - This library does some basic feature selection for you, meaning you can throw in a bunch of columns of data that you think are useless, and it will automatically filter out those that don't matter, while focusing in on the truly predictive features. 
  - The library will automatically handle categorical data, so you can pass in a column that holds city names, and it will encode these in a way the machine learning algorithms will understand. 
  - This library will min-max normalize all values for neural networks, to fit their expected API of having only values between -1 and 1 (or 0 and 1 for brain.js).
  - `data-formatter` will go through and replace missing values for you! Missing values in Continuous data columns will get replaced by the median value. Missing data points in Categorical data columns will get replaced by the mode of that column (most frequently occurring value). 
  - Even better, it will test all options: replacing missing values, keeping missing values, and creating a boolean flag noting that there are missing values for this row. We then allow ourselves to be empiricists and simply see which features actually end up being useful through feature selection. 
  - `data-formatter` will remove all categorical values that are present for only one observation, which makes them useless for making predictions. This speeds up training time and fights against overfitting. 

#### Novice?
Does some of that make your head spin? Have no idea what one (or more) of those bullet points means? No worries, that's the entire point of letting a library do this work for you! 

#### Expert?
Did any of the above get your heart racing and make you want to dive in to customize for your own project or kaggle competition? Awesome, follow along with `mainPythonProcess.py` and customize to your heart's content, while still having in place a structure to automate the process for you!


### Format of Output Files:
The formatted data will be broken out into a number of different files, to be compatible with scikit-learn's API:

- `X_train_`: All of the X (non-output-column) features in the training set
- `X_test_`: All of the X features in the testing (predicting) set
- `y_train_`: All of the output columns for the training set. By definition, the testing/predicting data set has no output columns (they have to be predicted!).
- `id_train_`: The ID column for the rows in the training data set. This prevents the ID column from being included as a feature when training a machine learning algorithm. 
- `id_test_`: The ID column for the rows in the testing data set. 
- `X_train_nn_`: All of the X features in the training data set, min-max normalized to have only values between -1 and 1.
- `X_test_nn_`: All of the X features in the testing data set, min-max normalized to have only values between -1 and 1. 

## How to Use Outside of machineJS:
Again, this is baked into machineJS, but if you're using it in a different project:

1. Add a dataDescription row to the top of your training data (more info in a following section)

### Within node.js code using require:
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

### From the command line
```
data-formatter relative/path/to/training/data.csv relative/path/to/testing/data.csv
```
Make sure that you have used the `-g` flag when installing using npm if you want to use `data-formatter` from the command line.


### API Documentation:

#### an `args` object with the following properties:

###### `trainingData`
A full, absolute path to a .csv file. See above for more info on adding an additional dataDescription row to the .csv file itself above the header row.

###### `testingData`
The testing data. This file is assumed to only have a header row, not a dataDescription row. The columns *must* be in the same order as they are for the `trainingData` file. This is almost always the case anyways. 

###### `joinFileName` [OPTIONAL]
A full, absolute path to a .csv file that you would like to join in with the testing and training datasets. This file must have both a dataDescription and a header row. By default, it will be joined on any value in the headerRow that is shared across our training/testing dataset, and the join file.

###### `outputFolder` [OPTIONAL]
This property of the `args` object is optaional. If included, all formatted files will be written to this folder. This folder will be created if it does not exist already. 
DEFAULT: If a value is not passed in, this will default to creating a folder called `data-formatterResults` in whichever directory this library is invoked in. This is designed to make files easy to find if, say, you invoke this library from a directory where you are already working on a machine learning project. 

#### `callback` [OPTIONAL]
After the args object, you may choose to pass in a callback function that will be invoked once training is done. This parameter is optional. If provided, the callback function will be invoked with an object containing the file paths to all of the formatted data files created. 

#### `keepAllFeatures` [OPTIONAL]
If you do not want to perform any feature selection, and keep all the features (both the ones in the original training data, and the ones created by `data-formatter`), pass in `true` for this flag

#### `allFeatureCombinations` [OPTIONAL]
This is still a beta feature. If you want to try adding all possible combinations of continuous features together, set this flag to true. Since it creates all possible combinations of all the continuous features, this can rapidly create a memory problem, and should only be used on small datasets, or if you have a ton of RAM. 



### Using from the command line

As of the 1.2 release, `data-formatter` can be invoked right from the command line. 

#### Installation
```
npm install -g data-formatter
```
Note the "-g" flag directing npm to install the module globally. This makes it available from the command line throughout your entire file directory. 

#### Invoking from the command line
```
data-formatter path/to/training/data.csv path/to/testing/data.csv
```
The formatted data files will be written into whichever directory you invoke `data-formatter` from. 


### Other Random Info

#### machineJS
If you find this library useful, you might want to check out [machineJS](https://github.com/ClimbsRocks/machineJS), which helps reduce the drudge work of other parts of the machine learning process!

#### Contributing- yes please!
There are few things that make me as happy as reading through Pull Requests over a morning espresso :)

#### Starring- yes please!
I've had a great time building this out so far. If you find it useful too, let me know by starring it!

