
from .pdb_parser import PDBParser
from .source import Source

class Protein:
  def __init__(self, id = -1, name = "", title = "", source = None, \
               date = -1, model_date = "", models = set()):
    self.__id = id
    self.__name = name
    self.__title = title
    self.__source = source
    self.__date = date
    self.__model_date = model_date
    self.__models = models

  def add_model(self, model_id):
    self.__models.add(model_id)

  def get_id(self):
    return self.__id

  def get_models(self):
    return self.__models

  def get_name(self):
    return self.__name

  def is_processing(self):
    return not self.__model_date

  def set_source(self, source):
    self.__source = source
