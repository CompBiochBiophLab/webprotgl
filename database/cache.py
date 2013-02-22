
class DBCache:
  __PROTEIN = 0
  __SOURCE  = 1

  def __init__(self):
    self.__map = dict()

  def add_protein(self, name, sid, protein):
    if self.__map.has_key((self.__PROTEIN, name, sid)):
      raise Exception("Protein already in cache")
    self.__map[(self.__PROTEIN, name, sid)] = protein

  def add_source(self, name, mime, source):
    if self.__map.has_key((self.__SOURCE, name, mime)):
      raise Exception("Source already in cache")
    self.__map[(self.__SOURCE, name, mime)] = source

  def find_protein(self, name, sid):
    if self.__map.has_key((self.__PROTEIN, name, sid)):
      return self.__map[(self.__PROTEIN, name, sid)]
    return None

  def find_source(self, name, mime):
    if self.__map.has_key((self.__SOURCE, name, mime)):
      return self.__map[(self.__SOURCE, name, mime)]
    return None
