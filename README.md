# data-formatter
> take an input .csv file and format it to be ready for a neural network

This library is designed to work with ppComplete, but is so broadly useful that I wanted to make it easily available.

## How to use:

### Format of Input File:
1. .csv file
2. First row is a header row
3. The first column holds the output data (what you want the net to make a prediction about). It must be the first column, otherwise we will normalize the data, impute missing values, etc. 
4. Make sure there are no empty rows!
5. Make sure each row has the same number of columns (even if those columns are blank, they must exist)
6. Make sure any strings are formatted using UTF-8. 
7. Make sure there is no empty line at the end of the file. This manifests itself as "unexpected end of input" when parsing that row inside of brainChildMemoryHog.js to add it to our testing set
9. Anything that can be turned into a number will be turned into a number. What this means: do not use numbers for categorical data. For example, if you are saving occupations, save them as ["carpenter","astronaut","cyclist"], not as [24,8,4]. While you may know that 24 actually means "carpenter", the machine will not, and will simply see any rows with the number 24 in them as being 3x more occupation than the rows with 8 in them. An easy way to avoid this is simply to add a letter to each row in this column, which will turn the data into a string, and therefore be recognized as categorical data. For example, [24,8,4] would get turned into ["a24","a8","a4"]


### Format of Output File:



### API

#### trainingData
A .csv file with the full absolute path to the training data. See above for more info on the .csv file itself

#### testingData
A .csv file with the full absolute path to the testing data (the data you want to eventually make predictions against)



