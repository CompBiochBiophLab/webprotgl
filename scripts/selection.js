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
          for (var i = 0; i < amino.getSize(); ++i) {
            var atomTrf = protein.getAtomTransform(c, a, i);
            op(atomTrf);
          }
        }
      }
    }
  }
}