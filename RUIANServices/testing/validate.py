# -*- coding: utf-8 -*-
__author__ = 'Augustyn'

import sharedtools
import urllib2
import urllib
import codecs

def test(testerParam = None):
    if testerParam == None:
        tester = sharedtools.FormalTester()
    else:
        tester = testerParam

    tester.newSection("Ověření funkčnosti služby Validate",
                """Tento test ověřuje funkčnost služby Validate, která slouží k ověření zadané adresy.
                Adresa je zadána pomocí jednotlivých prvků adresního místa.""",
                "Compiling person", "Tester")

    def addTest(path, params, expectedValue):
        paramsList = params.split("&")
        query = []
        if paramsList != [""]:
            for param in paramsList:
                v = param.split("=")
                query.append(v[0] + "=" + urllib.quote(codecs.encode(v[1], "utf-8")))
            params = "&".join(query)
        else:
            params = ""

        params = path + params
        try:
            result = urllib2.urlopen(sharedtools.SERVER_URL + params).read()
        except Exception as inst:
            result = str(inst)
        #result = result.strip()
        result = urllib.quote(codecs.encode(result, "utf-8"))
        params = params.decode("utf-8")
        tester.addTest(params, result, expectedValue, "")

    addTest("/Validate/text?", "Street=Severní", "False")
    addTest("/Validate/text?", "Street=Severní&HouseNumber=507", "False")
    addTest("/Validate/text?", "Street=Severní&Locality=Kladno&HouseNumber=507", "False")
    addTest("/Validate/text?", "Street=Severn%C3%AD&RecordNumber=25", "False")
    addTest("/Validate/text?", "Street=Fillova&HouseNumber=980&OrientationNumber=5", "False")
    
    addTest("/Validate/text?", "Street=Severní&Locality=Kladno&HouseNumber=507&ZIPCode=27204&LocalityPart=Kladno", "True")
    addTest("/Validate/text?", "Street=Severní&Locality=Kladno&HouseNumber=507&ZIPCode=27206&LocalityPart=Kladno", "False")
    addTest("/Validate/text?", "Street=Žižkova&Locality=Jirkov&ZIPCode=43111&LocalityPart=Jirkov&RecordNumber=263", "True")
    addTest("/Validate/text?", "Street=Rodinná&Locality=Havířov&HouseNumber=1003&ZIPCode=73601&LocalityPart=Bludovice&OrientationNumber=25", "True")
    addTest("/Validate/text?", "Street=U%20Jeslí&Locality=Broumov&HouseNumber=222&ZIPCode=55001&LocalityPart=Nové%20Město", "True")
    addTest("/Validate/text?", "Street=Žižkova&Locality=Jirkov&ZIPCode=43111&LocalityPart=Jirkov&RecordNumber=273", "False")
    addTest("/Validate/text?", "Street=Rodinná&Locality=Havířov&HouseNumber=1027&ZIPCode=73601&LocalityPart=Bludovice", "False")
    addTest("/Validate/text?", "Street=U%20Jeslí&Locality=Broumov&HouseNumber=226&ZIPCode=55001&LocalityPart=Nové%20Město", "False")
    
    addTest("/Validate/text?", "HouseNumber=507a", "False")
    addTest("/Validate/text?", "RecordNumber=145s", "False")
    addTest("/Validate/text?", "OrientationNumber=12a", "False")
    addTest("/Validate/text?", "ZIPCode=27206r", "False")
    addTest("/Validate/text?", "", "False")
    
    

    tester.closeSection()

    if testerParam == None:
        tester.saveToHTML("Validate.html")


if __name__ == '__main__':
    sharedtools.setupUTF()
    test()