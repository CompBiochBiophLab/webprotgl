

class ProteinGroup:
  def __init__(self, id = -1, name = "", protein_groups = [], proteins = set()):
    self.__id = id
    self.__name = name
    self.__protein_groups = protein_groups
    self.__proteins = proteins

  def get_name(self):
    return self.__name

  def get_proteins(self):
    proteins = self.__proteins
    for child in self.__protein_groups:
      proteins |= child.get_proteins()
    return proteins
