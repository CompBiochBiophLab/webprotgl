//<script>

////////////////////////////////////////////////////////////////

function AminoAcid()
{
  var atoms_ = [];
//  var bonds_ = [[0,1], [1,2], [2,3]];
//  var size_ = 4;

  this.addAtom = function(x, y, z) {
    atoms_.push([x, y, z]);
  }
//  this.addBond = function(bond) { bonds_.push(bond); }

//  this.getBonds = function() { return [[0,1], [1,2], [2,3]]; }
//  this.getSize = function() { return 4; }

  this.prepareAtoms = function(root, sphere) {
    for (var i in atoms_) {
      if (atoms_[i][0] > 1e10)
        continue;
      var trf = root.addChild();
      trf.translate(atoms_[i]);
      trf.addShape(sphere);
      var colour = [1., 1., 1., 1.];
      /*switch (atoms_[i][0]) {
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
      }*/

      trf.setParameter("colour", createVectorParameter(colour));
    }
  }
/*
  this.setPosition = function(type, name, x, y, z) {
    if (type == "H")
      return;

    atoms_[name] = [type, [x, y, z]];
  }
  */
}

////////////////////////////////////////////////////////////////

function Alanine() {}
Alanine.prototype = new AminoAcid;
Alanine.prototype.getSize = function() { return 5; }
Alanine.prototype.getBonds = function() { return [[0,1], [1,2], [2,3], [1,4]]; }
Alanine.prototype.newInstance = function() { return new Alanine(); }

function Arginine() {}
Arginine.prototype = new AminoAcid;
Arginine.prototype.getSize = function() { return 11; }
Arginine.prototype.getBonds = function() { return [[0,1], [1,2], [2,3], [1,4], [4,5], [5,6], [6,7], [7,8], [8,9], [8,10]]; }
Arginine.prototype.newInstance = function() { return new Arginine(); }

function Asparagine() {}
Asparagine.prototype = new AminoAcid;
Asparagine.prototype.getSize = function() { return 8; }
Asparagine.prototype.getBonds = function() { return [[0,1], [1,2], [2,3], [1,4], [4,5], [5,6], [5,7]]; }
Asparagine.prototype.newInstance = function() { return new Asparagine(); }

function AsparticAcid() {}
AsparticAcid.prototype = new AminoAcid;
AsparticAcid.prototype.getSize = function() { return 8; }
AsparticAcid.prototype.getBonds = function() { return [[0,1], [1,2], [2,3], [1,4], [4,5], [5,6], [5,7]]; }
AsparticAcid.prototype.newInstance = function() { return new AsparticAcid(); }

function Cysteine() {}
Cysteine.prototype = new AminoAcid;
Cysteine.prototype.getSize = function() { return 6; }
Cysteine.prototype.getBonds = function() { return [[0,1], [1,2], [2,3], [1,4], [4,5]]; }
Cysteine.prototype.newInstance = function() { return new Cysteine(); }

function GlutamicAcid() {}
GlutamicAcid.prototype = new AminoAcid;
GlutamicAcid.prototype.getSize = function() { return 9; }
GlutamicAcid.prototype.getBonds = function() { return [[0,1], [1,2], [2,3], [1,4], [4,5], [5,6], [6,7], [6,8]]; }
GlutamicAcid.prototype.newInstance = function() { return new GlutamicAcid(); }

function Glutamine() {}
Glutamine.prototype = new AminoAcid;
Glutamine.prototype.getSize = function() { return 9; }
Glutamine.prototype.getBonds = function() { return [[0,1], [1,2], [2,3], [1,4], [4,5], [5,6], [6,7], [6,8]]; }
Glutamine.prototype.newInstance = function() { return new Glutamine(); }

function Glycine() {}
Glycine.prototype = new AminoAcid;
Glycine.prototype.getSize = function() { return 4; }
Glycine.prototype.getBonds = function() { return [[0,1], [1,2], [2,3]]; }
Glycine.prototype.newInstance = function() { return new Glycine(); }

function Histidine() {}
Histidine.prototype = new AminoAcid;
Histidine.prototype.getSize = function() { return 10; }
Histidine.prototype.getBonds = function() { return [[0,1], [1,2], [2,3], [1,4], [4,5], [5,6], [5,7], [6,8], [7,9], [8,9]]; }
Histidine.prototype.newInstance = function() { return new Histidine(); }

function Isoleucine() {}
Isoleucine.prototype = new AminoAcid;
Isoleucine.prototype.getSize = function() { return 8; }
Isoleucine.prototype.getBonds = function() { return [[0,1], [1,2], [2,3], [1,4], [4,5], [4,6], [5,7]]; }
Isoleucine.prototype.newInstance = function() { return new Isoleucine(); }

