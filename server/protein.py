#! /usr/bin/python

from database.pdb_parser import PDBParser
from webob.response import Response

class ProteinServer():
  def __init__(self):
    self.__proteins = dict()

  def serve(self, env, start_response):
    path = env["PATH_INFO"].split("/")
    server = path[2]
    extension = path[3]
    protein = path[4]
#    print("{0}.{1} from {2}".format(protein, extension, server))
    res = None

    try:
      pdb = PDBParser()
      buf = pdb.parse(open("static/3M3N", "r"))
      #buf = pdb.parse(open("static/2KXR.pdb", "r"))
      mtype = "application/octet-stream"
      res = Response(status=200, content_type=mtype)
      res.body = buf.read()
    except IOError as e:
      res = Response(status=404, content_type="text/html")
      res.body = "<html><body><h1>404 - Not found</h1></body></html>"
    except Exception as e:
      res = Response(status=500, content_type="text/html")
      res.body = "<html><body><h1>500 - Internal server error</h1></body></html>"
      print("errrrrrr " + str(e))
    finally:
      return res(env, start_response)

