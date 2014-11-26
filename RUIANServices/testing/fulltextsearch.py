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

        
    tester.loadAndAddTest("/FullTextSearch/text/?", "SearchText=12&ExtraInformation=id", "")
    tester.loadAndAddTest("/FullTextSearch/text/?", "SearchText=&ExtraInformation=id", "")
    tester.loadAndAddTest("/FullTextSearch/textToOneRow/?", "SearchText=V%20Hlink%C3%A1ch,%20Vys&ExtraInformation=id", "72405651, V Hlinkách 265, 26716 Vysoký Újezd\n41446593, V Hlinkách 269, 26716 Vysoký Újezd\n42535581, V Hlinkách 274, 26716 Vysoký Újezd\n40973298, V Hlinkách 261, 26716 Vysoký Újezd\n41447018, V Hlinkách 268, 26716 Vysoký Újezd")
    tester.loadAndAddTest("/FullTextSearch/textToOneRow/?", "SearchText=U%20Kam,%20Vys&ExtraInformation=id", "41326474, U Kamene 181, 26716 Vysoký Újezd\n42616123, U Kamene 182, 26716 Vysoký Újezd\n73185396, U Kamene 180, 26716 Vysoký Újezd")
    tester.loadAndAddTest("/FullTextSearch/textToOneRow/?", "SearchText=Mramor,%20Tet%C3%ADn&ExtraInformation=id", "1521209, Mramorová 234, 26601 Tetín\n1521292, Mramorová 243, 26601 Tetín\n1521225, Mramorová 236, 26601 Tetín")
    tester.loadAndAddTest("/FullTextSearch/textToOneRow/?", "SearchText=Fill,%20Praha&ExtraInformation=id", "21867178, Fillova 990/1, Krč, 14000 Praha 4\n21867054, Fillova 980/5, Krč, 14000 Praha 4\n21868107, Fillova 1084/11, Krč, 14000 Praha 4\n21867038, Fillova 979/7, Krč, 14000 Praha 4\n21867160, Fillova 989/3, Krč, 14000 Praha 4")
    
    tester.loadAndAddTest("/FullTextSearch/text/?", "SearchText=V%20Hlink%C3%A1ch,%20Vys&ExtraInformation=id", "72405651\nV Hlinkách 265\n26716 Vysoký Újezd\n41446593\nV Hlinkách 269\n26716 Vysoký Újezd\n42535581\nV Hlinkách 274\n26716 Vysoký Újezd\n40973298\nV Hlinkách 261\n26716 Vysoký Újezd\n41447018\nV Hlinkách 268\n26716 Vysoký Újezd")
    tester.loadAndAddTest("/FullTextSearch/text/?", "SearchText=U%20Kam,%20Vys&ExtraInformation=id", "41326474\nU Kamene 181\n26716 Vysoký Újezd\n42616123\nU Kamene 182\n26716 Vysoký Újezd\n73185396\nU Kamene 180\n26716 Vysoký Újezd")
    tester.loadAndAddTest("/FullTextSearch/text/?", "SearchText=Mramor,%20Tet%C3%ADn&ExtraInformation=id", "1521209\nMramorová 234\n26601 Tetín\n1521292\nMramorová 243\n26601 Tetín\n1521225\nMramorová 236\n26601 Tetín")
    tester.loadAndAddTest("/FullTextSearch/text/?", "SearchText=Fill,%20Praha&ExtraInformation=id", "21867178\nFillova 990/1\nKrč\n14000 Praha 4\n21867054\nFillova 980/5\nKrč\n14000 Praha 4\n21868107\nFillova 1084/11\nKrč\n14000 Praha 4\n21867038\nFillova 979/7\nKrč\n14000 Praha 4\n21867160\nFillova 989/3\nKrč\n14000 Praha 4")
     
     
    
    
    tester.closeSection()


    if testerParam == None:
        tester.saveToHTML("FulltextSearch.html")


if __name__ == '__main__':
    sharedtools.setupUTF()
    test()