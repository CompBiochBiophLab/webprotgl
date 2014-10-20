"""
Static files server
Only for testing (?)
"""

import logging
import mimetypes
#import os

from server import post_parser, responder

class Static(object):
  def __init__(self):
    pass

  def serve(self, env, path, user, database):
    response = responder.Response()
    if len(path) <= 1:
      logging.debug("Missing path")
      response.set_status_code(response.BAD_REQUEST)
      return response

    filename = os.path.join(os.environ["WORKDIR"], "/".join(path))
    with open(filename, "rb") as static:
      mtype, menc = mimetypes.guess_type(filename)
      if not mtype:
        mtype = "application/octet-stream"
      response.set_body(static.read(), mtype)
      static.close()
    return response
