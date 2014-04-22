# -*- coding: utf-8 -*-
__author__ = 'Augustyn'

import os


class HtmlLog:
    NEXT_CODE_ID = "<!-- NEXTCODE -->"
    CHANGES_START_ID = "<!-- CHANGES START -->"
    CHANGES_END_ID = "<!-- END -->"

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

    def addCol(self, value, align = ""):
        if align == "":
            self.htmlCode += "<td>"
        else:
            self.htmlCode += '<td align="' + align + '" >'

        self.htmlCode += str(value) + "</td>"

    def save(self, fileName):
        if os.path.exists(fileName):
            with open(fileName, "r") as f:
                htmlPage = f.read()
                f.close()
        else:
            htmlPage = """
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
""" + \
            self.NEXT_CODE_ID + self.CHANGES_END_ID + """
    </body>
</html>
"""
        with open(fileName, "w") as f:
            prefix = htmlPage[:htmlPage.find(self.CHANGES_START_ID)]
            suffix = htmlPage[htmlPage.find(self.CHANGES_END_ID):]
            f.write(prefix + self.htmlCode + suffix)
            f.close()

    def clear(self):
        self.htmlCode = ""

htmlLog = HtmlLog()

