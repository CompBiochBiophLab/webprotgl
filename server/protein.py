#! /usr/bin/python

from database.database import Database
from database.pdb_parser import PDBParser
from traceback import print_exc

class ProteinServer():
  def __init__(self):
    self.__proteins = dict()

  def serve(self, env, start_response):
    path = env["PATH_INFO"].split("/")
    status = "404 - Not found"
    mimetype = "text/html"
    body = "<html><body><h1>404 - Not found</h1></body></html>"

    try:
      self.__db = Database()
      self.__db.load()
      server = path[2]
      basetype = path[3]
      protname = path[4]

      # Find source server
      source = self.__db.find_source(server, basetype)
      if source:
        protein = self.__db.get_protein_info(source,  protname)
        if protein:
          model = None
          for mid in protein.get_models():
            model = self.__db.load_model(protein, mid)
            break
          if model:
            status = "200 - OK"
            mimetype = "application/octet-stream"
            body = model
          else:
            status = "500 - Internal Server Error"
            body = "<html><body><h1>500 - Internal server error</h1></body></html>"
    except IOError as e:
      print_exc()
    except Exception as e:
      status = "500 - Internal Server Error"
      body = "<html><body><h1>500 - Internal server error</h1></body></html>"
      print_exc()
    finally:
      start_response(status, [("Content-Type", mimetype), ("Content-Length", str(len(body)))])
      return [body]

