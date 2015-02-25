//<script>

////////////////////////////////////////////////////////////////

function Selection(protein)
{
  var proteins_ = [protein];
  var selection_ = null;
  var inverted_ = false;

  SelectionState = {
    EXCLUDED: -1,
    PARTIAL :  0,
    SELECTED:  1
  }

  this.selected = function(chain, amino, atom)
  {
    var included = false;
    if (selection_ == null) {
      included = !inverted_;
    } else if (chain in selection_) {
      var c_s = selection_[chain]["state"];
      if (c_s != SelectionState.PARTIAL) {
        included = (c_s == SelectionState.SELECTED) ^ inverted_;
      } else if (amino in selection_[chain]) {
        var a_s = selection_[chain][amino]["state"];
        if (a_s != SelectionState.PARTIAL) {
          included = (a_s == SelectionState.SELECTED) ^ inverted_;
        } else if (atom in selection_[chain][amino]) {
          included = (selection_[chain][amino][atom]["state"] == SelectionState.SELECTED) ^ inverted_;
        } else if (atom) {
          included = inverted_;
        } else {
          return SelectionState.PARTIAL;
        }
      } else if (amino) {
        included = inverted_;
      } else {
        return SelectionState.PARTIAL;
      }
    } else {
      included = inverted_;
    }

    if (included)
      return SelectionState.SELECTED;
    else
      return SelectionState.EXCLUDED;
  }

  this.iterateAtoms = function(op)
  {
    for (p in proteins_) {
      var protein = proteins_[p];
      var chains = protein.getChains();
      for (c in chains) {
        var c_s = this.selected(c);
        if (c_s == SelectionState.EXCLUDED)
          continue;
        //console.log("Chain " + c);
        var chain = chains[c];
        var aminos = chain.getAminos();
        for (a in aminos) {
          var a_s = c_s;
          if (c_s == SelectionState.PARTIAL) {
            a_s = this.selected(c, a);
            if (a_s == SelectionState.EXCLUDED)
              continue;
          }
          //console.log("Amino " + a);
          //console.log(a_s);
          var amino = aminos[a];
          for (var i = 0; i < amino.numberOfAtoms(); ++i) {
            var t_s = a_s;
            if (a_s == SelectionState.PARTIAL) {
              t_s = this.selected(c, a, i);
              if (t_s != SelectionState.SELECTED)
                continue;
            }
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