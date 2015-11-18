var expect = require('chai').expect;
var mocha = require('mocha');
var killChildProcess = require('../killChildProcess');

module.exports = function() {

  describe('joining data', function() {
    
    var dataDescription;
    var headerRow;
    var X;
    var problemType;

    before(function(done) {

      console.time('joiningData time');
      pyControllerRossman.on('message', function(message) {
        if(message.type === 'join.py') {


          X = message.text[0];
          dataDescription = message.text[1];
          headerRow = message.text[2];
          problemType = message.text[3];

          console.timeEnd('joiningData time');
          // setTimeout(function() {
            killChildProcess(global.pyControllerRossman.childProcess);
          // },25000);
          done();
        }
      });
    });

    // should have a certain number of columns
    it('should have columns from the input data and join data', function() {
      expect( X[0].length ).to.equal(13);
    });
    // compare the sums of columns to known correct values

    it('should include all the X data', function() {
      expect( X.length ).to.equal( 99999 + 41088 )
    });

    it('should only include joinFile values that match up to a row in X', function() {
      // TODO: add in fake values to our dataset
      function noNonMatchedValues() {
        for( var i = 0; i < X.length; i++) {
          for( var j = 0; j < X[i].length; j++) {
            if( j === 'SHOULD_NOT_EXIST' ) {
              return X[i];
            }
          }
        }
        return true;
      }

      expect( noNonMatchedValues() ).to.be.true;

    });

    // ideally, test for cases where we pass in a join value, and cases where we do not, and just match it up based on matching header names
    // dataDescription row should have certain values and a certain length
    it('should have accurate dataDescription values for all columns', function() {
      var expectedDataDescription = ["categorical","categorical","categorical","categorical","categorical","categorical","categorical","categorical","continuous","categorical","categorical","categorical","categorical"];
      expect( dataDescription.length ).to.equal(13);
      expect( dataDescription ).to.deep.equal( expectedDataDescription );
    })
    // header row should have certain values and a certain length
    it('should have accurate headerRow values for all columns', function() {
      var expectedHeader = ["store","dayofweek","open","promo","stateholiday","schoolholiday","storetype","assortment","competitiondistance","competitionopensinceyear","promo2","promo2sinceyear","promointerval"];
      expect( headerRow ).to.deep.equal( expectedHeader );
      expect( headerRow.length ).to.equal(13);
    });

    it('should keep track of the problem type (regression or category', function() {
      expect( problemType ).to.equal('regression');
    });

    after(function() {
      dataDescription = null;
      headerRow = null;
      X = null;
      trainingLength = null;
    });
    
  });


};
