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
        for param in paramsList:
            v = param.split("=")
            query.append(v[0] + "=" + urllib.quote(codecs.encode(v[1], "utf-8")))
        params = "&".join(query)

        params = path + params
        try:
            result = urllib2.urlopen(sharedtools.SERVER_URL + params).read()
        except Exception as inst:
            result = str(inst)
        #result = result.strip()
        result = urllib.quote(codecs.encode(result, "utf-8"))
        params = params.decode("utf-8")
        tester.addTest(params, result, expectedValue, "")

    addTest("/Validate/txt?", "Street=Severní&Locality=Kladno&HouseNumber=507", "True")
    addTest("/Validate/txt?", "Street=Severní&Locality=Kladno&HouseNumber=507&ZIPCode=27204&LocalityPart=Kladno", "True")
    addTest("/Validate/txt?", "Street=Severní&Locality=Kladno&HouseNumber=507&ZIPCode=27206&LocalityPart=Kladno", "False")
    addTest("/Validate/txt?", "Street=Severní&Locality=Kladno&HouseNumber=120", "False")
    addTest("/Validate/txt?", "Street=%C5%BDi%C5%BEkova&Locality=Jirkov&ZIPCode=43111&LocalityPart=Jirkov&RecordNumber=263", "True")
    addTest("/Validate/txt?", "Street=Rodinn%C3%A1&Locality=Hav%C3%AD%C5%99ov&HouseNumber=1003&ZIPCode=73601&LocalityPart=Bludovice&OrientationNumber=25", "True")
    addTest("/Validate/txt?", "Street=U%20Jesl%C3%AD&Locality=Broumov&HouseNumber=222&ZIPCode=55001&LocalityPart=Nov%C3%A9%20M%C4%9Bsto", "True")
    addTest("/Validate/txt?", "Street=%C5%BDi%C5%BEkova&Locality=Jirkov&ZIPCode=43111&LocalityPart=Jirkov&RecordNumber=273", "False")
    addTest("/Validate/txt?", "Street=Rodinn%C3%A1&Locality=Hav%C3%AD%C5%99ov&HouseNumber=1027&ZIPCode=73601&LocalityPart=Bludovice", "False")
    addTest("/Validate/txt?", "Street=U%20Jesl%C3%AD&Locality=Broumov&HouseNumber=226&ZIPCode=55001&LocalityPart=Nov%C3%A9%20M%C4%9Bsto", "False")

    tester.closeSection()

    if testerParam == None:
        tester.saveToHTML("Validate.html")


if __name__ == '__main__':
    import sys
    reload(sys)
    sys.setdefaultencoding('utf-8')

    test()

