""" Server for non-200 codes """

import logging
import traceback

from database.dictionary import Dictionary
from server.html import html_format_template


class Response(object):
    PROCESSING  = 102
    OK          = 200
    NO_CONTENT  = 204
    REDIRECT    = 303
    BAD_REQUEST = 400
    BAD_LOGIN   = 401
    FORBIDDEN   = 403
    NOT_FOUND   = 404
    GONE        = 410
    PRECONDITION_FAILED = 412
    ERROR       = 500

    def __init__(self):
        self.__status = self.NOT_FOUND
        self.__body = b""
        self.__mime_type = "application/json"
        self.__cookie = None
        self.__location = ""

    def finalise(self, user):
        if not self.__body and self.__status >= 400:
            try:
                self.__body = html_format_template("errors/" + str(self.__status) + ".html", user)
                self.__mime_type = "text/html"
            except Exception as exc:
                logging.error("Exception serving error " + str(self.__status) + ": " + str(exc))
                logging.error(traceback.format_exc())
                logging.error("--------")

    def get_body(self):
        return [self.__body]
    
    def set_body(self, body, mime_type=None):
        self.__status = self.OK
        self.__body = body
        if mime_type:
            self.__mime_type = mime_type

    def set_html(self, path, user=None, nav=None, variables=None):
        self.__body = html_format_template(path, user, nav, variables)
        if self.__body:
            self.__status = self.OK
            self.__mime_type = "text/html"
        else:
            self.__status = self.NOT_FOUND
            self.__body = b""
  
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

    def get_params(self):
        domain = Dictionary.get("_hostname_")
        host = Dictionary.get("_protocol_") + "://" + domain
        root = Dictionary.format("{_base_path_}/")
        port = int(Dictionary.get("_port_"))
        params = [("Content-Type", self.__mime_type),
                  ("Content-Base", host),
                  ("Content-Length", str(len(self.__body)))]
        if self.__cookie:
            logging.debug("Has cookie")
            params.append(("Set-Cookie", self.__cookie.get_string(domain, root, port)))
        if self.__location:
            logging.debug("Redirect to " + self.__location)
            params.append(("Location", self.__location))
        return params


class Responder(object):
    def __init__(self):
        pass

    def serve(self, start_response, response=Response):
        """ Serve the response """

        status = response.get_status_code()

        params = response.get_params()
        start_response(status, params)
        return response.get_body()
