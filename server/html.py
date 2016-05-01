""" HTML formatter for responses
"""

import logging
import os

from database.dictionary import Dictionary
from database.user import User
from server.navigation import Navigation


def html_format_template(path, user=None, nav=None, variables=None):
    with open(os.path.join(os.environ["WORKDIR"], "templates", path), "r") as temp:
        return html_format_text(temp.read(), user, nav, variables)
    return None


def html_format_file(name, title="", user=None, nav=None):
    with open(os.path.join(os.environ["WORKDIR"], "templates", name + ".html"), "r") as temp:
        variables = {"title": title}
        return html_format_text(temp.read(), user, nav, variables)
    return None


def html_format_text(main, user=None, nav=None, variables=None):
    if not variables:
        variables = dict()

    if user:
        translator = user.get_dictionary()
        variables.update(user.get_variables())
    else:
        translator = Dictionary.get_default()

    variables.update(translator.get_map())

    if "title" in variables:
        variables["html_title"] = variables["title"] + " | " + variables["html_title"]

    # Navigation defaults
    if not nav:
        nav = Navigation()
    nav.add_link("{_root_}", "{_link_home_}", Navigation.HOME, 0)
    if user:
        # Logout
        nav.add_link("{_root_}/{_session_}/{_logout_}", "{_link_logout_}", Navigation.LOGOUT, 0)
    else:
        # Register
        nav.add_link("{_root_}/{_session_}/{_register_}", "{_link_register_}", Navigation.HOME, 1)
        # Login
        nav.add_link("{_root_}/{_session_}/{_login_}", "{_link_login_}", Navigation.HOME, 2)

    variables["html_nav"] = nav.flatten_to_html(translator)

    variables["html_main"] = translator.format(main, variables)

    with open(os.path.join(os.environ["WORKDIR"], "templates", "backbone.html")) as backbone:
        page = backbone.read()
        return translator.format(page, variables).encode("UTF-8")
    return None
