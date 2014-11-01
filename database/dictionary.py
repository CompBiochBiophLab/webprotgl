""" A global dictionary of text variables
"""

import pickle

class Dictionary(object):
  __singleton = None

################################################################

  def __init__(self, file_path):
    with open(file_path, "rb") as dic:
      Dictionary.__singleton = pickle.load(dic)
      dic.close()
    if int(Dictionary.__singleton["_port_"]) != 80:
      port_txt = ":{0}".format(Dictionary.__singleton["_port_"])
    else:
      port_txt = ""

    Dictionary.__singleton["_root_"] = "{0}://{1}{2}{3}".format(
        Dictionary.__singleton["_protocol_"],
        Dictionary.__singleton["_hostname_"],
        port_txt,
        Dictionary.__singleton["_base_path_"])

################################################################

  @staticmethod
  def all():
    return Dictionary.__singleton

################################################################

  @staticmethod
  def get(key):
    if key in Dictionary.__singleton:
      return Dictionary.__singleton[key]
    return None

################################################################

  @staticmethod
  def format(value, variables=None):
    if variables:
      variables.update(Dictionary.__singleton)
      return value.format(**variables)
    return value.format(**Dictionary.__singleton)

################################################################
