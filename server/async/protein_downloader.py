""" Thread to download a given protein
"""

import logging
import sqlite3
import time
import traceback

from database.pdb_parser import PDBParser
from datetime import datetime
from threading import Thread

class ProteinGetter(Thread):
  def __init__(self, database, source, protein_name):
    Thread.__init__(self)
    # 1st clone: still in same thread? But avoids problems with closing behind the scenes ?
    self.__database = database.clone(True)
    # # MUST immediately close... that's ok
    # self.__database.close()
    self.__source = source
    self.__protein = protein_name

  def run(self):
    logging.debug("Get protein " + str(self.__source.get_id()) + " / " + self.__protein)

    # 2nd clone: really in this thread !?
    self.__database = self.__database.clone()

    try:
      cursor = self.__database.cursor()

      # Check state in DB
      for row in cursor.execute("SELECT pid, name, title, sid, date, model_date \
                                 FROM Proteins WHERE sid = ? AND name = ?", \
                               (self.__source.get_id(), self.__protein)):
        logging.info("Duplicate thread detected for " + str(self.__source.get_id()) + " / " + self.__protein)
        return

      # Set state (processing) in DB
      now = datetime.now()
      cursor.execute("INSERT INTO Proteins (name, sid, date) \
                      VALUES (?, ?, ?)", \
                     (self.__protein, self.__source.get_id(), now))
      pid = cursor.lastrowid
      self.__database.commit()

      # Fetch the file if exists
      try:
        (title, date, structure, models) = self.__source.fetch(self.__protein)
        if not date:
          date = now

        # Write to DB
        cursor = self.__database.cursor()
        cursor.execute("UPDATE Proteins SET title = ?, model_date = ? \
                        WHERE pid = ?", (title, date, pid))
        for mid in models:
          cursor.execute("INSERT INTO Models (pid, model, version, date, data) \
                          VALUES (?, ?, ?, ?, ?)", \
                        (pid, mid, PDBParser.VERSION_CURRENT, \
                         date, sqlite3.Binary(models[mid].getvalue())))

        self.__database.commit()
      except Exception as exc:
        # Mark as failed to process rather than processing
        logging.error("Exception in ProteinGetter: " + str(exc))
        logging.error(traceback.format_exc())
        logging.error("Incomplete " + str(self.__source.get_id()) + " / " + self.__protein)
        cursor = self.__database.cursor()
        cursor.execute("UPDATE Proteins SET model_date = ? \
                        WHERE pid = ?", (now, pid))
        self.__database.commit()

      logging.debug("Done with " + str(self.__source.get_id()) + " / " + self.__protein)
    except Exception as exc:
      # Write failure to DB
      logging.error("Exception in ProteinGetter: " + str(exc))
      logging.error(traceback.format_exc())
      logging.error("Failed with " + str(self.__source.get_id()) + " / " + self.__protein)
    finally:
      self.__database.close()