function Leucine() {}
Leucine.prototype = new AminoAcid;
Leucine.prototype.getSize = function() { return 8; }
Leucine.prototype.getBonds = function() { return [[0,1], [1,2], [2,3], [1,4], [4,5], [5,6], [5,7]]; }
Leucine.prototype.newInstance = function() { return new Leucine(); }

function Lysine() {}
Lysine.prototype = new AminoAcid;
Lysine.prototype.getSize = function() { return 9; }
Lysine.prototype.getBonds = function() { return [[0,1], [1,2], [2,3], [1,4], [4,5], [5,6], [6,7], [7,8]]; }
Lysine.prototype.newInstance = function() { return new Lysine(); }

function Methionine() {}
Methionine.prototype = new AminoAcid;
Methionine.prototype.getSize = function() { return 8; }
Methionine.prototype.getBonds = function() { return [[0,1], [1,2], [2,3], [1,4], [4,5], [5,6], [6,7]]; }
Methionine.prototype.newInstance = function() { return new Methionine(); }

function Phenylalanine() {}
Phenylalanine.prototype = new AminoAcid;
Phenylalanine.prototype.getSize = function() { return 11; }
Phenylalanine.prototype.getBonds = function() { return [[0,1], [1,2], [2,3], [1,4], [4,5], [5,6], [5,7], [6,8], [7,9], [8,10], [9,10]]; }
Phenylalanine.prototype.newInstance = function() { return new Phenylalanine(); }

function Proline() {}
Proline.prototype = new AminoAcid;
Proline.prototype.getSize = function() { return 7; }
Proline.prototype.getBonds = function() { return [[0,1], [1,2], [2,3], [1,4], [4,5], [5,6], [5,0]]; }
Proline.prototype.newInstance = function() { return new Proline(); }

function Pyrrolysine() {}
Pyrrolysine.prototype = new AminoAcid;
Pyrrolysine.prototype.getSize = function() { return 17; }
//Pyrrolysine.prototype.getBonds = function() { return [[0,1], [1,2], [2,3], [1,4], [4,5], [5,6], [6,7], [7,8], [8,9], [9,10], [9,11], ...]; }
Pyrrolysine.prototype.newInstance = function() { return new Pyrrolysine(); }

function Selenocysteine() {}
Selenocysteine.prototype = new AminoAcid;
Selenocysteine.prototype.getSize = function() { return 6; }
Selenocysteine.prototype.getBonds = function() { return [[0,1], [1,2], [2,3], [1,4]]; }
Selenocysteine.prototype.newInstance = function() { return new Selenocysteine(); }

function Serine() {}
Serine.prototype = new AminoAcid;
Serine.prototype.getSize = function() { return 6; }
Serine.prototype.getBonds = function() { return [[0,1], [1,2], [2,3], [1,4], [4,5]]; }
Serine.prototype.newInstance = function() { return new Serine(); }

function Threonine() {}
Threonine.prototype = new AminoAcid;
Threonine.prototype.getSize = function() { return 7; }
Threonine.prototype.getBonds = function() { return [[0,1], [1,2], [2,3], [1,4], [4,5], [4,6]]; }
Threonine.prototype.newInstance = function() { return new Threonine(); }

function Tryptophan() {}
Tryptophan.prototype = new AminoAcid;
Tryptophan.prototype.getSize = function() { return 14; }
Tryptophan.prototype.getBonds = function() { return [[0,1], [1,2], [2,3], [1,4], [4,5], [5,6], [5,7], [6,8], [7,9], [8,9], [7,10], [9,11], [10,12], [11,13], [12,13]]; }
Tryptophan.prototype.newInstance = function() { return new Tryptophan(); }

function Tyrosine() {}
Tyrosine.prototype = new AminoAcid;
Tyrosine.prototype.getSize = function() { return 12; }
Tyrosine.prototype.getBonds = function() { return [[0,1], [1,2], [2,3], [1,4], [4,5], [5,6], [5,7], [6,8], [7,9], [8,10], [9,10], [10,11]]; }
Tyrosine.prototype.newInstance = function() { return new Tyrosine(); }

function Valine() {}
Valine.prototype = new AminoAcid;
Valine.prototype.getSize = function() { return 7; }
Valine.prototype.getBonds = function() { return [[0,1], [1,2], [2,3], [1,4], [4,5], [4,6]]; }
Valine.prototype.newInstance = function() { return new Valine(); }

////////////////////////////////////////////////////////////////

