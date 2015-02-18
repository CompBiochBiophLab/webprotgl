//<script>

////////////////////////////////////////////////////////////////

function Selection()
{
  var proteins_ = [];

  this.iterateAtoms = function()
  {
    for (p in proteins_) {
      protein = proteins_[p];
      chains = protein.getChains();
      for (c in chains) {
        chain = chains[c];
        aminos = chain.getAminos();
        for (a in aminos) {

        }
      }
    }
  }
}