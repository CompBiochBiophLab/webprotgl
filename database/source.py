
from urllib.request import urlopen
from .pdb_parser import PDBParser

class Source:
  def __init__(self, id = -1, name = "", mimetype="", url="", description=""):
    self.__id = id
    self.__name = name
    if mimetype == PDBParser.MIMETYPE:
      self.__parser = PDBParser()
    else:
      self.__parser = None

    self.__url = url
    self.__desc = description

  def fetch(self, protein_name):
    if self.__parser == None: #if not isinstance(parser, Parser):
      raise Exception("No parser set")

    url = self.get_url(protein_name)
    return self.__parser.parse(urlopen(url))
#    (title, date, structure, models) = parser.parse(urlopen(url))
#    print(structure)
#    return Protein(-1, name, title, source, date)

  def get_id(self):
    return self.__id

  def get_name(self):
    return self.__name

  def get_parser(self):
    return self.__parser

  def get_url(self, protein_name):
    if self.__url == "":
      raise Exception("Source URL not set")

    return self.__url.format(protein_name)

