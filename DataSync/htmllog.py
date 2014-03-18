# -*- coding: utf-8 -*-
__author__ = 'Augustyn'

class HtmlLog:
    def __init__(self):
        self.htmlCode = ""
        pass

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
        f.write("</body>/n</html>")
        f.close()

    def clear(self):
        pass

htmlLog = HtmlLog()

