""" HTML formatter for responses
"""

import os

from database.dictionary import Dictionary

def html_format_template(path, user=None, nav=None, vars=None):
  with open(os.path.join(os.environ["WORKDIR"], "templates", path)) as input:
    return html_format_text(input.read(), user, nav, vars)
  return None

def html_format_file(name, title="", user=None, nav=None):
  with open(os.path.join(os.environ["WORKDIR"], "templates", name + ".html")) as input:
    vars = {"title": title}
    return html_format_text(input.read(), user, nav, vars)
  return None

def html_format_text(main, user=None, nav=None, vars=None):
  if not vars:
    vars = dict()

  vars.update(Dictionary.all())

  if "title" in vars:
    vars["html_title"] = vars["title"] + " | " + vars["html_title"]

  # Navigation defaults
  if not nav:
    nav = []
  nav.insert(0, (Dictionary.format("{_root_}/"), Dictionary.get("home")))
  if not user:
    # Register
    nav.insert(1, (Dictionary.format("{_root_}/{_session_}/{_register_}"), Dictionary.get("register")))
    # Login
    nav.insert(2, (Dictionary.format("{_root_}/{_session_}/{_login_}"), Dictionary.get("login"), "bottom"))
    nav.insert(2, ())
  else:
    # Logout
    nav.append((Dictionary.format("{_root_}/{_session_}/{_logout_}"), Dictionary.get("logout"), "bottom"))
  navigation = ""
  for item in nav:
    attr = ""
    if len(item) < 2:
      # Separation
      navigation += "   <li class=\"separator\"></li>\n"
    else:
      navigation += "   <li><a href=\"{0}\">{1}</a></li>\n".format(item[0], item[1])
  vars["html_nav"] = navigation
  vars["html_main"] = Dictionary.format(main)

  with open(os.path.join(os.environ["WORKDIR"], "templates", "backbone.html")) as backbone:
    page = backbone.read()
    return page.format(**vars).encode("UTF-8")
  return None
