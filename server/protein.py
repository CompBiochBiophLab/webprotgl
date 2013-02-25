#! /usr/bin/python

from database.database import Database
from database.pdb_parser import PDBParser
from traceback import print_exc
from webob.response import Response

class ProteinServer():
  def __init__(self):
    self.__proteins = dict()

  def serve(self, env, start_response):
    path = env["PATH_INFO"].split("/")

    try:
      self.__db = Database()
      self.__db.load()
      server = path[2]
      basetype = path[3]
      protname = path[4]

      # Find source server
      source = self.__db.find_source(server, basetype)
      if not source:
        res = Response(status=404, content_type="text/html")
        res.body = "<html><body><h1>404 - Not found</h1><p>Source server {0} not found for {1}</body></html>".format(server, basetype)
      else:
        protein = self.__db.get_protein_info(source,  protname)
        if not protein:
          res = Response(status=404, content_type="text/html")
          res.body = "<html><body><h1>404 - Not found</h1><p>Protein {0} not found</body></html>".format(protname)
        else:
          model = None
          for mid in protein.get_models():
            model = self.__db.load_model(protein, mid)
            break
          if model:
            res = Response(status=200, content_type="application/octet-stream")
            res.body = model
          else:
            res = Response(status=500, content_type="text/html")
            res.body = "<html><body><h1>500 - Internal server error</h1></body></html>"
    except IOError as e:
      res = Response(status=404, content_type="text/html")
      res.body = "<html><body><h1>404 - Not found</h1></body></html>"
    except Exception as e:
      res = Response(status=500, content_type="text/html")
      res.body = "<html><body><h1>500 - Internal server error</h1></body></html>"
      print_exc()
    finally:
      return res(env, start_response)

