//<script>

////////////////////////////////////////////////////////////////

function AminoAcid()
{
  var atoms_ = {};

  this.prepareAtoms = function(root, sphere) {
     for (var i in atoms_) {
      var trf = root.addChild();
      trf.translate(atoms_[i][1]);
      trf.addShape(sphere);
      var colour = [1., 1., 1., 1.];
      switch (atoms_[i][0]) {
        case "N":
          colour = [0., 0., 1., 1.];
          break;
        case "O":
          colour = [1., 0., 0., 1.];
          break;
        case "S":
          colour = [1., 1., 0., 1.];
        default:
          break;
      }

      trf.setParameter("colour", createVectorParameter(colour));
    }
  }

  this.setPosition = function(type, name, x, y, z) {
    if (type == "H")
      return;

    atoms_[name] = [type, [x, y, z]];
  }
}

////////////////////////////////////////////////////////////////

function Threonine()
{
  var bbox_ = new BBox();
}

Threonine.prototype = new AminoAcid;
Threonine.prototype.constructor = Threonine;

////////////////////////////////////////////////////////////////

function Chain()
{
  var that = this;

  var aminos_ = [];

  this.addAminoAcid = function(code3) {
    switch (code3) {
    case "THR":
      aminos_.push(new Threonine());
      break;
    default:
      aminos_.push(new AminoAcid());
    }
  }

  this.prepareAtoms = function(root, sphere) {
    var trf = root.addChild();
    for (i in aminos_) {
      aminos_[i].prepareAtoms(trf, sphere);
    }
  }

  this.print = function() {
  }

  this.setAtomPosition = function(pos, type, name, x, y, z) {
    if (pos > aminos_.length) {
      throw new Error("Too far: " + pos);
    }

    var aa = aminos_[pos-1];
    if (aa) {
      aa.setPosition(type, name, x, y, z);
    }
  }
}

////////////////////////////////////////////////////////////////

function Protein()
{
  this.addAminoAcid = function(chainID, code3) {
    var chain = chains_[chainID];
    if (!chain) {
      chain = new Chain();
      chains_[chainID] = chain;
    }
    
    chain.addAminoAcid(code3);
  }

  this.getBarycenter = function() {
    return bbox_.getCenter();
  }

  this.parsePDB = function(pdb) {
    var lines = pdb.split(/[\r\n]+/);
    var rxHeader  = /HEADER\s{4}((?:\w|\s){40})\d\d-\w{3}-\d\d\s{3}(\w{4})/;
    var rxSeqres  = /SEQRES\s(?:\d|\s){3}\s(\w)\s((?:\d|\s){4})\s\s((?:\w{3}\s?){1,13})/;
    var rxAtom    = /ATOM\s\s(?:\d|\s){5}\s((?:\w|\s){4}).(?:\w{3})\s(.)((?:\d|\s){4}).\s{3}(.{8})(.{8})(.{8})(.{6})(.{6})\s{10}(.{2})(.{2})/;
    var rxModel   = /MODEL\s{5}(\s{0,3}\d{1,4})/;
    var rxEndMdl  = /ENDMDL/;
    var match;
    var currentModel = 0;

    for (i in lines) {
      if (match = rxAtom.exec(lines[i])) {
        that.setAtomPosition(currentModel, match[2], match[3].trim(), match[9].trim(), match[1].trim(), parseFloat(match[4].trim()), parseFloat(match[5].trim()), parseFloat(match[6].trim()));
      } else if (match = rxSeqres.exec(lines[i])) {
        var aminos = match[3].split(" ");
        for (a in aminos) {
          if (aminos[a].length > 0)
            that.addAminoAcid(match[1], aminos[a]);
        }
      } else if (match = rxModel.exec(lines[i])) {
        currentModel = match[1].trim();
      } else if (match = rxEndMdl.exec(lines[i])) {
        currentModel = -1;
      } else if (match = rxHeader.exec(lines[i])) {
        that.setID(match[2]);
      }
    }
  }

  this.prepareScene = function(camera, sphere) {
    var root = camera.getGLScene();
    for (c in chains_) {
      chains_[c].prepareAtoms(root, sphere);
    }
  }

  this.print = function() {
    console.log(id_);
    for (c in chains_) {
      chains_[c].print();
    }
  }

  this.setAtomPosition = function(model, chainID, pos, type, name, x, y, z) {
    if (model > 1)
      return;

    if (type == "H")
      return;

    var chain = chains_[chainID];
    if (!chain) {
      throw new Error("No such chain: " + chainID);
    }

    chain.setAtomPosition(pos, type, name, x, y, z);
    bbox_.include([x, y, z]);
  }

  this.setID = function(id) {
    id_ = id;
  }

  var that = this;
  var bbox_ = new BBox();
  var chains_ = {};
  var id_;


////////////////////////////////////////////////////////////////

}
