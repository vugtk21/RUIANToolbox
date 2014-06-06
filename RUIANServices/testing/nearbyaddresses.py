# -*- coding: utf-8 -*-
__author__ = 'Augustyn'

import sharedtools
import urllib2
import urllib
import codecs

def test(testerParam = None):
    if testerParam == None:
        tester = sharedtools.FormalTester("Ověření funkčnosti služby NearByAddresses")
    else:
        tester = testerParam
    tester.newSection("Ověření funkčnosti služby NearByAddresses",
"""Tento test ověřuje funkčnost služby NearByAddresses, která umožňuje vyhledat adresní místa v okolí
zadaných souřadnic do určité vzdálenosti. Vrací záznamy databáze RÚIAN setříděné podle vzdálenosti od zadaných souřadnic.""",
                "Compiling person", "Tester")

    def addTest(path, expectedValue):
        try:
            result = urllib2.urlopen(sharedtools.SERVER_URL + path).read()
        except Exception as inst:
            result = str(inst)
        #result = result.strip()
        result = urllib.quote(codecs.encode(result, "utf-8"))
        tester.addTest(path, result, expectedValue, "")

    addTest("/NearbyAddresses/txt/1030730/655130/100", "č.p. 22, 50315 Pšánky")
    addTest("/NearbyAddresses/txt/1025770/625350/200", "č.p. 54, 55203 Říkov")
    
    addTest("/NearbyAddresses/txt/1026662/560670/300", "Kamenička 22, 79069 Bílá Voda\nKamenička č.ev. 31, 79069 Bílá Voda\nKamenička 29, 79069 Bílá Voda")
    addTest("/NearbyAddresses/txt/1066880/697180/500", "Červený Hrádek 44, 28504 Bečváry\nČervený Hrádek 111, 28504 Bečváry")
    
    tester.closeSection()

    if testerParam == None:
        tester.saveToHTML("NearByAddresses.html")


if __name__ == '__main__':
    import sys
    reload(sys)
    sys.setdefaultencoding('utf-8')

    test()


