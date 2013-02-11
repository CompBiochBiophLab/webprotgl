#! /usr/bin/python

import os
import mimetypes
from paste import httpserver
import re
from webob import Request, Response
from server.static import StaticServer
from server.protein import ProteinServer

class RESTServer():
  def __init__(self):
    self.__routes = []
    self.__routes.append((re.compile("/static/.+"), StaticServer()))
    self.__routes.append((re.compile("/protein/\\w+/\\w+/\\w+"), ProteinServer()))

  def __call__(self, env, start_response):
    res = None
    for (rx, fn) in self.__routes:
      if (rx.match(env["PATH_INFO"])):
        res = fn.serve(env, start_response)
        break
    if res:
      return res
    start_response("200 OK", [("Content-Type", "text/html")])
    return ["Hello router"]

if __name__ == "__main__":
  httpserver.serve(RESTServer(), host="192.168.2.128", port=8080)

