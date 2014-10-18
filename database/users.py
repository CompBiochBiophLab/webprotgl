""" User database wrapper """

import base64
import logging
import os

from database.user import User
from database.whirlpool import Whirlpool
from datetime import datetime, timedelta
from server.cookie import Cookie

class UserDB(object):
  """ The user table access """

  SESSION_STANDARD = 1
  SESSION_REGISTER = 3

################################################################

  def __init__(self, database):
    """
    """
    self.__database = database

################################################################

  def find_session(self, data):
    if "session" in data:
      sid = data["session"]
      cursor = self.__database.cursor()
      
      for s_row in cursor.execute("SELECT expires, type, username \
        FROM Sessions WHERE sid = ?", (sid,)):
        # Verify session type
        if s_row[1] != self.SESSION_STANDARD:
          return None

        # Verify expiration
        expires = datetime.strptime(s_row[0], "%Y-%m-%d %H:%M:%S.%f")
        if expires < datetime.now():
          cursor.execute("DELETE FROM Sessions WHERE sid = ?", (sid,))
          self.__db.commit()
          return None
        
        for row in cursor.execute( \
          "SELECT rid, username, clan, email FROM Users \
           WHERE username = ?", (s_row[2],)):
          return self.__load(row)

################################################################

  def find_user(self, data):
    if "username" in data and "password" in data:
      username = data["username"].lower()
      logging.debug(username)
      password = data["password"]
      
      cursor = self.__database.cursor()
      
      # Verify the registration was activated
      for row in cursor.execute( \
        "SELECT * FROM Sessions WHERE username = ? AND type = ?", \
        (username, self.SESSION_REGISTER)):
        logging.warning("Not activated yet")
        return (None, None)
    
      #find id + salt
      for info_row in cursor.execute("SELECT rid, salt FROM Users \
        WHERE username = ?", (username, )):
        (pwd_salt, pwd_hash) = self.__hash(info_row[1], password)
        for row in cursor.execute( \
          "SELECT rid, username, clan, email FROM Users \
          WHERE rid = ? AND password = ?", (info_row[0], pwd_hash)):
          user = self.__load(row)
          
          # Remove all existing sessions of this user
          cursor.execute("DELETE FROM Sessions WHERE username = ?", \
	    (username, ))
        
          # Create a new session
          (sid, expires) = self.__create_session(7)
          cursor.execute("INSERT INTO Sessions (sid, username, type, expires) \
                          VALUES (?, ?, ?, ?)", \
                          (sid, username, self.SESSION_STANDARD, expires))
          self.__database.commit()
          return (user, Cookie("session", "{1}".format(username, sid), \
            expires))
    
    return (None, None)

################################################################

  def __create_session(self, exp_days=0, exp_hours=0, exp_minutes=0):
    """Create a new unique ID for a session
    
    :type  exp_days: integer
    :param exp_days: Number of days to expiration
    :type  exp_hours: integer
    :param exp_hours: Number of hours to expiration
    :type  exp_minutes: integer
    :param exp_minutes: Number of minutes to expiration
    :rtype:   string
    :returns: An UID
    """
    return (base64.urlsafe_b64encode(os.urandom(36)).decode("UTF-8"), \
            datetime.now() + \
            timedelta(days=exp_days, hours=exp_hours, minutes=exp_minutes))

################################################################

  def __hash(self, salt, password):
    """Create a hash from a password
    
    :type  password: string
    :param password: The password to hash
    :rtype:   string
    :returns: An irreversible hash
    """
    # Need salt?
    if not salt:
      salt = base64.urlsafe_b64encode(os.urandom(96)).decode("UTF-8")
    return (salt, Whirlpool(salt + password).hexdigest())

################################################################

  def __load(self, row):
    """Load an Author User object
    
    :type  row: array[...]
    :param row: Author's data
    :rtype:   User
    :returns: An Author object
    """
    return User(row[0], row[1], row[2], row[3])
