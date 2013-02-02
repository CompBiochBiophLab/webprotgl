

from datetime import datetime
from protein import Protein
from source import Source
from user import User
import sqlite3

class Database:
  def __init__(self, strCnx = "database.sqlite"):
    self.__db = sqlite3.connect(strCnx)
    self.__groups = dict()
    self.__proteins = dict()
    self.__sources = dict()
    self.__users = dict()

  def add_protein(self, protein_name, title, source_id, date):
    name = protein_name.upper()
    if self.__proteins.has_key(name):
      raise Exception("Protein already exists")

    c = self.__db.cursor()
    c.execute("INSERT INTO Proteins (name, title, sid, date) VALUES (?,?,?,?)", (name, title, source_id, date.isoformat()))
    self.__db.commit()
    protein = Protein(c.lastrowid, name, title, source_id, date)
    self.__proteins[name] = protein
    return protein

  def add_source(self, sourcename, mimetype, url, description):
    name = sourcename.lower()
    if self.__sources.has_key((name, mimetype)):
      raise Exception("Source already exists")

    c = self.__db.cursor()
    c.execute("INSERT INTO Sources (name, mimetype, url, description) VALUES (?,?,?,?)", (name, mimetype, url, description))
    self.__db.commit()
    source = Source(c.lastrowid, name, mimetype, url, description)
    self.__sources[(name, mimetype)] = source
    return source

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

  def close(self):
    self.__db.close()

  def load(self):
    self.__groups = dict()
    self.__users = dict()
    self.__sources = dict()
    self.__proteins = dict()

    c = self.__db.cursor()

    c.execute("CREATE TABLE IF NOT EXISTS Groups (gid INTEGER, name TEXT, children BLOB, CONSTRAINT group_pk PRIMARY KEY(gid))")
    c.execute("CREATE TABLE IF NOT EXISTS Users (uid INTEGER, name TEXT, email TEXT, passwd BLOB, CONSTRAINT user_pk PRIMARY KEY(uid), CONSTRAINT user_uname UNIQUE(name))")
    c.execute("CREATE TABLE IF NOT EXISTS Sources (sid INTEGER PRIMARY KEY, name TEXT, mimetype TEXT, url TEXT, description TEXT, CONSTRAINT source_unique UNIQUE (name, mimetype))")
    c.execute("CREATE TABLE IF NOT EXISTS Proteins (pid INTEGER PRIMARY KEY, name TEXT, title TEXT, sid INTEGER, date DATETIME)")
    c.execute("CREATE TABLE IF NOT EXISTS Models (pid INTEGER, model INTEGER, data BLOB, CONSTRAINT model_pk PRIMARY KEY (pid, model))")
    self.__db.commit()

    for (uid, name, email, pwd) in c.execute("SELECT uid, name, email, passwd FROM Users"):
      self.__users[name] = User(uid, name, email, pwd)

    for (sid, name, mime, url, desc) in c.execute("SELECT sid, name, mimetype, url, description FROM Sources"):
      self.__sources[(name, mime)] = Source(sid, name, mime, url, desc)

    for (pid, name, title, sid, date) in c.execute("SELECT pid, name, title, sid, date FROM Proteins"):
      self.__proteins[name] = Protein(pid, name, title, sid, datetime.strptime(date, "%Y-%m-%dT%H:%M:%S.%f"))

