
from user_group import UserGroup

class User:
  def __init__(self, id = -1, name = "", email = "", pwdhash = -1, groups = {}):
    self.__id = id
    self.__name = name
    self.__email = email
    self.__hash = pwdhash
    self.__pseudo_group = UserGroup(-1, "", groups)

  def get_name(self):
    return self.__name

  def get_proteins(self):
    return self.__pseudo_group.get_proteins()

  def validate(self, pwhash):
    return self.__hash == pwhash
