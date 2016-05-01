__author__ = 'jrenggli'

from database.dictionary import Dictionary


class Navigation(object):
    HOME = 0
    DISPLAY = 100
    LOGOUT = 10000

    def __init__(self):
        self.__categories = dict()
        self.__sublinks = dict()

    def add_link(self, link, text, category, priority,
                 subcategory="", attributes=None):
        categ = dict()
        if category in self.__categories:
            categ = self.__categories[category]

        attrs = dict()
        if attributes:
            attrs.update(attributes)

        if subcategory:
            for item in categ:
                (categ_link, categ_name, categ_sub, categ_attr) = categ[item]
                if categ_name == subcategory:
                    assert (priority not in categ_sub)
                    categ_sub[priority] = (link, text, attrs)
                    break
        else:
            categ[priority] = (link, text, dict(), attrs)
        self.__categories[category] = categ

    def flatten_to_html(self, translator):
        html = ""
        first = True
        for category in self.__categories:
            # Separator
            if first:
                first = False
            else:
                html += "   <li class=\"separator\"></li>\n"

            cat = self.__categories[category]
            for c_priority in cat:
                (c_link, c_name, c_sub, c_attr) = cat[c_priority]
                temp = ""
                c_group = ""
                cc_group = ""
                cc_attr = ""
                for attr in c_attr:
                    cc_attr += " " + attr + "=\"" + c_attr[attr] + "\""
                if len(c_sub) > 0:
                    c_group = " closed_group"
                    cc_group = " class=\"closed_group\""
                if c_link:
                    temp += "   <li{3}><a href=\"{0}\"{3}>{1}</a>"
                else:
                    temp += "   <li class=\"nolink{2}\"{3}>{1}"
                html += temp.format(c_link, c_name, c_group, cc_group, cc_attr)
                if len(c_sub) > 0:
                    html += "\n    <ul>"
                    for item in c_sub:
                        (sub_link, sub_name, sub_attr) = c_sub[item]
                        temp = ""
                        sub_att = ""
                        for attr in sub_attr:
                            sub_att += " " + attr + "=\"" + sub_attr[attr] + "\""
                        if sub_link:
                            temp += "\n     <li><a href=\"{0}\"{2}>{1}</a></li>"
                        else:
                            temp += "\n     <li class=\"nolink\"{2}>{1}</li>"
                        html += temp.format(sub_link, sub_name, sub_att)
                    html += "\n    </ul>"
                html += "</li>\n"

        return translator.format(html)