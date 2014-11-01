""" User database wrapper """

import base64
import logging
import os

from database.dictionary import Dictionary
from database.user import User
from database.whirlpool import Whirlpool
from datetime import datetime, timedelta
from server.cookie import Cookie
from server.async.email import Email


class UserDB(object):
  """ The user table access """

  SESSION_STANDARD = 1
  SESSION_REGISTER = 3

################################################################

  def __init__(self, database):
    """
    """
    self.__database = database
    self.__session_select = "SELECT expires, state, email FROM Sessions "
    self.__user_select = "SELECT rid, title, first_name, last_name, email FROM Users "

################################################################

  def activate(self, session_id):
    cursor = self.__database.cursor()
    logging.debug(session_id)
    for s_row in cursor.execute("SELECT expires, email FROM Sessions \
                                 WHERE eid = ? AND state = ?",
                                (session_id, self.SESSION_REGISTER)):
      # Verify expiration
      expires = datetime.strptime(s_row[0], "%Y-%m-%d %H:%M:%S.%f")
      email = s_row[1]

      logging.debug("Found session")

      cursor.execute("DELETE FROM Sessions WHERE eid = ? AND state = ?",
                    (session_id, self.SESSION_REGISTER))
      self.__database.commit()
      if expires > datetime.now():
        logging.debug("Activating " + email)
        return 0
      else:
        return 1
    return -1

################################################################

  def find_session(self, data):
    if "session" in data:
      sid = data["session"]
      cursor = self.__database.cursor()

      for s_row in cursor.execute(self.__session_select +
                                  "WHERE eid = ?", (sid,)):
        # Verify session type
        if s_row[1] != self.SESSION_STANDARD:
          return None

        # Verify expiration
        expires = datetime.strptime(s_row[0], "%Y-%m-%d %H:%M:%S.%f")
        if expires < datetime.now():
          cursor.execute("DELETE FROM Sessions WHERE eid = ?", (sid,))
          self.__db.commit()
          return None
        
        for row in cursor.execute(
                self.__user_select + "WHERE email = ?", (s_row[2],)):
          return self.__load(row)

################################################################

  def find_user(self, data):
    # Validate data
    needed = ["email", "password", "password_bis"]
    for item in needed:
      if item not in data:
        return None, None
    if data["password_bis"]:  # Attempt to keep bots at bay
      return None, None

    email = data["email"].lower()
    password = data["password"]
      
    cursor = self.__database.cursor()
      
    # Verify the registration was activated
    for row in cursor.execute(
            self.__session_select + "WHERE email = ? AND state = ?",
            (email, self.SESSION_REGISTER)):
      logging.warning("Not activated yet")
      return None, None
    
    #find id + salt
    for info_row in cursor.execute("SELECT rid, salt FROM Users \
                                    WHERE email = ?", (email, )):
      (pwd_salt, pwd_hash) = self.__hash(info_row[1], password)
      for row in cursor.execute(
              self.__user_select + "WHERE rid = ? AND password = ?",
              (info_row[0], pwd_hash)):
        user = self.__load(row)
          
        # Remove all existing sessions of this user
        cursor.execute("DELETE FROM Sessions WHERE email = ?", (email,))
        
        # Create a new session
        (sid, expires) = self.__create_session(7)
        cursor.execute(
            "INSERT INTO Sessions (eid, email, state, expires) \
             VALUES (?, ?, ?, ?)",
            (sid, email, self.SESSION_STANDARD, expires))
        self.__database.commit()

        return user, Cookie("session", "{1}".format(email, sid), expires)
    
    return None, None

################################################################

  def register(self, data):
    # Validate data
    needed = ["salutation", "first_name", "last_name", "email",
              "password", "password_bis", "captcha"]
    for item in needed:
      if item not in data:
        return False
    if data["captcha"]:  # Attempt to keep bots at bay
      return False
    if data["password"] != data["password_bis"]:
      return False

    # Hash the password
    (pwd_salt, pwd_hash) = self.__hash(None, data["password"])

    # Create a "Session" that is actually the registration link
    email = data["email"].lower()
    (sid, expires) = self.__create_session(2)
    logging.debug("Registration link for {1}: {0}".format(sid, email))

    # Try adding to db
    cursor = self.__database.cursor()

    cursor.execute("INSERT INTO Sessions (eid, email, state, expires) \
      VALUES (?, ?, ?, ?)", (sid, email, UserDB.SESSION_REGISTER, expires))
    cursor.execute("INSERT INTO Users (title, first_name, last_name, \
        email, password, salt) VALUES (?, ?, ?, ?, ?, ?)", (
        data["salutation"], data["first_name"],
        data["last_name"], email, pwd_hash, pwd_salt))

    logging.debug("Registering " + email)
    # Send an email before committing. BUT it will be on its own thread !
    mail = Email(email, Dictionary.get("mail_register_subject"))
    variables = {"__activation_link": sid}
    mail.load_body("activation", variables)
    mail.run()

    self.__database.commit()

    return True

################################################################

  @staticmethod
  def __create_session(exp_days=0, exp_hours=0, exp_minutes=0):
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
    return (base64.urlsafe_b64encode(os.urandom(36)).decode("UTF-8"),
            datetime.now() +
            timedelta(days=exp_days, hours=exp_hours, minutes=exp_minutes))

################################################################

  @staticmethod
  def __hash(salt, password):
    """Create a hash from a password
    
    :type  password: string
    :param password: The password to hash
    :rtype:   string
    :returns: An irreversible hash
    """
    # Need salt?
    if not salt:
      salt = base64.urlsafe_b64encode(os.urandom(96)).decode("UTF-8")
    return salt, Whirlpool(salt + password).hexdigest()

################################################################

  @staticmethod
  def __load(row):
    """Load an User object
    
    :type  row: array[...]
    :param row: User's fields
    :rtype:   User
    :returns: An User object
    """
    return User(row[0], row[1], row[2], row[3], row[4])
