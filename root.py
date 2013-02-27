#! /usr/bin/python

import sys

sys.path.append("var/www/webglprotein/")

#import os
#import mimetypes
#from paste import httpserver
import re
#from webob import Request, Response
#from server.static import StaticServer
from server.protein import ProteinServer
from wsgiref.simple_server import make_server

#def application(env, start_response):
#  res = None
#  server = ProteinServer()
#  res = server.serve(env, start_response)
#  if res:
#    return res
#  else:
#    body = "Hello server"
#    start_response("200 OK", [("Content-Type", "text/plain"),
#                              ("Content-Length", str(len(body)))])
#    return ["Hello server"]
#
#httpd = make_server("localhost", 8051, application)
#httpd.handle_request()

class RESTServer():
  def __init__(self):
    self.__routes = []
#    self.__routes.append((re.compile("/static/.+"), StaticServer()))
    self.__routes.append((re.compile("/protein/\\w+/\\w+/\\w+"), ProteinServer()))

  def __call__(self, env, start_response):
    res = None
    for (rx, fn) in self.__routes:
      if (rx.match(env["PATH_INFO"])):
        res = fn.serve(env, start_response)
        break
    if res:
      return res
    start_response("404 Not found", [("Content-Type", "text/html")])
    return ["<html><body><h1>404 - Not found</h1></body></html>"]

  def serve(self, env, start_response):
    return self.__call__(env, start_response)

def application(env, start_response):
  server = RESTServer()
  return server.serve(env, start_response)

if __name__ == "__main__":
  httpd = make_server("localhost", 8051, RESTServer())
  httpd.handle_request()

#if __name__ == "__main__":
#  httpserver.serve(RESTServer(), host="192.168.2.128", port=8080)

