#! /usr/bin/python3
""" REST Server for the WebGLProtein webservice """

import sys, os

__here__ = os.path.dirname(__file__)
sys.path.append(__here__)

import importlib
import logging
import traceback

from database.database import Database
from database.dictionary import Dictionary
from server import html, post_parser, responder
from wsgiref.simple_server import make_server

os.environ["WORKDIR"] = __here__
dictionary = Dictionary(os.path.abspath(os.path.join(__here__, "dict.pickle")))

class RESTServer(object):
  """ The rest server itself """

################################################################

  def __init__(self):
    """ Initialise servers, regexes """
    logging.basicConfig(filename=os.path.join(__here__, "webglprotein.log"),
        level=logging.DEBUG)

    self.__db = Database(os.path.join(__here__, "webglprotein.db"))
    self.__server = responder.Responder()

################################################################

  def __call__(self, env, start_response):
    """ Entry point """
    user = None
    response = responder.Response()
    
    # First' check for session cookie
    try:
      database = self.__db.connect()
      if "HTTP_COOKIE" in env:
        args = post_parser.parse(data=env["HTTP_COOKIE"])
        if args:
        #cookie = cookie.Cookie(client_string = env["HTTP_COOKIE"])
          user = database.users().find_session(args)
        logging.debug(user)
      
      # # Check there is a valid path
      # path = env["PATH_INFO"]
      # if path[0:len(self.__root)] != self.__root:
      #   logging.error("Can't handle this path!")
      #   response.set_status_code(response.BAD_REQUEST)
      #   return

      path = env["PATH_INFO"][1:].split("/")

      # Special paths: "", "favicon.ico", "sitemap.xml", "robots.txt"
      special = ["favicon.ico", "sitemap.xml", "robots.txt"]
      if len(path) == 1 and path[0] in special:
        path.append(path[0])
        path[0] = "static"
        # if not path[1]:
        #   path[1] = "index.html"
        # if path[1].endswith(".html"):
        #   response.set_body(html_format_file("protein", protein_name.upper()), "text/html")
        #   return response
      
      try:
        logging.debug("Now serving " + str(path))

        if len(path) == 1:
          if not path[0]:
            path[0] = "index.html"
          if path[0].endswith(".html"):
            response.set_html(path[0], user)
        else:
          module = importlib.import_module("server." + path[0])
          factory = getattr(module, path[0].title())
          server = factory()
          response = server.serve(env, path, user, database)
          assert(response)
      finally:
        pass

    except Exception as exc:
      logging.error("Exception in main: " + str(exc))
      logging.error(traceback.format_exc())
      logging.error("--------")
    finally:
      response.finalise(user)
      logging.debug(response.get_status_code())
      if database:
        database.close()
      return self.__server.serve(start_response, response)

################################################################

def application(env, start_response):
  """ WSGI "main" """
  server = RESTServer()
  return server.__call__(env, start_response)

################################################################

if __name__ == "__main__":
  """ Running from command line, no Apache """
  httpd = make_server("", 8080, RESTServer())
  print("What is thy bidding my master?")
  httpd.serve_forever()

