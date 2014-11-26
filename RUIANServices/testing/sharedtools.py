# -*- coding: utf-8 -*-
__author__ = 'Augustyn'

import codecs
import urllib2
import os

#SERVER_URL = "http://localhost:5689/"
SERVER_URL = "http://localhost/euradin/services/rest.py/"
#SERVER_URL = "http://www.vugtk.cz/euradin/services/rest.py/"

def setupUTF():
    import sys
    reload(sys)
    sys.setdefaultencoding('utf-8')

HTML_PREFIX = u"""
<html>
    <head>
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
	    <meta http-equiv="X-UA-Compatible" content="IE=edge" />
	    <style>
	    body {
	        font-family: Arial;
			font-size: small;
			color: #575757;
			margin: 10 10 10 10;
	    }

		a {
            color: #1370AB;
		}

        th {
         background-color: #1370AB;
         color : #fff;
        }

        h1 {
            color: #1370AB;
			border-bottom: 1 solid #B6B6B6;
        }

        tr.alt td {
          color: #00;
          background-color: #EAF2D3;
        }

        table {
            border-collapse: collapse;
        	font-size: small;
        }

        td, th {
            border: 1px solid #4F81BD;
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

def makeDelimetersVisible(result):
      result = result.replace("\t", "\\t")
      result = result.replace("\r", "\\r")
      result = result.replace("\n", "\\n")
      return result

class FormalTester:
    def __init__(self, pageTitle = ""):
        self.content = HTML_PREFIX
        self.content = self.content.replace("<#TITLE>", pageTitle)
        self.longPrint = False
        self.isOddRow = False
        self.numTests = 0

    def newSection(self, caption, desc, compilingPerson, tester):
        self.numTests = 0
        self.isOddRow = False
        self.compilingPerson = compilingPerson
        self.tester = tester
        self.testsHTML = RESULTS_TABLE_HEADER

        if caption != "":
            self.content += "<h1>" + caption + "</h1>\n"

        if desc != "":
            self.content += "<p>" + desc + \
                                      u" Výpis výsledků testu nemusí být z důvodu úspory místa zcela přesný, pro přesnou podobu je možné použít odkaz." + \
                                      u"<br><br>Testovaný server: <a href='" + SERVER_URL + "'>" + SERVER_URL + "</a><br>" + \
                                      "</p>\n"


    def closeSection(self):
        self.content += self.testsHTML + "</table>"
        self.testsHTML = u""

    def addTest(self, inputs, result, expectedResult, errorMessage = ""):
        #result = makeDelimetersVisible(result)
        #result = unicode(result)
        self.numTests = self.numTests + 1

        if isinstance(result, list):
            pom = expectedResult.splitlines()
            if set(result) == set(pom):
                status = "checked"
                print "   ok :", inputs, "-->", "\n".join(result)
                expectedResultMessage = u""
            else:
                status = ""
                expectedResultMessage = u" ≠ " + expectedResult
                print "chyba :", inputs, "-->", "\n".join(result), "<>", expectedResult, errorMessage
        else:
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
            self.testsHTML += '    <td align="center">' + str(self.numTests) + "</td>"
            self.testsHTML += "    <td>" + '<input type="checkbox" value=""' + status + ' \>' + "</td>"

            self.testsHTML += "    <td>" + inputs + "</td>"
            self.testsHTML += "    <td>" + str(result) + expectedResultMessage + "</td>" # →
            self.testsHTML += "    <td>" + errorMessage + "</td>"
            self.testsHTML += "</tr>\n"
        else:
            self.testsHTML += "<tr" + oddText + ">\n"
            self.testsHTML += '    <td align="center">' + str(self.numTests) + "</td>"
            self.testsHTML += "    <td>" + '<input type="checkbox" value=""' + status + ' \>' + "</td>"

            caption = urllib2.unquote(inputs)
            #caption = caption.encode("utf=8")
            self.testsHTML += '    <td><a href="' + SERVER_URL + inputs + '">'  + caption + "</a><br>"
            self.testsHTML += str(result) + expectedResultMessage + "<br>"
            if errorMessage != "":
                self.testsHTML += "    <td>" + errorMessage + "</td>"
            self.testsHTML += "</tr>\n"

        self.isOddRow = not self.isOddRow


    def loadAndAddTest(self, path, params, expectedValue):
        paramsList = params.split("&")
        query = []

        params = path + params
        try:
            result = urllib2.urlopen(SERVER_URL + params).read()
        except Exception as inst:
            result = str(inst)
        #result = "\n".join(result.splitlines())
        result = result.splitlines()
        params = params.decode("utf-8")
        self.addTest(params, result, expectedValue, "")

    def saveToHTML(self, fileName):
        with codecs.open(fileName, "w", "utf-8") as outFile:
            htmlContent = self.content + HTML_SUFFIX
            outFile.write(codecs.encode(htmlContent, "utf-8"))
            outFile.close()

def test():
    tester = FormalTester("Caption text", """Description text""", "Compiling person", "Tester")

    tester.addTest("OK test", "Test value", "Test value", "OK Test")
    tester.addTest("Fail test", "Wrong test value", "Test value", "Error message")
    tester.saveToHTML("sharedtools.html")


if __name__ == '__main__':
    test()
