# -*- coding: utf-8 -*-
__author__ = 'Augustyn'

import sharedtools
import urllib2
import urllib
import codecs

def test():
    tester = sharedtools.FormalTester("Ověření funkčnosti služby ValidateAddressID",
"""Tento test ověřuje funkčnost služby ValidateAddressID, která ověřuje existenci zadaného identifikátoru adresy RÚIAN v databázi.""",
                "Compiling person", "Tester")

    def addTest(path, expectedValue):
        try:
            result = urllib2.urlopen(sharedtools.SERVER_URL).read()
        except Exception as inst:
            result = str(inst)
        #result = result.strip()
        result = urllib.quote(codecs.encode(result, "utf-8"))
        tester.addTest(path, result, expectedValue, "")

    addTest("/ValidateAddressId/txt/1408739", "True")
    addTest("/ValidateAddressId/txt/18480", "False")

    tester.saveToHTML("ValidateAddressID.html")


if __name__ == '__main__':
    import sys
    reload(sys)
    sys.setdefaultencoding('utf-8')

    test()

