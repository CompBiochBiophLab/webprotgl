""" Thread to email a (group of) user(s)
"""

import logging
import os
import smtplib
import traceback

# from datetime import datetime
from database.dictionary import Dictionary
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from threading import Thread


class Email(Thread):
    def __init__(self, recipient, translator, subject_key, body="", attachments=None):
        Thread.__init__(self)
        if isinstance(recipient, str):
            self.__recipients = [recipient]
        else:
            self.__recipients = recipient
        self.__subject = translator.get(subject_key)
        self.__body = body
        self.__attachments = attachments
        self.__translator = translator

    def load_body(self, file, var=None):
        with open(os.path.join(os.environ["WORKDIR"], "templates", "mail",
                               file + ".txt"), "r") as body:
            self.__body = self.__translator.format(body.read(), var)
            body.close()

    def run(self):
        logging.debug("Sending email to " + str(self.__recipients))

        # TODO: Copy to sent messages ! OR Send to Bcc !
        try:
            mail = smtplib.SMTP(self.__translator.get("_email_server_"),
                                self.__translator.get("_email_port_"))
            mail.ehlo()
            mail.starttls()
            mail.login(self.__translator.get("_email_login_"),
                       self.__translator.get("_email_password_"))
            sender = self.__translator.get("_email_sender_")
            for address in self.__recipients:
                if not self.__attachments:
                    msg = MIMEText((self.__body))
                else:
                    msg = MIMEMultipart()
                    msg.attach(MIMEText((self.__body)))
                    assert False

                msg["From"] = sender
                msg["To"] = address
                msg["Subject"] = self.__subject
                mail.sendmail(sender, [address], msg.as_string())
            mail.quit()
        except Exception as exc:
            # Write failure to DB
            logging.error("Exception in Email: " + str(exc))
            logging.error(traceback.format_exc())