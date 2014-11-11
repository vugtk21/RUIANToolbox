# -*- coding: utf-8 -*-
__author__ = 'Augustyn'

import sharedtools
import urllib2
import urllib
import codecs

def test(testerParam = None):
    if testerParam == None:
        tester = sharedtools.FormalTester("Ověření funkčnosti služby ValidateAddressID")
    else:
        tester = testerParam

    tester.newSection("Ověření funkčnosti služby ValidateAddressID",
"""Tento test ověřuje funkčnost služby ValidateAddressID, která ověřuje existenci zadaného identifikátoru adresy RÚIAN v databázi.""",
                "Compiling person", "Tester")

    def addTest(path, expectedValue):
        try:
            result = urllib2.urlopen(sharedtools.SERVER_URL + path).read()
        except Exception as inst:
            result = str(inst)
        #result = result.strip()
        result = urllib.quote(codecs.encode(result, "utf-8"))
        tester.addTest(path, result, expectedValue, "")

    addTest("/ValidateAddressId/txt?AddressPlaceId=1408739", "True")
    addTest("/ValidateAddressId/txt?AddressPlaceId=18480", "False")
    
    addTest("/ValidateAddressId/txt?AddressPlaceId=1498011", "True")
    addTest("/ValidateAddressId/txt?AddressPlaceId=40094944", "True")
    addTest("/ValidateAddressId/txt?AddressPlaceId=11505095", "True")
    addTest("/ValidateAddressId/txt?AddressPlaceId=1550080", "True")
    addTest("/ValidateAddressId/txt?AddressPlaceId=11390808", "True")
    addTest("/ValidateAddressId/txt?AddressPlaceId=150", "False")
    addTest("/ValidateAddressId/txt?AddressPlaceId=6084810", "False")
    addTest("/ValidateAddressId/txt?AddressPlaceId=18753880", "False")
    
    addTest("/ValidateAddressId/txt?AddressPlaceId=12j", "False")
    addTest("/ValidateAddressId/txt?AddressPlaceId=k", "False")
    
    tester.closeSection()

    if testerParam == None:
        tester.saveToHTML("ValidateAddressID.html")


if __name__ == '__main__':
    sharedtools.setupUTF()
    test()