# -*- coding: utf-8 -*-
__author__ = 'Augustyn'

import os


class HtmlLog:
    CHANGES_START_ID = "<!-- CHANGES START -->"
    CHANGES_END_ID = "<!-- CHANGES END -->"
    HTML_TEMPLATE = """
<html>
    <head>
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
        <style>
            body {
                font-family:Tahoma;
            }
        </style>
    </head>
    <body>
""" + CHANGES_START_ID + CHANGES_END_ID + """
    </body>
</html>
"""

    def __init__(self):
        self.htmlCode = ""
        pass

    def addHeader(self, caption):
        self.htmlCode += "<h1>" + caption + "</h1>"

    def openTable(self):
        self.htmlCode += "<table>"

    def closeTable(self):
        self.htmlCode += "</table>"

    def openTableRow(self):
        self.htmlCode += "<tr>"

    def closeTableRow(self):
        self.htmlCode += "</tr>"

    def addCol(self, value, align=""):
        if align == "":
            self.htmlCode += "<td>"
        else:
            self.htmlCode += '<td align="' + align + '" >'

        self.htmlCode += str(value) + "</td>"

    def closeSection(self, fileName):
        if os.path.exists(fileName):
            with open(fileName, "r") as f:
                htmlPage = f.read()
                f.close()
        else:
            htmlPage = self.HTML_TEMPLATE
        htmlPage = htmlPage.replace(self.CHANGES_START_ID, "")
        htmlPage = htmlPage.replace(self.CHANGES_END_ID, self.CHANGES_START_ID + self.CHANGES_END_ID)
        with open(fileName, "w") as f:
            f.write(htmlPage)
            f.close()

    def save(self, fileName):
        if os.path.exists(fileName):
            with open(fileName, "r") as f:
                htmlPage = f.read()
                f.close()
        else:
            htmlPage = self.HTML_TEMPLATE

        with open(fileName, "w") as f:
            prefix = htmlPage[:htmlPage.find(self.CHANGES_START_ID) + len(self.CHANGES_START_ID)]
            suffix = htmlPage[htmlPage.find(self.CHANGES_END_ID):]
            f.write(prefix + self.htmlCode + suffix)
            f.close()

    def clear(self):
        self.htmlCode = ""


htmlLog = HtmlLog()

