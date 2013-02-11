#! /usr/bin/python

from webob import Request
from paste import httpserver

def application(environ, start_response):
  start_response("200 OK", [("Content-Type", "text/html")])
  path = environ["PATH_INFO"].split("/")
  print(path)
  return ["Hello World!"]

if __name__ == "__main__":
  httpserver.serve(application, host="127.0.0.1", port=8080)
#req = Request.blank("http://localhost/test")
#resp = req.get_response(application);

