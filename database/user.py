""" A user """

from database.dictionary import Dictionary
from database.user_group import UserGroup


class User(object):
    def __init__(self, user_id, title, first_name, last_name, email, language):
        self.__id = user_id
        self.__salutation = title
        self.__first_name = first_name
        self.__last_name = last_name
        self.__email = email
        self.__groups = None
        #self.__pseudo_group = UserGroup(-1, "", groups)
        self.__language = language

        self.__cookie = None

    def get_cookie(self):
        return self.__cookie

    def get_dictionary(self):
        return Dictionary.get_language(self.__language)

    def get_email(self):
        return self.__email

    def get_id(self):
        return self.__id

    def get_name(self, fmt="{0} {1}"):
        return fmt.format(self.__first_name, self.__last_name)

    def get_proteins(self):
        return self.__pseudo_group.get_proteins()


    def get_variables(self):
        """Get the user's variables for adding to a template

        :type  translator: Server
        :param translator: An object that handles string translation
        :rtype: map[string, string]
        :returns: A dictionary for the page's template
        """
        var = {"__user_salutation"  : self.__salutation,
               "__user_name_first"  : self.__first_name,
               "__user_name_last"   : self.__last_name,
               "__user_email"   : self.__email,
			   "__user_groups"  : self.__groups
              }
        return var

    def set_cookie(self, cookie):
        """Set the new cookie to store session info

        :type  cookie: Cookie
        :param cookie: A cookie to return to the server
        """
        self.__cookie = cookie

