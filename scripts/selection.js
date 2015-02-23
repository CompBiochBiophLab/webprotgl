//<script>

////////////////////////////////////////////////////////////////

function Selection(protein)
{
  var proteins_ = [protein];

  this.iterateAtoms = function(op)
  {
    for (p in proteins_) {
      var protein = proteins_[p];
      var chains = protein.getChains();
      for (c in chains) {
        var chain = chains[c];
        var aminos = chain.getAminos();
        for (a in aminos) {
          var amino = aminos[a];
          for (var i = 0; i < amino.numberOfAtoms(); ++i) {
            var atomTrf = protein.getAtomTransform(c, a, i);
            op(atomTrf);
          }
        }
      }
    }
  }

  this.iterateBonds = function(op)
  {
    for (p in proteins_) {
      var protein = proteins_[p];
      var chains = protein.getChains();
      for (c in chains) {
        var chain = chains[c];
        var aminos = chain.getAminos();
        for (a in aminos) {
          var amino = aminos[a];
          var nob = amino.numberOfBonds();
          for (var i = 0; i < nob; ++i) {
            var bondTrf = protein.getBondTransform(c, a, i);
            op(bondTrf);
          }
          // Link to previous amino acid
          var bondTrf = protein.getBondTransform(c, a, nob);
          if (bondTrf)
            op(bondTrf);
        }
      }
    }
  }
}