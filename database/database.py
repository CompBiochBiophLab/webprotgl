
from cache import DBCache
from datetime import datetime
from io import BytesIO
from protein import Protein
from source import Source
from user import User
import cPickle
import sqlite3

class DBBlob(object):
  ''' automatic converter for BytesIO'''
  def __init__(self, bytes): self.__bytes = bytes

  def quote(self):
    return "'%s'" % sqlite.encode(self.__bytes)

class Database:
  def __init__(self, strCnx = "database.sqlite"):
    self.__db = sqlite3.connect(strCnx)
    self.__cache = DBCache()
    self.__type_to_mime = {"pdb": "text/pdb"}

################################################################

  def add_source(self, sourcename, basetype, url, description):
    """Add a source if not exists; returns the source whether added or existent"""
    name = sourcename.lower()
    mime = self.__type_to_mime[basetype.lower()]
    source = self.__cache.find_source(name, mime)
    if source:
      return source

    c = self.__db.cursor()
    c.execute("INSERT INTO Sources (name, mimetype, url, description) VALUES (?,?,?,?)", (name, mime, url, description))
    self.__db.commit()
    source = Source(c.lastrowid, name, mime, url, description)
    self.__cache.add_source(name, mime, source)
    return source

################################################################

  def add_user(self, username, email, pwdhash):
    name = username.lower()
    if self.__users.has_key(name):
      raise Exception("User already exists")

    c = self.__db.cursor()
    c.execute("INSERT INTO Users (name, email, passwd) VALUES (?,?,?)", (name, email, pwdhash))
    self.__db.commit()
    user = User(c.lastrowid, name, email, pwdhash)
    self.__users[name] = user
    return user

################################################################

  def close(self):
    self.__db.close()

################################################################

  def find_source(self, sourcename, basetype):
    name = sourcename.lower()
    mime = self.__type_to_mime[basetype.lower()]
    source = self.__cache.find_source(name, mime)
    if source:
      return source

    # Lookup in db?
    return None

################################################################

  def get_protein_info(self, source, protein_name):
    if not isinstance(source, Source):
      raise Exception("Not a source")

    # Verify if already exists
    name = protein_name.upper()
    sid = source.get_id()
    protein = self.__cache.find_protein(name, sid)
    if protein:
      return protein

    # Load from DB???

    # Create new protein by downloading one
    protein = self.__add_protein(source, name)
    return protein

################################################################

  def load(self):
#    self.__groups = dict()
#    self.__users = dict()
#    self.__sources = dict()
#    self.__proteins = dict()

    c = self.__db.cursor()

    c.execute("CREATE TABLE IF NOT EXISTS Groups (gid INTEGER, name TEXT, children BLOB, CONSTRAINT group_pk PRIMARY KEY(gid))")
    c.execute("CREATE TABLE IF NOT EXISTS Users (uid INTEGER, name TEXT, email TEXT, passwd BLOB, CONSTRAINT user_pk PRIMARY KEY(uid), CONSTRAINT user_uname UNIQUE(name))")
    c.execute("CREATE TABLE IF NOT EXISTS Sources (sid INTEGER PRIMARY KEY, name TEXT, mimetype TEXT, url TEXT, description TEXT, CONSTRAINT source_unique UNIQUE (name, mimetype))")
    c.execute("CREATE TABLE IF NOT EXISTS Proteins (pid INTEGER PRIMARY KEY, name TEXT, title TEXT, sid INTEGER, date DATETIME, CONSTRAINT protein_unique UNIQUE (name, sid))")
    c.execute("CREATE TABLE IF NOT EXISTS Models (pid INTEGER, model INTEGER, data BLOB, CONSTRAINT model_pk PRIMARY KEY (pid, model))")
    self.__db.commit()

    for (uid, name, email, pwd) in c.execute("SELECT uid, name, email, passwd FROM Users"):
      self.__users[name] = User(uid, name, email, pwd)

    for (sid, name, mime, url, desc) in c.execute("SELECT sid, name, mimetype, url, description FROM Sources"):
      self.__cache.add_source(name, mime, Source(sid, name, mime, url, desc))

    for (pid, name, title, sid, date) in c.execute("SELECT pid, name, title, sid, date FROM Proteins"):
      ids = set()
      for mid in c.execute("SELECT model FROM Models WHERE pid=?", (pid,)):
        ids.add(mid[0])
      self.__cache.add_protein(name, sid, Protein(pid, name, title, sid, datetime.strptime(date, "%Y-%m-%dT%H:%M:%S"), ids))

################################################################

  def load_model(self, protein, mid):
    if not isinstance(protein, Protein):
      raise Exception("Not a protein")
    c = self.__db.cursor()
    for model in c.execute("SELECT data FROM Models WHERE pid=? AND model=?", (protein.get_id(), mid)):
      return BytesIO(str(model[0]))

################################################################

  def __add_protein(self, source, name):
    sid = source.get_id()
    (title, date, models) = source.fetch(name)

    c = self.__db.cursor()
    c.execute("INSERT INTO Proteins (name, title, sid, date) VALUES (?,?,?,?)", (name, title, sid, date.isoformat()))
    pid = c.lastrowid
    ids = set()
    for mid in models:
      c.execute("INSERT INTO Models (pid, model, data) VALUES (?,?,?)", (pid, mid, sqlite3.Binary(models[mid].getvalue())))
      ids.add(mid)
    self.__db.commit()
    protein = Protein(pid, name, title, sid, date, ids)
    self.__cache.add_protein(name, sid, protein)
    return protein

