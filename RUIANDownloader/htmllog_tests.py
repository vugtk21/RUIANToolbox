# -*- coding: utf-8 -*-
__author__ = 'Augustyn'

import htmllog
import unittest
import os

def getFileContent(fileName):
    with open(fileName, "r") as f:
        lines = f.read()
        f.close()
    return lines


class TestInfoFile(unittest.TestCase):
    FILENAME = "test.html"

    def tearDown(self):
        os.remove(self.FILENAME)
        pass

    def testSave(self):
        """ Tests Save and consequently Init """
        htmlLog = htmllog.HtmlLog()
        htmlLog.save(self.FILENAME)

        fileContent = getFileContent(self.FILENAME).replace(os.linesep, "\n")
        print(len(htmlLog.HTML_TEMPLATE))
        print(len(fileContent))
        self.assertEqual(htmlLog.HTML_TEMPLATE,  fileContent,  "File not saved properly")
        pass

if __name__ == '__main__':
    #unittest.main()
    os.remove("test.html")

    htmlLog = htmllog.HtmlLog()
    htmlLog.htmlCode = "<div>Info 1 verze 0</div>"
    htmlLog.save("test.html")

    htmlLog.htmlCode = "<div>Info 1 verze 0.1</div>"
    htmlLog.save("test.html")

    htmlLog.htmlCode = "<div>Info 1 verze 0.2</div>"
    htmlLog.save("test.html")

    htmlLog.closeSection("test.html")

    htmlLog = htmllog.HtmlLog()
    htmlLog.htmlCode = "<div>Info 2 verze 0</div>"
    htmlLog.save("test.html")

    htmlLog.htmlCode = "<div>Info 2 verze 1</div>"
    htmlLog.save("test.html")

    htmlLog.htmlCode = "<div>Info 2 verze 2</div>"
    htmlLog.save("test.html")
    htmlLog.closeSection("test.html")
