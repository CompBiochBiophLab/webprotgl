""" Serve a specific protein """

import logging

from server import responder
from server.async.protein_downloader import ProteinGetter
from server.html import html_format_file
from server.navigation import Navigation


class Protein(object):
  def __init__(self):
    pass

  def serve(self, _env, path, user, database):
    response = responder.Response()

    server = path[1].lower()
    in_fmt = path[2].lower()
    s_name = path[3].lower()

    protein_db = database.proteins()

    source = protein_db.find_source(server, in_fmt)
    if not source:
      response.set_status_code(response.NOT_FOUND)
      return response

    protein = protein_db.get_protein_info(source, s_name)
    if not protein:
      logging.debug("Protein not in db")
      # Try downloading a new one!
      if source.is_private():
        response.set_status_code(response.NOT_FOUND)
        return response

      # Return processing for now; we've queued the request !?
      getter = ProteinGetter(database, source, s_name)
      getter.start()

      if len(path) == 4:
        # Serve an html page for that protein!
        return self.__serve_html(s_name, user, response)

      response.set_status_code(response.PROCESSING)
      return response

    if len(path) == 4:
      # Serve an html page for that protein!
      return self.__serve_html(s_name, user, response)

    mid = path[4]

    if protein.is_processing():
      logging.debug("Protein not ready yet")
      response.set_status_code(response.PROCESSING)
      return response
    model = None
    if mid in protein.get_models():
      model = protein_db.load_model(protein, mid)
    else:
      # Load first model (?)
      for mid in protein.get_models():
        model = protein_db.load_model(protein, mid)
        break
    if model:
      response.set_body(model, "application/octet-stream")
    return response

  def __serve_html(self, protein_name, user, response):
    nav = Navigation()
    nav.add_link("", "Show", Navigation.DISPLAY, 0)
    nav.add_link("", "van der Waals", Navigation.DISPLAY, 0, "Show", {"show": "vdw"})
    nav.add_link("", "Balls & Sticks", Navigation.DISPLAY, 1, "Show", {"show": "balls"})
    variables = {
        "html_title": protein_name.upper(),
        "__protein": protein_name.upper(),
        "__canvas_width": 500,
        "__canvas_height": 500
    }
    response.set_html("protein.html", user, nav, variables)
    #response.set_body(html_format_file("protein", protein_name.upper()), "text/html")
    return response