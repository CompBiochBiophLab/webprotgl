
import StringIO

from database.pdb_parser import PDBParser
from database.protein import Protein
from database.source import Source

class ProteinTests:
  def __init__(self):
    self.__rcsb = Source(1, "rcsb", "text/pdb", "http://www.rcsb.org/pdb/download/downloadFile.do?fileFormat=pdb&compression=NO&structureId={0}", "RCSB Protein Data Bank")
    self.__protein = Protein()

  def test_parsers(self):
    pdb = PDBParser()
    pdb.parse(open("tests/3M3N", "r"))
  def test_prepare(self):
    self.__protein.set_source(self.__rcsb)
    self.__protein.fetch("3M3N")

test = ProteinTests()
test.test_parsers()
#test.test_prepare()
