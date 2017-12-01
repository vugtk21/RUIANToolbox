# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        htmllog_tests
# Purpose:     Test htmllog module routines.
#
# Author:      Radek Augustýn
# Copyright:   (c) VUGTK, v.v.i. 2014
# License:     CC BY-SA 4.0
#-------------------------------------------------------------------------------

import downloader.htmllog
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
        htmlLog = downloader.htmllog.HtmlLog()
        htmlLog.save(self.FILENAME)


if __name__ == '__main__':
    #unittest.main()
    os.remove("test.html")

    htmlLog = downloader.htmllog.HtmlLog()
    htmlLog.htmlCode = "<div>Info 1 verze 0</div>"
    htmlLog.save("test.html")

    htmlLog.htmlCode = "<div>Info 1 verze 0.1</div>"
    htmlLog.save("test.html")

    htmlLog.htmlCode = "<div>Info 1 verze 0.2</div>"
    htmlLog.save("test.html")

    htmlLog.closeSection("test.html")

    htmlLog = downloader.htmllog.HtmlLog()
    htmlLog.htmlCode = "<div>Info 2 verze 0</div>"
    htmlLog.save("test.html")

    htmlLog.htmlCode = "<div>Info 2 verze 1</div>"
    htmlLog.save("test.html")

    htmlLog.htmlCode = "<div>Info 2 verze 2</div>"
    htmlLog.save("test.html")
    htmlLog.closeSection("test.html")
