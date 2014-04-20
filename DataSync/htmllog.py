# -*- coding: utf-8 -*-
__author__ = 'Augustyn'

class HtmlLog:
    def __init__(self):
        self.clear()
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

    def addCol(self, value):
        self.htmlCode += "<td>" + str(value) + "</td>"

    def save(self, fileName):
        f = open(fileName, "w")
        f.write(self.htmlCode)
        f.write("""
    </body>
</html>
""")
        f.close()

    def clear(self):
        self.htmlCode = """
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
"""


        pass

htmlLog = HtmlLog()

