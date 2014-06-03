# -*- coding: utf-8 -*-
__author__ = 'Augustyn'

import sharedtools
import urllib2
import urllib
import codecs

def buildParamString(street, houseNumber, recordNumber, orientationNumber, zipCode, locality, localityPart, districtNumber):
    url = u"/CompileAddress?"
    params = {
        "Street"            : street,
        "HouseNumber"       : houseNumber,
        "RecordNumber"      : recordNumber,
        "OrientationNumber" : orientationNumber,
        "ZipCode"           : zipCode,
        "Locality"          : locality,
        "LocalityPart"      : localityPart,
        "DistrictNumber"    : districtNumber
    }

    for key in params:
        url += key + "=" + urllib.quote(codecs.encode(params[key], "utf-8")) + "&"

    return url

def test():
    tester = sharedtools.FormalTester("Ověření funkčnosti služby Validate",
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


    tester.saveToHTML("validate.html")


if __name__ == '__main__':
    import sys
    reload(sys)
    sys.setdefaultencoding('utf-8')

    test()

