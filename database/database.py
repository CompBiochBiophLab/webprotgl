""" Database wrapper """

import os
import sqlite3

from database.proteins import ProteinDB
from database.users import UserDB

# class DBBlob(object):
#   ''' automatic converter for BytesIO'''
#   def __init__(self, bytes): self.__bytes = bytes
#
#   def quote(self):
#     return "'%s'" % sqlite.encode(self.__bytes)

class Connected(object):
  def __init__(self, db_path):
    self.__filepath = db_path
    self.__database = sqlite3.connect(db_path, \
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
    :param root: Database file path
    """
    self.__filepath = filepath
    self.__users = None

################################################################

  # def clone(self):
  #   return Connected(self.__filepath)

################################################################

  def connect(self):
    return Connected(self.__filepath)

################################################################

#   def add_source(self, sourcename, basetype, url, description):
#     """Add a source if not exists; returns the source whether added or existent"""
#     name = sourcename.lower()
#     mime = self.__type_to_mime[basetype.lower()]
#     source = self.__cache.find_source(name, mime)
#     if source:
#       return source
#
#     c = self.__db.cursor()
#     c.execute("INSERT INTO Sources (name, mimetype, url, description) VALUES (?,?,?,?)", (name, mime, url, description))
#     self.__db.commit()
#     source = Source(c.lastrowid, name, mime, url, description)
#     self.__cache.add_source(name, mime, source)
#     return source

# ################################################################
#
#   def load(self):
#     c = self.__db.cursor()
#     d = self.__db.cursor()
#
#     c.execute("CREATE TABLE IF NOT EXISTS Groups (gid INTEGER, name TEXT, children BLOB, CONSTRAINT group_pk PRIMARY KEY(gid))")
#     c.execute("CREATE TABLE IF NOT EXISTS Users (uid INTEGER, name TEXT, email TEXT, passwd BLOB, CONSTRAINT user_pk PRIMARY KEY(uid), CONSTRAINT user_uname UNIQUE(name))")
#     c.execute("CREATE TABLE IF NOT EXISTS Sources (sid INTEGER PRIMARY KEY, name TEXT, mimetype TEXT, url TEXT, description TEXT, CONSTRAINT source_unique UNIQUE (name, mimetype))")
#     c.execute("CREATE TABLE IF NOT EXISTS Proteins (pid INTEGER PRIMARY KEY, name TEXT, title TEXT, sid INTEGER, model_date DATETIME, date DATETIME, CONSTRAINT protein_unique UNIQUE (name, sid))")
#     c.execute("CREATE TABLE IF NOT EXISTS Models (pid INTEGER, model INTEGER, version INTEGER, date DATETIME, data BLOB, CONSTRAINT model_pk PRIMARY KEY (pid, model))")
#     self.__db.commit()
#
#     for (uid, name, email, pwd) in c.execute("SELECT uid, name, email, passwd FROM Users"):
#       self.__users[name] = User(uid, name, email, pwd)
#
#     for (sid, name, mime, url, desc) in c.execute("SELECT sid, name, mimetype, url, description FROM Sources"):
#       self.__cache.add_source(name, mime, Source(sid, name, mime, url, desc))
#
#     c.execute("SELECT pid, name, title, sid, date FROM Proteins")
#     for (pid, name, title, sid, date) in c.execute("SELECT pid, name, title, sid, date FROM Proteins"):
#       ids = set()
#       for mid in d.execute("SELECT model FROM Models WHERE pid=?", (pid,)):
#         ids.add(mid[0])
#       self.__cache.add_protein(name, sid, Protein(pid, name, title, sid, datetime.strptime(date, "%Y-%m-%dT%H:%M:%S.%f"), ids))
#