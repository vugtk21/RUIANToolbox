# -*- coding: utf-8 -*-
__author__ = 'Augustyn'

import sharedtools
import urllib2
import urllib
import codecs

def test():
    tester = sharedtools.FormalTester("Ověření funkčnosti služby NearByAddresses",
"""Tento test ověřuje funkčnost služby NearByAddresses, která umožňuje vyhledat adresní místa v okolí
zadaných souřadnic do určité vzdálenosti. Vrací záznamy databáze RÚIAN setříděné podle vzdálenosti od zadaných souřadnic.""",
                "Compiling person", "Tester")

    def addTest(path, expectedValue):
        try:
            result = urllib2.urlopen(sharedtools.SERVER_URL).read()
        except Exception as inst:
            result = str(inst)
        #result = result.strip()
        result = urllib.quote(codecs.encode(result, "utf-8"))
        tester.addTest(path, result, expectedValue, "")

    addTest("/NearbyAddresses/txt/1033000/766500/1000", "Mládežnická 841, 272 04 Kladno")

    tester.saveToHTML("NearByAddresses.html")


if __name__ == '__main__':
    import sys
    reload(sys)
    sys.setdefaultencoding('utf-8')

    test()


