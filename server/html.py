""" HTML formatter for responses
"""

import os

def html_format_file(name, title="", nav=dict()):
  with open(os.path.join(os.environ["WORKDIR"], "templates", name + ".html")) as input:
    vars = {
    #   "_protein_": "protein",
    #   "_root_": "",
    #   "_static_": "static",
    #   "title": title,
    #   "html_footer": "",
    #   "html_header": "",
    #   "html_nav": "",
      "html_title": "WebGLProtein"
    }
    
    if title:
      vars["html_title"] = title + " - WebGLProtein"

    global dictionary
    vars.update(dictionary)

    content = input.read()
    vars["html_main"] = content.format(**vars)
    vars.update(nav)

    with open(os.path.join(os.environ["WORKDIR"], "templates", "backbone.html")) as backbone:
      page = backbone.read()
      return page.format(**vars).encode("UTF-8")

def html_format_text(main, title="", nav=dict()):
  vars = {
  #   "_root_": "/webglprotein",
  #   "_static_": "static",
    "html_title": "WebGLProtein",
  #   "html_footer": "",
  #   "html_header": "",
  #   "html_nav": "",
    "html_main": main
  }
  if title:
    vars["html_title"] = title + " - WebGLProtein"

  global dictionary
  vars.update(dictionary)
  vars.update(nav)

  with open(os.path.join(os.environ["WORKDIR"], "templates", "backbone.html")) as backbone:
    page = backbone.read()
    return page.format(**vars).encode("UTF-8")
