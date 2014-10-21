""" HTML formatter for responses
"""

import os

from database.dictionary import Dictionary

def html_format_file(name, title="", nav=dict()):
  with open(os.path.join(os.environ["WORKDIR"], "templates", name + ".html")) as input:
    vars = {
      "title": title,
    }

    vars.update(Dictionary.all())

    if title:
      vars["html_title"] = title + " - WebGLProtein"

    content = input.read()
    vars["html_main"] = content.format(**vars)
    vars.update(nav)

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
