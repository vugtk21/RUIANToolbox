# -*- coding: utf-8 -*-
__author__ = 'Augustyn'

import sharedtools
import urllib2
import urllib
import codecs

def test(testerParam = None):
    if testerParam == None:
        tester = sharedtools.FormalTester("Ověření funkčnosti služby Geocode")
    else:
        tester = testerParam
    tester.newSection("Ověření funkčnosti služby Geocode",
                """Tento test ověřuje funkčnost služby Geocode, která slouží získání souřadnic zadaného adresního místa.
                Adresní místo zadáme buď pomocí jeho identifikátoru RÚIAN nebo pomocí textového řetězce adresy..
                 Textový řetězec adresy může být nestandardně formátován nebo může být i neúplný.""",
                "Compiling person", "Tester")

    tester.loadAndAddTest("/Geocode/txt?", "AddressPlaceId=1408739", "1033052.61, 766195.05")
    tester.loadAndAddTest("/Geocode/txt?", "SearchText=Hromadova%202741%20Kladno", "1033052.61, 766195.05")
    tester.loadAndAddTest("/Geocode/txt?", "Street=Hromadova&Locality=Kladno&HouseNumber=2741&ZIPCode=27201&LocalityPart=Kladno", "1033052.61, 766195.05")
    tester.closeSection()

    if testerParam == None:
        tester.saveToHTML("Geocode.html")


if __name__ == '__main__':
    import sys
    reload(sys)
    sys.setdefaultencoding('utf-8')

    test()


