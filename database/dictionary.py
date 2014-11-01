""" A global dictionary of text variables
"""

import pickle

class Dictionary(object):
  __singleton = None

  def __init__(self, file_path):
    with open(file_path, "rb") as dic:
      Dictionary.__singleton = pickle.load(dic)
      dic.close()
    if int(Dictionary.__singleton["_port_"]) != 80:
      port_txt = ":{0}".format(Dictionary.__singleton["_port_"])
    else:
      port_txt = ""

    Dictionary.__singleton["_root_"] = "{0}://{1}{2}{3}".format( \
      Dictionary.__singleton["_protocol_"], \
      Dictionary.__singleton["_hostname_"], \
      port_txt, \
      Dictionary.__singleton["_base_path_"])

  def all():
    return Dictionary.__singleton

  def get(key):
    if key in Dictionary.__singleton:
      return Dictionary.__singleton[key]
    return None

  def format(value, vars=None):
    if vars:
      vars.update(Dictionary.__singleton)
      return value.format(**vars)
    return value.format(**Dictionary.__singleton)