function Chain()
{
  var that = this;

  var aminos_ = [];

  var mapAminos_ = {
    'A': new Alanine(),
    'B': new AsparticAcid(),
    'C': new Cysteine(),
    'D': new AsparticAcid(),
    'E': new GlutamicAcid(),
    'F': new Phenylalanine(),
    'G': new Glycine(),
    'H': new Histidine(),
    'I': new Isoleucine(),
    'J': new Isoleucine(),
    'K': new Lysine(),
    'L': new Leucine(),
    'M': new Methionine(),
    'N': new Asparagine(),
    //'O': new Pyrrolysine(),
    'P': new Proline(),
    'Q': new Glutamine(),
    'R': new Arginine(),
    'S': new Serine(),
    'T': new Threonine(),
    'U': new Selenocysteine(),
    'V': new Valine(),
    'W': new Tryptophan(),
    //'X': new AminoAcid(),
    'Y': new Tyrosine(),
    'Z': new GlutamicAcid()
  };

  this.addAminoAcid1 = function(code) {
    var amino = mapAminos_[code];
    if (amino)
      amino = amino.newInstance();
    else
      amino = new AminoAcid();

    aminos_.push(amino);
    return amino;
  }
/*
  this.addAminoAcid3 = function(code3) {
    switch (code3) {
    case "THR":
      aminos_.push(new Threonine());
      break;
    default:
      aminos_.push(new AminoAcid());
    }
  }
*/
  this.prepareAtoms = function(root, sphere) {
    var trf = root.addChild();
    for (i in aminos_) {
      console.log(i);
      aminos_[i].prepareAtoms(trf, sphere);
    }
  }

  this.print = function() {
  }
/*
  this.setAtomPosition = function(pos, type, name, x, y, z) {
    if (pos > aminos_.length) {
      throw new Error("Too far: " + pos);
    }

    var aa = aminos_[pos-1];
    if (aa) {
      aa.setPosition(type, name, x, y, z);
    }
  }
  */
}

////////////////////////////////////////////////////////////////

function Protein()
{
	/*
  this.addAminoAcid = function(chainID, code3) {
    var chain = chains_[chainID];
    if (!chain) {
      chain = new Chain();
      chains_[chainID] = chain;
    }
    
    chain.addAminoAcid3(code3);
  }
*/
  this.getBarycenter = function() {
    return bbox_.getCenter();
  }

  this.parse = function(data) {
    // Make a buffer on the data
    var buffer = new jDataView(data);
    var offset = 0;

    // Version: unsigned short
    var version = buffer.getUint16(offset, true);
    offset += 2;

    console.log("Version " + version);

    // # Sequences: ui8
    var totSequences = buffer.getUint8(offset);
    offset += 1;
    console.log(totSequences + " sequences");

    for (var seq = 0; seq < totSequences; ++seq) {
      // Char: ID
      var sid = buffer.getChar(offset);
      offset += 1;
      console.log("Sequence " + sid);

      // Type of sequence: Protein=0, DNA=1, RNA=2
      var stype = buffer.getUint8(offset);
      offset += 1;
      console.log("Type " + stype);

      offset = this.__parseProtein(sid, buffer, offset);
      break;
    }
  }

  this.__parseProtein = function(sid, buffer, offset) {
    chain = new Chain();
    chains_[sid] = chain;

    // Total residues
    var totRes = buffer.getUint16(offset, true);
    offset += 2;
      
    var sequence = buffer.getString(totRes, offset);
    offset += totRes;
    console.log(sequence);

    // Total atoms
    var totAtoms = buffer.getInt32(offset, true);
    offset += 4;
    console.log(totAtoms + " atoms");

    var sum = 0;
    for (var res = 0; res < totRes; ++res) {
      var amino = chain.addAminoAcid1(sequence[res]);
//      console.log(amino.getSize());
      for (var atom = 0; atom < amino.getSize(); ++atom) {
        var x = buffer.getFloat32(offset, true);
        offset += 4;
        var y = buffer.getFloat32(offset, true);
        offset += 4;
        var z = buffer.getFloat32(offset, true);
        offset += 4;
        amino.addAtom(x, y, z);
        ++sum;
      }
    }
    console.log(sum);
    return offset;
  }
/*
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
*/
  this.prepareScene = function(camera, sphere) {
    var root = camera.getGLScene();
    for (c in chains_) {
      console.log(c);
      chains_[c].prepareAtoms(root, sphere);
      console.log("chain");
    }
  }

  this.print = function() {
    //console.log(id_);
    for (c in chains_) {
      chains_[c].print();
    }
  }
/*
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
*/
  this.setID = function(id) {
    id_ = id;
  }

  var that = this;
  var bbox_ = new BBox();
  var chains_ = {};
  var id_;


////////////////////////////////////////////////////////////////

}
