var expect = require('chai').expect;
var mocha = require('mocha');

module.exports = function() {

  describe('sumByID', function() {
    
    var idColumn;
    var outputColumn;
    var X;
    var trainingLength;

    before(function(done) {

      console.time('sumByID time');
      pyControllerWmt.on('message', function(message) {
        if(message.type === 'sumById.py') {

          idColumn = message.text[1];
          trainingLength = message.text[2];
          outputColumn = message.text[3];
          X = message.text[0];

          console.timeEnd('sumByID time');
          done();
        }
      });
    });

    it('should turn each ID into a single row of data', function() {
      var idSummaryObj = {};

      function summarizeIDColumn() {
        for (var i = 0; i < idColumn.length; i++) {
          var id = idColumn[i];
          if( idSummaryObj[id] !== undefined) {
            return false;
          } else {
            idSummaryObj[id] = 1;
          }
        }
        return true;
      }

      expect( summarizeIDColumn( idColumn) ).to.be.true;

    });

    it('should not have id or output column in the rowObj itself, only in their own separate columns', function() {
      function checkForIDAndOutput(results) {
        for( var i = 0; i < results.length; i++) {
          var rowObj = results[i];
          for( var key in rowObj ) {
            if( key === 'id' || key === 'output') {
              console.log('rowObj:',rowObj);
              return false;
            }
          }
        }
        return true;
      };

      expect( checkForIDAndOutput(X) ).to.be.true;
    });



    it('should return a list of dictionaries', function() {
      function checkForObjects(results) {
        for( var i = 0; i < results.length; i++) {
          if( results[i].constructor !== Object) {
            return false;
          }
        }
        return true;
      }

      expect( checkForObjects(X) ).to.be.true;

    });

    it('should have columns for each category', function() {

      function countColumns(results) {
        var count = 0;
        var columnSummary = {};
        for( var i = 0; i < results.length; i++) {
          for( var key in results[i]) {
            if( columnSummary[key] === undefined) {
              count++;
              columnSummary[key] = true;
            } 
          }
        }
        return count;
      }
      expect( countColumns(X) ).to.equal(660);
    });

    // it('should sum up results by id for each category', function() {
    //   // TODO: get the expected sum of each aggregated column by calculating it manually
    //     // compare the observed sums to those to make sure it's calculating correctly!
    // });


    it('should keep track of which IDs are part of the training set, and which are in the testing set', function() {
      var trainingIDs = [5,7,8,9,10,11,12,15,17,19,20,23,25,26,28,29,30,31,32,33,40,41,42,43,45,47,49,50,51,53,54,55,56,57,61,63,68,69,72,74,76,79,81,83,84,85,86,87,91,92,93,95,97,98,99,100,102,103,105,106,107,110,117,121,123,124,125,130,132,133,134,137,138,139,140,145,146,152,153,154,155,162,164,177,179,181,182,185,188,189,190,194,195,199,203,205,207,209,210,211,214,216,217,218,219,220,221,223,224,225,228,229,232,235,236,238,239,241,245,248,251,252,253,255,256,257,259,261,263,265,267,274,275,277,278,279,281,283,284,285,286,287,288,289,290,291,292,295,298,302,308,309,310,312,313,314,315,316,317,322,323,324,325,326,328,330,333,334,335,341,343,344,346,347,348,349,350,351,357,358,359,360,361,362,363,367,369,371,372,373,375,377,378,379,382,383,384,385,386,387,388,389,390,393,394,396,397,398,399,400,402,403,407,408,409,412,413,418,419,420,421,425,427];
      var testingIDs = [1,2,3,4,6,13,14,16,18,21,22,24,27,34,35,36,37,38,39,44,46,48,52,58,59,60,62,64,65,66,67,70,71,73,75,77,78,80,82,88,89,90,94,96,101,104,108,109,111,112,113,114,115,116,118,119,120,122,126,127,128,129,131,135,136,141,142,143,144,147,148,149,150,151,156,157,158,159,160,161,163,165,166,167,168,169,170,171,172,173,174,175,176,178,180,183,184,186,187,191,192,193,196,197,198,200,201,202,204,206,208,212,213,215,222,226,227,230,231,233,234,237,240,242,243,244,246,247,249,250,254,258,260,262,264,266,268,269,270,271,272,273,276,280,282,293,294,296,297,299,300,301,303,304,305,306,307,311,318,319,320,321,327,329,331,332,336,337,338,339,340,342,345,352,353,354,355,356,364,365,366,368,370,374,376,380,381,391,392,395,401,404,405,406,410,411,414,415,416,417,422,423,424,426,428,429,432,434,435,438,439,440,441,442,443,444,445,450,451,454,455,459,463,464,467];
      function checkIDs(idColumn, trainingLength) {
        for( var i = 0; i < trainingLength; i++) {
          if( trainingIDs.indexOf( parseInt(idColumn[i], 10) ) === -1) {
            console.log('the id that is incorrectly sorted as a training ID is:',idColumn[i]);
            return idColumn[i];
          }
        }
        for (var i = trainingLength; i < idColumn.length; i++) {
          if( testingIDs.indexOf( parseInt(idColumn[i], 10) ) === -1) {
            console.log('the id that is incorrectly sorted as a testing ID is:',idColumn[i]);
            return idColumn[i];
          }
        }
        return true;
      }
      expect( checkIDs(idColumn, trainingLength) ).to.be.true;

    });

    // it('should return new idColumn and outputColumn lists that match up to the order of X', function() {
    //   // check some IDs, and test against their known output value
    //   // also check lengths of these lists
    // });

    after(function() {
      idColumn = null;
      outputColumn = null;
      X = null;
      trainingLength = null;
    });
    
  });

};
