""" Database wrapper """

import sqlite3

from database.proteins import ProteinDB
from database.users import UserDB

class Connected(object):
  def __init__(self, db_path):
    self.__filepath = db_path
    self.__database = sqlite3.connect(db_path,
        detect_types = sqlite3.PARSE_COLNAMES)

  def clone(self, shallow=False):
    assert(self.__database)
    clone = Connected(self.__filepath)
    if shallow:
      clone.close() # :( But thread-safety first!
    return clone

  def close(self):
    assert(self.__database)
    self.__database.close()

  def commit(self):
    self.__database.commit()

  def cursor(self):
    return self.__database.cursor()

  def proteins(self):
    assert(self.__database)
    return ProteinDB(self.__database)

  def users(self):
    assert(self.__database)
    return UserDB(self.__database)

################################################################

class Database(object):
  def __init__(self, filepath):
    """Connect to the database file, prepare queries
    
    :type  filepath: string
    """
    self.__filepath = filepath
    self.__users = None

################################################################

  def connect(self):
    return Connected(self.__filepath)

################################################################
