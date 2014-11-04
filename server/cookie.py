from datetime import datetime

class Cookie():
  def __init__(self, name, value, expires = None):
    self.__name = name
    self.__value = value
    self.__expires = expires

  def get_string(self, domain, path, port=80):
    if self.__expires:
      expires = "; Expires={0}".format(self.__expires.strftime("%a, %d %b %Y %T GMT"))
    else:
      expires = ""
     
    if port != 80:
      port_txt = "; Port={0}".format(port)
    else:
      port_txt = ""
      
    if domain == "localhost":
      domain = ""
    
    return "{0}={1}; Domain={2}; Path={3}{4}{5}".format(self.__name, self.__value, domain, path, expires, port_txt)
 
