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
    tester = sharedtools.FormalTester("Ověření funkčnosti služby CompileAddress",
                """
Tento test ověřuje sestavení zápisu adresy ve standardizovaném tvaru podle § 6 vyhlášky č. 359/2011 Sb.,
kterou se provádí zákon č. 111/2009 Sb., o základních registrech, ve znění zákona č. 100/2010 Sb.
Adresní místo lze zadat buď pomocí jeho identifikátoru RÚIAN, textového řetězce adresy nebo jednotlivých prvků adresy.
                """,
                "Compiling person", "Tester")

    def addTest(street, houseNumber, recordNumber, orientationNumber, zipCode, locality, localityPart, districtNumber, expectedValue):
        params = buildParamString(street, houseNumber, recordNumber, orientationNumber, zipCode, locality, localityPart, districtNumber)
        try:
            result = urllib2.urlopen(sharedtools.SERVER_URL + params).read()
        except Exception as inst:
            result = str(inst)
        #result = "aaa" #result.decode("utf-8")
        #expectedValue = "ev"
        params = params.decode("utf-8")
        #expectedValue = expectedValue.decode("utf-8")
        tester.addTest(params, result, expectedValue, "")

    addTest(u"Arnošta Valenty", u"670", u"", u"31", u"19800", u"Praha", u"Černý Most", u"9", u"Arnošta Valenty 670/31\nČerný Most\n198 00 Praha 9")
    addTest(u"Arnošta Valenty", u"670", u"", u"", u"198 00", u"Praha", u"Černý Most", u"9", u'Arnošta Valenty 670\nČerný Most\n198 00 Praha 9')
    addTest(u"Medová", u"", u"30", u"", u"10400", u"Praha", u"Křeslice",  u"10", u'Medová č. ev. 30\nKřeslice\n104 00 Praha 10')
    addTest(u"", u"", u"42", u"", u"10400", u"Praha", u"Křeslice", u"10", u'Křeslice č. ev. 42\n104 00 Praha 10')
    addTest(u"Lhenická", u"1120", u"", u"1", u"37005", u"České Budějovice", u"České Budějovice 2", u"", u'Lhenická 1120/1\nČeské Budějovice 2\n370 05 České Budějovice')
    addTest(u'Lhenická', u'1120', u'', u'', u'370 05', u'České Budějovice', u'České Budějovice 2', u'', u'Lhenická 1120\nČeské Budějovice 2\n37005 České Budějovice')
    addTest(u'Lhenická', u'', u'12', u'', u'37005', u'České Budějovice', u'České Budějovice 2', u'', u'Lhenická č. ev. 12\nČeské Budějovice 2\n37005 České Budějovice')
    addTest(u'Žamberecká', u'339', u'', u'-', u'51601', u'Vamberk', u'Vamberk', u'', u'Žamberecká 339\n51601 Vamberk\n')
    addTest(u'Žamberecká', u'339', u'', u'1', u'51601', u'Vamberk', u'Vamberk', u'', u'Žamberecká 339/1\n51601 Vamberk')
    addTest(u'Žamberecká', u'', u'21', u'', u'51601', u'Vamberk', u'Vamberk', u'', u'Žamberecká č. ev. 21\n51601 Vamberk')
    addTest(u'', u'106', u'', u'', u'53333', u'Pardubice', u'Dražkovice', u'', u'Dražkovice 106\n53333 Pardubice')
    addTest(u'', u'106', u'', u'12', u'53333', u'Pardubice', u'Dražkovice', u'', u'Dražkovice 106/12\n53333 Pardubice')
    addTest(u'', u'', u'32', u'', u'53333', u'Pardubice', u'Dražkovice', u'', u'Dražkovice č. ev. 32\n53333 Pardubice')
    addTest(u'', u'111', u'', u'', u'50333', u'Praskačka', u'Praskačka', u'', u'č. p. 111\n50333 Praskačka')
    addTest(u'', u'111', u'', u'1', u'53333', u'Praskačka', u'Praskačka', u'', u'č .p. 111/1\n53333 Praskačka')
    addTest(u'', u'', u'32', u'', u'53333', u'Praskačka', u'Praskačka', u'', u'č .ev. 32\n53333 Pardubice')

    tester.saveToHTML("compileaddress.html")


if __name__ == '__main__':
    import sys
    reload(sys)
    sys.setdefaultencoding('utf-8')

    test()
