# -*- coding: utf-8 -*-
__author__ = 'Augustyn'

import codecs

SERVER_URL = "http://www.vugtk.cz/euradin/services/rest.py"

HTML_PREFIX = u"""
<html>
    <head>
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
	    <meta http-equiv="X-UA-Compatible" content="IE=edge" />
	    <style>
	    body {
	        font-family: tahoma;
	    }

        th {
         background-color: #A7C942;
         color : #fff;
        }

        tr.alt td {
          color: #00;
          background-color: #EAF2D3;
        }

        table {
            border-collapse: collapse;
        }

        td, th {
            border: 1px solid #98bf21;
            vertical-align:top;
        }

	    </style>
	    <title><#TITLE></title>
	</head>
	<body>"""

HTML_SUFFIX = """
    </body>
</html>"""

RESULTS_TABLE_HEADER_LONG = u"""
<table>
    <tr>
            <th>#</th><th></th><th>Vstup</th><th>Výsledek</th><th>Pozn</th>
    </tr>
"""

RESULTS_TABLE_HEADER = u"""
<table>
    <tr>
            <th>#</th><th></th><th align="left">Test</th>
    </tr>
"""

class FormalTester:
    def __init__(self, caption, desc, compilingPerson, tester):
        self.numTests = 0
        self.caption = caption
        self.desc = desc
        self.compilingPerson = compilingPerson
        self.tester = tester
        self.testsHTML = RESULTS_TABLE_HEADER
        self.longPrint = False
        self.isOddRow = False

    def addTest(self, inputs, result, expectedResult, errorMessage = ""):
        self.numTests = self.numTests + 1

        if str(result) == expectedResult:
            status = "checked"
            print "   ok :", inputs, "-->", result
            expectedResultMessage = u""
        else:
            status = ""
            expectedResultMessage = u" ≠ " + expectedResult
            print "chyba :", inputs, "-->", result, "<>", expectedResult, errorMessage

        if self.isOddRow:
            oddText = ' class="alt"'
        else:
            oddText = ''

        if self.longPrint:
            self.testsHTML += "<tr" + oddText + ">\n"
            self.testsHTML += "    <td>" + str(self.numTests) + "</td>"
            self.testsHTML += "    <td>" + '<input type="checkbox" value=""' + status + ' \>' + "</td>"

            self.testsHTML += "    <td>" + inputs + "</td>"
            self.testsHTML += "    <td>" + str(result) + expectedResultMessage + "</td>" # →
            self.testsHTML += "    <td>" + errorMessage + "</td>"
            self.testsHTML += "</tr>\n"
        else:
            self.testsHTML += "<tr" + oddText + ">\n"
            self.testsHTML += "    <td>" + str(self.numTests) + "</td>"
            self.testsHTML += "    <td>" + '<input type="checkbox" value=""' + status + ' \>' + "</td>"

            self.testsHTML += "    <td>" + inputs + "<br>"
            self.testsHTML += str(result) + expectedResultMessage + "<br>"
            if errorMessage != "":
                self.testsHTML += "    <td>" + errorMessage + "</td>"
            self.testsHTML += "</tr>\n"

        self.isOddRow = not self.isOddRow

    def getHTML(self):
        result = HTML_PREFIX

        result = result.replace("<#TITLE>", self.caption)
        if self.caption != "": result += "<h1>" + self.caption + "</h1>\n"
        if self.desc != "": result += "<p>" + self.desc + \
                                      u"<br><br>Testovaný server: <a href='" + SERVER_URL + "'>" + SERVER_URL + "</a><br>" + \
                                      "</p>\n"
        result += self.testsHTML + "</table>"
        result += HTML_SUFFIX

        return result

    def saveToHTML(self, fileName):
        with codecs.open(fileName, "w", "utf-8") as outFile:
            htmlContent = self.getHTML()
            outFile.write(codecs.encode(htmlContent, "utf-8"))
            outFile.close()

def test():
    tester = FormalTester("Caption text", """Description text""", "Compiling person", "Tester")

    tester.addTest("OK test", "Test value", "Test value", "OK Test")
    tester.addTest("Fail test", "Wrong test value", "Test value", "Error message")
    tester.saveToHTML("sharedtools.html")


if __name__ == '__main__':
    test()