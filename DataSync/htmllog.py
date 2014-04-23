# -*- coding: utf-8 -*-
__author__ = 'Augustyn'

import os


class HtmlLog:
    CHANGES_START_ID = "<!-- CHANGES START -->"
    CHANGES_END_ID = "<!-- CHANGES END -->"
    TEMPLATE_FILENAME = 'logtemplate.html'

    def __init__(self):
        self.htmlCode = ""
        pass

    def addHeader(self, caption):
        self.htmlCode += "<h2>" + caption + "</h2>\n"

    def openTable(self):
        self.htmlCode += "<table>\n"

    def closeTable(self):
        self.htmlCode += "</table>\n"

    def openTableRow(self, tags = ""):
        if tags != "" and tags[:1] != " ":
            tags = " " + tags
        self.htmlCode += '<tr' + tags + '>'

    def closeTableRow(self):
        self.htmlCode += "</tr>\n"

    def addCol(self, value, tags = ""):
        if tags != "" and tags[:1] != " ":
            tags = " " + tags

        self.htmlCode += '<td' + tags + ' >' + str(value) + "</td>"

    def getHTMLContent(self, fileName):
        if not os.path.exists(fileName):
            fileName = self.TEMPLATE_FILENAME
        with open(fileName, "r") as f:
            result = f.read()
            f.close()
        return result

    def closeSection(self, fileName):
        htmlPage = self.getHTMLContent(fileName)

        htmlPage = htmlPage.replace(self.CHANGES_START_ID, "")
        htmlPage = htmlPage.replace(self.CHANGES_END_ID, self.CHANGES_START_ID + self.CHANGES_END_ID)
        htmlPage = htmlPage.replace("AutoRefresh = true", "AutoRefresh = false")

        with open(fileName, "w") as f:
            f.write(htmlPage)
            f.close()

    def save(self, fileName):
        htmlPage = self.getHTMLContent(fileName)
        htmlPage = htmlPage.replace("AutoRefresh = false", "AutoRefresh = true")

        with open(fileName, "w") as f:
            prefix = htmlPage[:htmlPage.find(self.CHANGES_START_ID) + len(self.CHANGES_START_ID)]
            suffix = htmlPage[htmlPage.find(self.CHANGES_END_ID):]
            f.write(prefix + self.htmlCode + suffix)
            f.close()

    def clear(self):
        self.htmlCode = ""

htmlLog = HtmlLog()

