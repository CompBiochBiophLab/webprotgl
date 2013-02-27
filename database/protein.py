
from .pdb_parser import PDBParser
from .source import Source

class Protein:
  def __init__(self, id = -1, name = "", title = "", source = None, date = -1, models = set()):
    self.__id = id
    self.__name = name
    self.__title = title
    self.__source = source
    self.__date = date
    self.__models = models

  def get_id(self):
    return self.__id

  def get_models(self):
    return self.__models

  def get_name(self):
    return self.__name

  def set_source(self, source):
    self.__source = source
