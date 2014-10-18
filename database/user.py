""" A user """

from database.user_group import UserGroup

class User(object):
  def __init__(self, id, username, name, email):
    self.__id = id
    self.__name = name
    self.__email = email
    self.__pseudo_group = UserGroup(-1, "", groups)

  def get_name(self):
    return self.__name

  def get_proteins(self):
    return self.__pseudo_group.get_proteins()

