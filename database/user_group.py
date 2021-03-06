

class UserGroup:
  def __init__(self, id = -1, name = "", parent_groups = {}, protein_groups = []):
    self.__id = id
    self.__name = name
    self.__parents = parent_groups
    self.__proteins = protein_groups

  def get_name(self):
    return self.__name

  def get_proteins(self):
    proteins = dict()
    for group in self.__parents:
      parent_proteins = group.get_proteins()
      for protein in parent_proteins:
        perm = parent_proteins[protein]
        if proteins.has_key(protein):
          proteins[protein] |= perm
        else:
          proteins[protein] = perm
    for (group, perm) in self.__proteins:
      for protein in group.get_proteins():
        if proteins.has_key(protein):
          proteins[protein] |= perm
        else:
          proteins[protein] = perm
    return proteins

