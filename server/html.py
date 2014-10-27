""" HTML formatter for responses
"""

import os

from database.dictionary import Dictionary

def html_format_file(name, title="", user=None, nav=[]):
  with open(os.path.join(os.environ["WORKDIR"], "templates", name + ".html")) as input:
    vars = {
      "title": title,
    }

    vars.update(Dictionary.all())

    if title:
      vars["html_title"] = title + " - WebGLProtein"

    # Navigation defaults
    if not user:
      # Register
      nav.insert(0, (Dictionary.format("/{_session_}/{_register_}"), Dictionary.get("register")))
      # Login
      nav.insert(1, (Dictionary.format("/{_session_}/{_login_}"), Dictionary.get("login"), "bottom"))
      nav.insert(1, ())
    else:
      # Logout
      nav.append((Dictionary.format("/{_session_}/{_logout_}"), Dictionary.get("logout"), "bottom"))
    navigation = ""
    for item in nav:
      attr = ""
      if len(item) < 2:
        # Separation
        navigation += "   <li class=\"separator\"></li>"
      else:
        navigation += "   <li><a href=\"{0}\">{1}</a></li>\n".format(item[0], item[1])
    vars["html_nav"] = navigation

    content = input.read()
    vars["html_main"] = content.format(**vars)

    with open(os.path.join(os.environ["WORKDIR"], "templates", "backbone.html")) as backbone:
      page = backbone.read()
      return page.format(**vars).encode("UTF-8")

def html_format_text(main, title="", nav=dict()):
  vars = {
    "html_main": main
  }
  vars.update(Dictionary.all())
  vars.update(nav)

  if title:
    vars["html_title"] = title + " - WebGLProtein"

  with open(os.path.join(os.environ["WORKDIR"], "templates", "backbone.html")) as backbone:
    page = backbone.read()
    return page.format(**vars).encode("UTF-8")
