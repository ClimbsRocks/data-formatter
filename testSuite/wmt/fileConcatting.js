var expect = require('chai').expect;
var mocha = require('mocha');

module.exports = function() {


  describe('fileConcatting', function() {

    var results;

    before(function(done) {
      console.time('file concatting time');

      pyControllerWmt.on('message', function(message) {
        // message is the message object coming to us from the Python process
        if(message.type === 'concat.py') {
          results = message.text;
          console.timeEnd('file concatting time');
          done();
        }  
      });

    });

    it('should delete columns with a dataDescription header of "IGNORE"', function() {
      // dataDescription row
      expect( results[0].length ).to.equal(4);
      // headerRow
      expect( results[1].length ).to.equal(4);
      // our X dataset
      var allRowsEqual4 = true;
      for( var i = 0; i < results[3].length; i++) {
        if( results[3][i].length !== 4 ) {
          allRowsEqual4 = false;
          break;
        }
      }
      expect( allRowsEqual4 ).to.be.true;
    });


    after(function() {
      results[0] = null;
      results[1] = null;
      results[2] = null;
      results[3] = null;
      results = null;
    });

  });
};
