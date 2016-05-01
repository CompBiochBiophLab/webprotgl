""" A global dictionary of text variables
"""

#import logging
import pickle


class Dictionary(object):
    ENGLISH = "en"

    LANGUAGES = [ENGLISH]

    __singletons = dict()

    def __init__(self, file_path):
        with open(file_path, "rb") as dic:
            self.__map = pickle.load(dic)
            dic.close()
        if int(self.__map["_port_"]) != 80:
            port_txt = ":{0}".format(self.__map["_port_"])
        else:
            port_txt = ""

        self.__map["_root_"] = "{0}://{1}{2}{3}".format(
            self.__map["_protocol_"],
            self.__map["_hostname_"],
            port_txt,
            self.__map["_base_path_"])

    @staticmethod
    def load(language, file_path):
        if language in Dictionary.__singletons:
            return
        if language not in Dictionary.LANGUAGES:
            raise Exception("No such language: " + language)
        Dictionary.__singletons[language] = Dictionary(file_path)

    @staticmethod
    def get_default():
        return Dictionary.__singletons[Dictionary.ENGLISH]

    @staticmethod
    def get_language(language):
        if language not in Dictionary.__singletons:
            raise Exception("Language not loaded: " + language)
        return Dictionary.__singletons[language]

    def get(self, key):
        if key in self.__map:
            return self.__map[key]
        return None

    def get_map(self):
        return self.__map

    def format(self, value, variables=None):
        if variables:
            temp = self.__map.copy()
            temp.update(variables)
            return value.format(**temp)
        return value.format(**self.__map)

    def format_date(self, date_fmt, date):
        fmt = self.__map[date_fmt]
        return fmt.format(date.year, date.month, date.day,
                          date.hour, date.minute, date.isoweekday())
