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
        #result = urllib.quote(codecs.encode(result, "utf-8"))
        result = "\n".join(result.splitlines())
        tester.addTest(path, result, expectedValue, "")

    addTest("/NearbyAddresses/textToOneRow/655180/1030800/50", "č.p. 22, 50315 Pšánky")
    addTest("/NearbyAddresses/textToOneRow/625350/1025770/200", "č.p. 54, 55203 Říkov")
    addTest("/NearbyAddresses/textToOneRow/724948/1007742/65", "č.p. 42, 27735 Kanina\nč.p. 47, 27735 Kanina")
    addTest("/NearbyAddresses/textToOneRow/560670/1026662/80", "Kamenička č.ev. 31, 79069 Bílá Voda")
    addTest("/NearbyAddresses/textToOneRow/697180/1066880/120", "Červený Hrádek 44, 28504 Bečváry")
    
    addTest("/NearbyAddresses/text/655180/1030800/50", "č.p. 22\n50315 Pšánky")
    addTest("/NearbyAddresses/text/625350/1025770/200", "č.p. 54\n55203 Říkov")   
    addTest("/NearbyAddresses/text/724948/1007742/65? ", "č.p. 42\n27735 Kanina\nč.p. 47\n27735 Kanina")
    addTest("/NearbyAddresses/text/560670/1026662/80", "Kamenička č.ev. 31\n79069 Bílá Voda")
    addTest("/NearbyAddresses/text/697180/1066880/120", "Červený Hrádek 44\n28504 Bečváry")
    
    addTest("/NearbyAddresses/text/a/1025770/200", "")
    addTest("/NearbyAddresses/text/625350/b/200", "")
    addTest("/NearbyAddresses/text/625350/1025770/c", "")
    addTest("/NearbyAddresses/text/a/b/c", "")
    addTest("/NearbyAddresses/text/a/b/200", "")
    addTest("/NearbyAddresses/text/625350/b/c", "")
    addTest("/NearbyAddresses/text/a/1025770/c", "")
    
    
    tester.closeSection()

    if testerParam == None:
        tester.saveToHTML("NearByAddresses.html")


if __name__ == '__main__':
    sharedtools.setupUTF()
    test()