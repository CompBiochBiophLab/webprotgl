""" Server for non-200 codes """

import logging

class Response(object):
  PROCESSING  = 102
  OK          = 200
  REDIRECT    = 303
  BAD_REQUEST = 400
  BAD_LOGIN   = 401
  FORBIDDEN   = 403
  NOT_FOUND   = 404
  PRECONDITION_FAILED = 412
  ERROR       = 500

  def __init__(self):
    self.__status = self.NOT_FOUND
    self.__body = "".encode("UTF-8")
    self.__mimetype = "application/json"
    self.__cookie = None
    self.__location = ""
    
  def get_body(self):
    return [self.__body]
    
  def set_body(self, body, mimetype = None):
    self.__status = self.OK
    self.__body = body#.encode("UTF-8")
    if mimetype:
      self.__mimetype = mimetype#.encode("UTF-8")
  
  def set_cookie(self, cookie):
    self.__cookie = cookie
    
  def set_redirect(self, location):
    self.__status = self.REDIRECT
    self.__location = location
    
  def get_status_code(self):
    available = {
      102: "Processing",
      200: "OK",
      201: "Created",
      202: "Accepted",
      204: "No Content",
      205: "Reset Content",
      303: "See Other (you will be redirected now)",
      400: "Bad Request",
      401: "Incorrect Login",
      403: "Forbidden",
      404: "Not Found",
      405: "Method Not Allowed",
      409: "Conflict",
      410: "Gone",
      412: "Precondition Failed",
      413: "Request Entity Too Large",
      415: "Unsupported Media Type",
      500: "Internal Server Error",
      501: "Not Implemented"
    }
    
    assert(self.__status in available)
    return str(self.__status) + " - " + available[self.__status]
    
  def set_status_code(self, code):
    self.__status = code

  def get_params(self, host, domain, root, port):
    params = [("Content-Type", self.__mimetype),
              ("Content-Base", host),
              ("Content-Length", str(len(self.__body)))]
    if self.__cookie:
      logging.debug("Has cookie")
      params.append(("Set-Cookie", self.__cookie.get_string(domain, root, port)))
    if self.__location:
      logging.debug("Redirect to " + self.__location)
      params.append(("Location", root + self.__location))
    return params

class Responder(object):
  def __init__(self, protocol, domain, root, port):
    self.__domain = domain
    self.__protocol = protocol
    self.__host = protocol + "://" + domain
    self.__root = root
    self.__port = port

  def serve(self, start_response, response = Response):
    """ Serve the response """

    status = response.get_status_code()

    params = response.get_params(self.__host, self.__domain, self.__root, self.__port)
    start_response(status, params)
    return response.get_body()
