# -*- coding: utf-8 -*-
__author__ = 'Augustyn'

import sharedtools
import urllib2
import urllib
import codecs

def test(testerParam = None):
    if testerParam == None:
        tester = sharedtools.FormalTester("Ověření funkčnosti služby FullTextSearch")
    else:
        tester = testerParam

    tester.newSection("Ověření funkčnosti služby FullTextSearch",
                """Tento test ověřuje funkčnost služby FullTextSearch, která slouží k nalezení a zobrazení seznamu
                 pravděpodobných adres na základě textového řetězce adresy.
                 Textový řetězec adresy může být nestandardně formátován nebo může být i neúplný.""",
                "Compiling person", "Tester")

    tester.loadAndAddTest("/FullTextSearch/txt/?", "SearchText=Severn%C3%AD,Kladno",
        "Severní 507, 272 04 Kladno\nSeverní 508, 272 04 Kladno\nSeverní 509, 272 04 Kladno")
    tester.loadAndAddTest("/FullTextSearch/txt/?", "SearchText=Severni%20Kladno",
        "Severní 507, 272 04 Kladno\nSeverní 508, 272 04 Kladno\nSeverní 509, 272 04 Kladno")
    tester.loadAndAddTest("/FullTextSearch/txt/?", "SearchText=Sev.%20Kladno",
        "Severní 507, 272 04 Kladno\nSeverní 508, 272 04 Kladno\nSeverní 509, 272 04 Kladno")
    tester.loadAndAddTest("/FullTextSearch/txt/?", "SearchText=Severni%20Klad",
        "Severní 507, 272 04 Kladno\nSeverní 508, 272 04 Kladno\nSeverní 509, 272 04 Kladno")
    tester.loadAndAddTest("/FullTextSearch/txt/?", "SearchText=Ml%C3%A1de%C5%BEnick%C3%A1%20Kladno",
        "Mládežnická 841, 272 04 Kladno\nMládežnická 842, 272 04 Kladno")
    tester.loadAndAddTest("/FullTextSearch/txt/?", "SearchText=Mladeznicka%20Kladno",
        "Mládežnická 841, 272 04 Kladno\nMládežnická 842, 272 04 Kladno")
    tester.loadAndAddTest("/FullTextSearch/txt/?", "SearchText=Kladruby", "č.ev. 11, Kladruby, 258 01\nč.p. 95, Kladruby, 258 01")
    tester.loadAndAddTest("/FullTextSearch/txt/?", "SearchText=V.%20Dub%C3%AD%20Kladno",
        "V. Sembdnera 611, Dubí, 272 03 Kladno\nV. Špály 571, Dubí, 272 03 Kladno")
    tester.loadAndAddTest("/FullTextSearch/txt/?", "SearchText=V%C3%A1c%20Kladno",
        "Václava Řacha 1352, Švermov, 273 09 Kladno\nVáclavova 1678, 272 01 Kladno\nVáclava Millera 163, Rozdělov, 272 04 Kladno")
    tester.loadAndAddTest("/FullTextSearch/txt/?", "SearchText=V%20Kladno%20Kladno",
        "Václavova 1678, 272 01 Kladno\nV. Burgra 131, 272 04 Kladno\nV. Burgra 132, 272 04 Kladno")
    tester.closeSection()


    if testerParam == None:
        tester.saveToHTML("FulltextSearch.html")


if __name__ == '__main__':
    import sys
    reload(sys)
    sys.setdefaultencoding('utf-8')

    test()


