
import re
from datetime import datetime
from io import BytesIO
from struct import *

class PDBParser:
  MIMETYPE = "pdb"
  __PROTEIN = 0
  __DNA     = 1
  __RNA     = 2
  VERSION_1 = 1
  VERSION_CURRENT = VERSION_1

  def __init__(self):
    self.__re_header = re.compile("\\s{4}((?:\\w|\\s){40})(\\d\\d)-(\\w{3})-(\\d\\d)\\s{3}(\\w{4})\\s*")
    self.__re_sequence = re.compile("\\s(?:\\d|\\s){3}\\s(\\w)\\s((?:\\d|\\s){4})\\s\\s((?:\\w{3}\\s?){1,13})")
    self.__re_modres = re.compile("\\s[\\s\\w]{4}\\s(\\w{3})\\s(\\w)\\s([\\s\\d]{4})[\\s\\w]\\s([\\s\\w]{3})\\s\\s[\\s\\w]{0,41}")
    self.__re_hetero = re.compile("\\s([\\s\\w]{3})\\s\\s(\\w)([\\s\\d]{4})([\\s\\d])\\s\\s([\\s\\d]{5})\\s{0,5}[\\s\\w]{0,40}")
    self.__re_model = re.compile("\\s{4}(\\s{0,3}\\d{1,4})")
    self.__re_atom = re.compile("[\\s\\d]{5}\\s([\\s\\w]{4}).[\\w]{3}\\s(.)([\\s\\d]{4}).\\s{3}(.{8})(.{8})(.{8})(.{6})(.{6})\\s{10}(.{2})(.{2})")

    self.__rna = {"A": "A", "U": "U", "G": "G", "C": "C", "I": "I"}
    self.__dna = {"DA": "A", "DT": "T", "DG": "G", "DC": "C"}
    self.__321 = {"ALA": ("A",  5), "ARG": ("R", 11), "ASN": ("N",  8),
                  "ASP": ("D",  8), "CYS": ("C",  6), "GLU": ("E",  9),
                  "GLN": ("Q",  9), "GLY": ("G",  4), "HIS": ("H", 10),
                  "ILE": ("I",  8), "LEU": ("L",  8), "LYS": ("K",  9),
                  "MET": ("M",  8), "PHE": ("F", 11), "PRO": ("P",  7),
                  "SER": ("S",  6), "THR": ("T",  7), "TRP": ("W", 14),
                  "TYR": ("Y", 12), "VAL": ("V",  7), "SEC": ("U",  6),
                  "PYL": ("O", 17), "ASX": ("B",  8), "GLX": ("Z",  9),
                  "XLE": ("J",  8), "XAA": ("X",  0), "UNK": ("X",  0)}
    self.__123 = dict()
    for item in self.__321:
      (o, l) = self.__321[item]
      self.__123[o] = (item, l)
    #self.__aminolen = [5, 8, 6, 8, 9, 10, 4, 10, 8, 8, 9, 8, 8, 8, #N
     #                  17, 7, 9, 11, 6, 7, 6, 7, 14, 0, 12, 9]

    # TODO: PYL (N CA C O CB CG CD CE NZ CH CI1 OI2 CJ NK1 CK2 CL1 CL2 CL3) ???
    self.__posdex = {  "N": 0,  "CA": 1,   "C": 2,   "O": 3,  "CB": 4,
                      "CG": 5, "CG1": 5,  "OG": 5, "OG1": 5,  "SG": 5, "SEG": 5,
                      "CD": 6, "CD1": 6, "CG2": 6, "ND1": 6, "OD1": 6,  "SD": 6,
                     "CD2": 7,  "CE": 7, "ND2": 7,  "NE": 7, "OD2": 7, "OE1": 7,
                     "CE1": 8,  "NE1": 8, "NE2": 8,  "NZ": 8, "OE2": 8,
                     "CE2": 9,  "CH": 9, "NH1": 9, "CE3": 10, "NH2": 10,
                      "CZ": 10, "CZ2": 11, "OH": 11, "CZ3": 12, "CH2": 13}

  def parse(self, data):
    title = ""
    date = None
    sequences = dict()
    models = dict()
    id_mod = -1
    for bline in data.readlines():
      line = bline.decode("utf-8")
      command = line[0:6].upper()
      if command[0:4] == "ATOM":
        if not id_mod in models:
          models[id_mod] = dict()
        self.__parse_atom(line[6:], sequences, models[id_mod])
      elif command == "HEADER":
        (title, date) = self.__parse_header(line[6:])
      elif command == "SEQRES":
        self.__parse_sequence(line[6:], sequences)
      elif command == "MODRES":
        self.__parse_modres(line[6:], sequences)
      elif command[0:5] == "MODEL":
        match = self.__re_model.match(line[6:])
        if match:
          id_mod = int(match.group(1).strip())
      elif command == "ENDMDL":
        id_mod = -1
      elif command[0:3] == "HET":
        self.__parse_heterogen(line[6:], sequences)
    data.close()
    prepared = self.__prepare_models(sequences, models)
    return (title.strip(), date, self.VERSION_CURRENT, prepared)

  def __parse_header(self, line):
    match = self.__re_header.match(line)
    if match:
      day = int(match.group(2))
      month = match.group(3).upper()
      year = 2000 + int(match.group(4))
      if year > 2050:
        year -= 100
      for (n, m) in enumerate(["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"], 1):
        if m == month:
          mon = n

      return (match.group(1), datetime(year, mon, day))

  def __parse_atom(self, line, sequences, model):
    match = self.__re_atom.match(line)
    name = match.group(1).strip().upper()
    chain = match.group(2)
    if not chain in sequences:
      return
    if not chain in model:
      model[chain] = dict()
    mod_chain = model[chain]

    (seqtype, array, _, _) = sequences[chain]
    residue = int(match.group(3).strip()) - 1
    pos = (float(match.group(4).strip()),
           float(match.group(5).strip()),
           float(match.group(6).strip()))
    if not residue in mod_chain:
      mod_chain[residue] = dict()
    if seqtype == self.__PROTEIN:
      special = False
      if array[residue] == "I" and name == "CD1":
        mod_chain[residue][7] = pos
        special = True
      if array[residue] == "H" and name == "NE2":
        mod_chain[residue][9] = pos
        special = True
      if array[residue] == "R" and name == "CZ":
        mod_chain[residue][8] = pos
        special = True
      if array[residue] != "!" and not special:
        if name in self.__posdex:
          mod_chain[residue][self.__posdex[name]] = pos

  def __parse_sequence(self, line, sequences):
    match = self.__re_sequence.match(line)
    if not match:
      return
    tag = match.group(1)
    residues = match.group(3).split(" ")
    if tag in sequences:
      (seqtype, array, nonstd, atoms) = sequences[tag]
    else:
      if len(residues[0]) == 1:
        seqtype = self.__RNA
      elif len(residues[0]) == 2:
        seqtype = self.__DNA
      else:
        seqtype = self.__PROTEIN
      array = ""
      nonstd = dict()
      atoms = 0
    for res in residues:
      if seqtype == self.__PROTEIN:
        if len(res) >= 3:
          key = res[0:3].upper()
          if key in self.__321:
            (l, a) = self.__321[key]
            array += l
            atoms += a
          else:
            array += "!"
            nonstd[len(array)] = (key, 0)
      elif seqtype == self.__DNA:
        if len(res) >= 2:
          key = res[0:2].upper()
          array += self.__dna[key]
      else:
        key = res[0].upper()
        array += self.__rna[key]
    sequences[tag] = (seqtype, array, nonstd, atoms)

  def __parse_modres(self, line, sequences):
    match = self.__re_modres.match(line)
    if not match:
      return

    mid = match.group(1).strip()
    cid = match.group(2)
    num = int(match.group(3).strip())
    res = match.group(4).strip()
    if not res in self.__321:
      return
    if not cid in sequences:
      return
    (a, array, b, atoms) = sequences[cid]
    if len(array) <= num:
      return
    sequences[cid] = (a, array[:num-1] + self.__321[res][0] + array[num:], b, atoms + self.__321[res][1])

  def __parse_heterogen(self, line, sequences):
    match = self.__re_hetero.match(line)
    if not match:
      return

    hid = match.group(1).strip()
    cid = match.group(2)
    num = int(match.group(3).strip())
    tot = int(match.group(5).strip())
    if not cid in sequences:
      return
    (_, _, nonstd, _) = sequences[cid]
    nonstd[num] = (hid, tot)

  def __prepare_models(self, sequences, models):
    binmod = dict()
    nan = float("NaN")
    for modkey in models:
      buf = BytesIO()
      # Version, # chains
      buf.write(pack("<HB", self.VERSION_CURRENT, len(sequences)))
      for seq_id in sequences:
        (c_type, chain, nonstd, tot_atoms) = sequences[seq_id]
        tot_res = len(chain)
        # chain ID, chain type, # residues, chain
        buf.write(pack("<cBH{0}s".format(tot_res),
                       seq_id.encode("UTF-8"), c_type, tot_res, chain.encode("UTF-8")))
        # heterogens
        buf.write(pack("<H", len(nonstd)))
        for position in sorted(nonstd.keys()): # 400: ('ATP', 31)
          (hetname, hetatoms) = nonstd[position]
          buf.write(pack("<H{0}sB".format(len(hetname)), len(hetname), hetname.encode("UTF-8"), hetatoms))
        # Total atoms to read
        buf.write(pack("<l", tot_atoms))
        aminos = models[modkey][seq_id]
        for i in range(0, tot_res):
          amino = chain[i]
          aminolen = self.__123[amino][1]
          if not i in aminos:
            # Fill with emtpy values
            for j in range(0, aminolen):
              buf.write(pack("fff", nan, nan, nan))
          else:
            atoms = aminos[i]
            # Fill with actual values, or empty
            for j in range(0, aminolen):
              if not j in atoms:
                buf.write(pack("fff", nan, nan, nan))
              else:
                buf.write(pack("fff", atoms[j][0], atoms[j][1], atoms[j][2]))
      buf.seek(0)
      binmod[modkey] = buf
    return binmod
        
