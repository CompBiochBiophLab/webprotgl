#! /usr/bin/python3
""" REST Server for the WebGLProtein webservice """

import sys, os

__here__ = os.path.dirname(__file__)
sys.path.append(__here__)

import importlib
import logging
import traceback

from database import database
from server import post_parser, responder
from wsgiref.simple_server import make_server

class RESTServer(object):
  """ The rest server itself """

################################################################

  def __init__(self):
    """ Initialise servers, regexes """
    logging.basicConfig(filename=os.path.join(__here__, "webglprotein.log"), \
      level=logging.DEBUG)
    
    self.__root = "/"
    self.__db = database.Database(os.path.join(__here__, "webglprotein.db"))
    self.__server = responder.Responder("http", "localhost", self.__root, 8080)

################################################################

  def __call__(self, env, start_response):
    """ Entry point """
    response = responder.Response()
    
    # First' check for session cookie
    try:
      database = self.__db.connect()
      user = None
      if "HTTP_COOKIE" in env:
        #print(env["HTTP_COOKIE"])
        args = post_parser.parse(data = env["HTTP_COOKIE"])
        if args:
        #cookie = cookie.Cookie(client_string = env["HTTP_COOKIE"])
          user = database.users().find_session(args)
        print(user)
      
      # Check there is a valid path
      path = env["PATH_INFO"]
      if path[0:len(self.__root)] != self.__root:
        print("Can't handle this path!")
        response.set_status_code(400)
        return
        
      path = path[len(self.__root):]
      path = path.split("/")

      # Special paths: "", "favicon.ico", "sitemap.xml", "robots.txt"
      if path == [""]:
        response.set_body("<html><body>Index.html</body></html>", "text/html")
        return
      
      try:
        logging.debug("Now serving " + str(path))
        module = importlib.import_module("server." + path[0])
        factory = getattr(module, path[0].title())
        server = factory()
        response = server.serve(env, path, user, database)
      finally:
        pass

    except Exception as exc:
      logging.error("Exception in main: " + str(exc))
      logging.error(traceback.format_exc())
      logging.error("--------")
    finally:
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

