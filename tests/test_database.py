#! /usr/bin/python -m tests.test_database

from database.database import Database
from database.source import Source
from datetime import datetime

import bcrypt
import os
import sqlite3

class DatabaseTests:
  def __init__(self):
    db = "test.db"
    os.remove(db)
    self.__db = Database(db)
    self.__db.load()

    failures = 0
    try:
      self.__db.add_user("jrenggli", "jrenggli@gmail.com", 42)
      self.__db.add_user("yschaerli", "yschaerli@crg.eu", 8383)
      self.__db.add_user("jreNggli", "jrenggli@gmail.com", 28482)
    except sqlite3.IntegrityError:
      assert(False)
    except Exception:
      failures += 1
    finally:
      assert(failures == 1)

    src = None
    try:
      src = self.__db.add_source("RCSB", "text/pdb", "http://www.rcsb.org/pdb/download/downloadFile.do?fileFormat=pdb&compression=NO&structureId={0}", "RCSB Protein Data Bank")
    except sqlite3.IntegrityError, e:
      assert(False)
    except Exception, e:
      failures += 1
      assert(False)
    finally:
      assert(failures == 1)
 
    try:
      self.__db.add_protein("3m3n", "Test protein", src.get_id(), datetime.now())
    except sqlite3.IntegrityError, e:
      assert(False)
    except Exception, e:
      failures += 1
      assert(False)
    finally:
      assert(failures == 1)
    
    self.__db.close()

#  def users(self):
#    self.

tests = DatabaseTests()
