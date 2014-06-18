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

        
    tester.loadAndAddTest("/FullTextSearch/txt/?", "SearchText=12", "")
    tester.loadAndAddTest("/FullTextSearch/txt/?", "SearchText=", "")
    tester.loadAndAddTest("/FullTextSearch/txt/?", "SearchText=V%20Hlink%C3%A1ch,%20Vys", "40973298, V Hlinkách 261, 26716 Vysoký Újezd\n72405651, V Hlinkách 265, 26716 Vysoký Újezd\n41446593, V Hlinkách 269, 26716 Vysoký Újezd\n42535581, V Hlinkách 274, 26716 Vysoký Újezd\n41447018, V Hlinkách 268, 26716 Vysoký Újezd")
    tester.loadAndAddTest("/FullTextSearch/txt/?", "SearchText=U%20Kam,%20Vys", "41326474, U Kamene 181, 26716 Vysoký Újezd\n42616123, U Kamene 182, 26716 Vysoký Újezd")
    tester.loadAndAddTest("/FullTextSearch/txt/?", "SearchText=Mramor,%20Tet%C3%ADn", "1521209 Mramorová 234, 26601 Tetín\n1521292 Mramorová 243, 26601 Tetín\n1521225 Mramorová 236, 26601 Tetín")
    tester.loadAndAddTest("/FullTextSearch/txt/?", "SearchText=Fill,%20Praha", "21867178, Fillova 990/1, Krč, 14000 Praha 4\n21867054, Fillova 980/5, Krč, 14000 Praha 4\n21868107, Fillova 1084/11, Krč, 14000 Praha 4\n21867038, Fillova 979/7, Krč, 14000 Praha 4\n21867160, Fillova 989/3, Krč, 14000 Praha 4")
     
     
    
    
    tester.closeSection()


    if testerParam == None:
        tester.saveToHTML("FulltextSearch.html")


if __name__ == '__main__':
    import sys
    reload(sys)
    sys.setdefaultencoding('utf-8')

    test()


