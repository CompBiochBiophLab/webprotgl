""" HTML formatter for responses
"""

import logging
import os

from database.dictionary import Dictionary
from server.navigation import Navigation


def html_format_template(path, user=None, nav=None, variables=None):
    with open(os.path.join(os.environ["WORKDIR"], "templates", path)) as temp:
        return html_format_text(temp.read(), user, nav, variables)
    return None


def html_format_file(name, title="", user=None, nav=None):
    with open(os.path.join(os.environ["WORKDIR"], "templates", name + ".html")) as temp:
        variables = {"title": title}
        return html_format_text(temp.read(), user, nav, variables)
    return None


def html_format_text(main, user=None, nav=None, variables=None):
    if not variables:
        variables = dict()

    variables.update(Dictionary.all())

    if "title" in variables:
        variables["html_title"] = variables["title"] + " | " + variables["html_title"]

    # Navigation defaults
    if not nav:
        nav = Navigation()
    nav.add_link("{_root_}", "{home}", Navigation.HOME, 0)
    if not user:
        # Register
        nav.add_link("{_root_}/{_session_}/{_register_}", "{register}", Navigation.HOME, 1)
        # Login
        nav.add_link("{_root_}/{_session_}/{_login_}", "{login}", Navigation.HOME, 2)
    else:
        # Logout
        nav.add_link("{_root_}/{_session_}/{_logout_}", "{logout}", Navigation.LOGOUT, 0)

    variables["html_nav"] = nav.flatten_to_html()
    variables["html_main"] = Dictionary.format(main, variables)

    with open(os.path.join(os.environ["WORKDIR"], "templates", "backbone.html")) as backbone:
        page = backbone.read()
        return Dictionary.format(page, variables).encode("UTF-8")
    return None
