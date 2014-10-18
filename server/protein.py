""" Serve a specific protein """

import logging
import mimetypes
import os
import traceback

from server import post_parser, responder
from server.protein_downloader import ProteinGetter

class Protein(object):
  def __init__(self):
    pass

  def serve(self, env, path, user, database):
    response = responder.Response()

    server = path[1]
    format = path[2]
    s_name = path[3]
    protein_db = database.proteins()

    source = protein_db.find_source(server, format)
    if not source:
      response.set_status_code(response.NOT_FOUND)
      return response

    protein = protein_db.get_protein_info(source, s_name)
    if not protein:
      # Try downloading a new one!
      if source.is_private():
        response.set_status_code(response.NOT_FOUND)
        return response

      # Return processing for now; we've queued the request !?
      getter = ProteinGetter(database, source, s_name)
      getter.start()
      response.set_status_code(response.PROCESSING)
      return response

    if protein.is_processing():
      response.set_status_code(response.PROCESSING)
      return response
    model = None
    for mid in protein.get_models():
      model = protein_db.load_model(protein, mid)
      break
    if model:
      response.set_body(model, "application/octet-stream")
    return response
