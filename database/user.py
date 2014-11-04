""" A user """

from database.user_group import UserGroup


class User(object):
  def __init__(self, user_id, title, first_name, last_name, email):
    self.__id = user_id
    self.__title = title
    self.__first_name = first_name
    self.__last_name = last_name
    self.__email = email
    self.__groups = None
    #self.__pseudo_group = UserGroup(-1, "", groups)

  def email(self):
    return self.__email

  def get_name(self, fmt="{0} {1}"):
    return fmt.format(self.__first_name, self.__last_name)

  def get_proteins(self):
    return self.__pseudo_group.get_proteins()

