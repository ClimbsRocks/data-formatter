var expect = require('chai').expect;
var mocha = require('mocha');

module.exports = function() {

  describe('sumById', function() {
  
    var idColumn;
    var outputColumn;
    var X;
    var trainingLength;

    before(function(done) {
      console.time('sumByID time');
      pyController.on('message', function(message) {
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

    it('should not change datasets where IDs are only present in one row', function() {
      expect(X.length).to.equal(251503);
      expect(idColumn.length).to.equal(251503);
      expect(outputColumn.length).to.equal(251503);
      expect(trainingLength).to.equal(150000);
    });
    
  });


};
