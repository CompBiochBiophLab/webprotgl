""" Protein database wrapper """

# import base64
# import logging
# import os
#
from database.protein import Protein
from database.source import Source
# from database.whirlpool import Whirlpool
# from datetime import datetime, timedelta
# from server.cookie import Cookie
#
class ProteinDB(object):
  """ The protein table access """
#
#   SESSION_STANDARD = 1
#   SESSION_REGISTER = 3

################################################################

  def __init__(self, database):
    """
    """
    self.__database = database

################################################################

  def find_source(self, sourcename, basetype):
    cursor = self.__database.cursor()
    for row in cursor.execute("SELECT sid, name, mimetype, url, description \
                               FROM Sources WHERE name = ? AND mimetype = ?", \
                              (sourcename.lower(), basetype.lower())):
      return Source(row[0], row[1], row[2], row[3], row[4])

    return None

################################################################

  def get_protein_info(self, source, protein_name):
    if not isinstance(source, Source):
      raise Exception("Not a source")

    name = protein_name.lower()

    # Search in DB
    cursor = self.__database.cursor()
    for row in cursor.execute("SELECT pid, name, title, sid, date, model_date \
                               FROM Proteins WHERE sid = ? AND name = ?", \
                              (source.get_id(), name)):
      protein = Protein(row[0], row[1], row[2], source, row[4], row[5])

      for row2 in cursor.execute("SELECT model FROM Models WHERE pid = ?", \
                                 (protein.get_id(),)):
        protein.add_model(row2[0])

      return protein

    return None

################################################################

  def load_model(self, protein, mid):
    if not isinstance(protein, Protein):
      raise Exception("Not a protein")

    c = self.__database.cursor()
    for model in c.execute("SELECT data FROM Models WHERE pid=? AND model=?", (protein.get_id(), mid)):
      return model[0]
