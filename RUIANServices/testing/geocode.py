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

    tester.loadAndAddTest("/Geocode/text?", "AddressPlaceId=1408739", "1033052.61, 766195.05")
    tester.loadAndAddTest("/Geocode/text?", "AddressPlaceId=20388802", "1056492.96, 529426.07")
    tester.loadAndAddTest("/Geocode/text?", "AddressPlaceId=8123934", "1098618.98, 568885.13")
    tester.loadAndAddTest("/Geocode/text?", "AddressPlaceId=8150656", "1086263.12, 572291.20")
    tester.loadAndAddTest("/Geocode/text?", "AddressPlaceId=140k", "")
 
    
    tester.loadAndAddTest("/Geocode/text?", "SearchText=Blahoslavova%201710,%20Louny", "1007250.67, 781971.94")
    tester.loadAndAddTest("/Geocode/text?", "SearchText=U%20Kam,%20Vys", "1051222.31, 759801.78\n1051248.61, 759804.26\n1051154.97, 759793.10")

    tester.loadAndAddTest("/Geocode/text?", "SearchText=Mramorov%C3%A1,%20Tet%C3%ADn", "1055481.79, 767602.15\n1055502.63, 767570.69\n1055447.02, 767576.82")
    tester.loadAndAddTest("/Geocode/text?", "SearchText=12", "")
    
    
    tester.loadAndAddTest("/Geocode/text?", "Street=Hromadova&Locality=Kladno&HouseNumber=2741&ZIPCode=27201&LocalityPart=Kladno", "1033052.61, 766195.05")
    tester.loadAndAddTest("/Geocode/text?", "Street=Mari%C3%A1nsk%C3%A1&Locality=Su%C5%A1ice&HouseNumber=67&ZIPCode=34201&LocalityPart=Su%C5%A1ice%20III", "1128217.51, 820609.28")
    tester.loadAndAddTest("/Geocode/text?", "Street=Dlouh%C3%A1&Locality=Terez%C3%ADn&HouseNumber=22&ZIPCode=41155&LocalityPart=Terez%C3%ADn", "993630.00, 755650.00")
    tester.loadAndAddTest("/Geocode/text?", "Street=Osadn%C3%AD&Locality=Rumburk&HouseNumber=1456&ZIPCode=40801&LocalityPart=Rumburk%201&OrientationNumber=12", "947618.24, 719309.30")
    
    tester.loadAndAddTest("/Geocode/text?", "HouseNumber=980f", "")
    tester.loadAndAddTest("/Geocode/text?", "HouseNumber=f", "")
    
    tester.loadAndAddTest("/Geocode/text?", "ZIPCode=14000a", "")
    tester.loadAndAddTest("/Geocode/text?", "ZIPCode=a", "")
    
    tester.loadAndAddTest("/Geocode/text?", "OrientationNumber=12a", "")
    tester.loadAndAddTest("/Geocode/text?", "OrientationNumber=a", "")
    
    tester.loadAndAddTest("/Geocode/text?", "RecordNumber=14d", "")
    tester.loadAndAddTest("/Geocode/text?", "RecordNumber=d", "")
    
    tester.loadAndAddTest("/Geocode/text?", "", "")
    
    
    
    tester.closeSection()

    if testerParam == None:
        tester.saveToHTML("Geocode.html")


if __name__ == '__main__':
    sharedtools.setupUTF()
    test()


