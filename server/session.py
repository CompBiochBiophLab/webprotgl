""" Serve session management """

import logging

from database.dictionary import Dictionary
from database.user import User
from server import responder
from server.post_parser import parse
from time import sleep


class Session(object):
    def __init__(self):
        pass

################################################################

    def serve(self, env, path, user, database):
        method = env["REQUEST_METHOD"]
        response = responder.Response()

        special_get = ["activate", "logout", "reset"]
        if method == "POST" or path[1] in special_get:
            fun = getattr(self, path[1])
            if fun:
                response = fun(env, path, user, database)
        elif method == "GET":
            if path[1] == "activate":
                response = self.activate(env, path, user, database)
            else:
                response.set_html("session/" + path[1] + ".html", user)
        else:
            response.set_status_code(405)  # Method Not Allowed
        return response

################################################################

    @staticmethod
    def activate(_, path, user, database):
        response = responder.Response()
        if user:
            response.set_status_code(409)  # Conflict
            return response

        if len(path) != 3:
            response.set_status_code(response.BAD_REQUEST)
            return response

        result = database.users().activate(path[2])
        if result == 0:
            response.set_redirect("{_root_}/{_session_}/{_activated_}")
        elif result == 1:
            response.set_status_code(response.GONE)
        return response

################################################################

    @staticmethod
    def login(env, _, user, database):
        response = responder.Response()
        # if user:
        #   response.set_status_code(409)  # Conflict
        #   return response

        data = parse(env)
        (user, cookie) = database.users().find_user(data)
        if user:
            response.set_status_code(response.NO_CONTENT)
            response.set_cookie(cookie)
        else:
            response.set_status_code(401)

        sleep(2)  # Don't allow mass-spamming
        return response

################################################################

    @staticmethod
    def logout(env, path, user, database):
        response = responder.Response()
        # if not user:
        #   response.set_status_code(409)  # Conflict
        #   return response

        response.set_cookie(database.users().revoke_session(user))
        response.set_redirect("{_root_}/{_session_}/{_login_}")
        return response

################################################################

    @staticmethod
    def lost(env, _, user, database):
        response = responder.Response()
        if user:
            response.set_status_code(409)  # Conflict
            return response

        data = parse(env)
        if database.users().initiate_reset(data):
            response.set_status_code(response.NO_CONTENT)

        sleep(2)  # Don't allow mass-spamming
        return response

################################################################

    @staticmethod
    def register(env, _, user, database):
        response = responder.Response()
        if user:
            response.set_status_code(409)  # Conflict
            return response

        data = parse(env)
        if database.users().register(data):
            response.set_status_code(response.NO_CONTENT)
        else:
            response.set_status_code(409)  # Conflict

        sleep(2)  # Don't allow mass-spamming
        return response

################################################################

    @staticmethod
    def reset(env, path, user, database):
        response = responder.Response()
        if user:
            response.set_status_code(409)  # Conflict
            return response

        if env["REQUEST_METHOD"] == "POST":
            data = parse(env)
            logging.debug("post")
            if len(path) > 2:
                # Last reset step with session ID
                result = database.users().finish_reset(path[2], data)
                if result == 410:
                    response.set_status_code(response.GONE)
                elif result == 412:
                    response.set_status_code(response.PRECONDITION_FAILED)
                elif result:
                    response.set_status_code(response.NO_CONTENT)
            else:
                if database.users().initiate_reset(data, User.NORMAL):
                    response.set_status_code(response.NO_CONTENT)
                elif database.users().initiate_reset(data, User.EXPERT):
                    response.set_status_code(response.NO_CONTENT)

            sleep(2)  # Don't allow mass-spamming
        else:
            # Information page or actual reset page?
            if path[-1] == "reset":
                # Display information page
                response.set_html("session/reset.html")
            # Check validity (expiration)
            elif database.users().reset_valid(path[-1]):
                response.set_html("session/reset_form.html")
            else:
                response.set_status_code(response.GONE)

        return response

################################################################

    @staticmethod
    def reset_form(env, path, user, database):
        response = responder.Response()
        if user:
            response.set_status_code(409)  # Conflict
            return response

        if env["REQUEST_METHOD"] == "POST":
            data = parse(env)
            if database.users().confirm_reset(path[-1], data):
                response.set_status_code(response.NO_CONTENT)

            sleep(2)  # Don't allow mass-spamming
        else:
            # Information page or actual reset page?
            if path[-1] == "reset":
                # Display information page
                response.set_html("session/reset.html")
            # Check validity (expiration)
            elif database.users().reset_valid(path[-1]):
                response.set_html("session/reset_success.html")
            else:
                response.set_status_code(response.GONE)

        return response

################################################################
