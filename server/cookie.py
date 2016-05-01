""" Cookie management """

from urllib.parse import unquote_plus


class Cookie():
    def __init__(self, name, value, expires=None):
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
    
        return "{0}={1}; Domain={2}; Path={3}{4}{5}".format(self.__name, self.__value,
                                                            domain, path, expires, port_txt)

    @staticmethod
    def restore(data):
        cookies = []
        while True:
            key_sep = data.find("=")
            val_sep = data.find(";", key_sep)
            if key_sep < 0:
                break

            key = unquote_plus(data[0:key_sep])
            if val_sep < 0:
                val = data[key_sep+1:]
                cookies.append(Cookie(key, unquote_plus(val)))
                break

            val = data[key_sep+1:val_sep]
            cookies.append(Cookie(key, unquote_plus(val)))
            data = data[val_sep+1:].lstrip()
        return cookies

    def name(self):
        return self.__name

    def value(self):
        return self.__value