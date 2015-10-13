# data-formatter
> take an input .csv file and format it to be ready for a neural network

This library is designed to work with ppComplete, but is so broadly useful that I wanted to make it easily available.

## How to use:

### Format of Input File:
1. .csv file
2. The first row holds information describing each column. Specifically, it must specify:
  - "ID", the column that holds the IDs
  - "Output", the column that holds the variable we are trying to predict for the test dataset, and train on for the training data set
  All other columns must be labeled as holding either Categorical or Numerical data:
  - "Categorical": all columns holding strings are categorical. Similarly, if you have saved someone's occupation as a number (1 for engineer, 2 for carpenter, 3 for processional cyclist, etc.), that column must be labeled "Categorical". Otherwise, the algorithm won't know any better and will simply think the data says the rows with 3 have 3x the occupation as the rows with 1, rather than simply encoding which category that row belongs in. All non-continuous numbers generally count as categorical data. The easy way to check this is that they will frequently be described as "number of", as in "number of children", "number of trophies", "number of kaggle competitions entered". These are ordinal categories (meaning that having entered 3 kaggle competitions has a relative relationship to having entered 2 kaggle competitions), but they are still categorical data. 
  - "Continuous": any column that should hold only continuous numbers. Any non-numerical values in these columns will be assumed to be missing values, and will be replaced by the median values for this column.
3. Next row (the second row) is a header row containing the names of each column
4. Make sure there are no empty rows!
5. Make sure each row has the same number of columns (even if those columns are blank, they must exist)
6. Make sure any strings are formatted using UTF-8. 


### Format of Output File:



### API

#### trainingData
A .csv file with the full absolute path to the training data. See above for more info on the .csv file itself

#### testingData
A .csv file with the full absolute path to the testing data (the data you want to eventually make predictions against)



