""" Serve session management """

import logging

from database.dictionary import Dictionary
from server import post_parser, responder
from server.html import html_format_file
from server.post_parser import parse

class Session(object):
  def __init__(self):
    pass

  def serve(self, env, path, user, database):
    method = env["REQUEST_METHOD"]
    response = responder.Response()

    if method == "GET":
      response.set_body(html_format_file("session/" + path[1]), "text/html")
    elif method == "POST":
      fun = getattr(self, path[1])
      if fun:
        response = fun(env, path, user, database)
    else:
      response.set_status_code(405) # Method Not Allowed
    return response

  def register(self, env, path, user, database):
    response = responder.Response()
    if user:
      response.set_status_code(409) # Conflict
      return response

    data = parse(env)
    if database.users().register(data):
      response.set_redirect(Dictionary.format( \
        "{_root_}/{_session_}/{_registered_}"))
    return response