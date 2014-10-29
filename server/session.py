""" Serve session management """

import logging
#import mimetypes
#import os
#import traceback

from server import post_parser, responder
from server.html import html_format_file

class Session(object):
  def __init__(self):
    pass

  def serve(self, env, path, user, database):
    response = responder.Response()

    method = env["REQUEST_METHOD"]
    if method == "GET":
      response.set_body(html_format_file("session_" + path[1]), "text/html")
      logging.debug(path[1])

    return response

  def __serve_html(self, protein_name, response):
    response.set_body(html_format_file("protein", protein_name.upper()), "text/html")
    return response