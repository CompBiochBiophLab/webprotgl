""" Thread to email a (group of) user(s)
"""

import logging
import os
import smtplib
import traceback

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from threading import Thread

class Email():
  def __init__(self, recipient, subject, body="", attachments=None):
    if isinstance(recipient, str):
      self.__recipients = [recipient]
    else:
      self.__recipients = recipient
    self.__subject = subject
    self.__body = body
    self.__attachments = attachments

  def run(self):
    logging.debug("Sending email to " + str(self.__recipients))

    # TODO: Copy to sent messages ! OR Send to Bcc !
    try:
      mail = smtplib.SMTP("localhost", 25)
      mail.ehlo()
      mail.starttls()
      mail.login("test", "test")
      sender = "test@jrenggli.com"
      for address in self.__recipients:
        if not self.__attachments:
          msg = MIMEText((self.__body))
        else:
          msg = MIMEMultipart()
          msg.attach(MIMEText((self.__body)))
          assert(False)

        msg["From"] = sender
        msg["To"] = address
        msg["Subject"] = self.__subject
        mail.sendmail(sender, [address], msg.as_string())
      mail.quit()
    except Exception as exc:
      # Write failure to DB
      logging.error("Exception in Email: " + str(exc))
      logging.error(traceback.format_exc())

m = Email("test@jrenggli.com", "Test", "Again")
m.run()
