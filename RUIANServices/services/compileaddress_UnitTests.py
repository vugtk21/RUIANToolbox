# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
# Name:        compileaddress_UnitTests
# Purpose:     Module compileaddress unit tests implementation.
#
# Author:      Radek Augustýn
# Copyright:   (c) VUGTK, v.v.i. 2014
# License:     CC BY-SA 4.0
# -------------------------------------------------------------------------------

import unittest
import compileaddress as AT

addressCompileSamples = []

class TestGlobalFunctions(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testcompileAddress(self):
        for s in addressCompileSamples:
            self.assertEqual(
            AT.compileAddress(AT.TextFormat.plainText,
             s.street, s.houseNumber, s.recordNumber, s.orientationNumber, s.zipCode, s.locality, s.localityPart, s.districtNumber),
             s.textResult
        )

        pass

class AddressSample:
    def __init__(self, street, houseNumber, recordNumber, orientationNumber, zipCode, locality, localityPart, districtNumber, textResult):
        self.street = street
        self.houseNumber = houseNumber
        self.recordNumber = recordNumber
        self.orientationNumber = orientationNumber
        self.zipCode = zipCode
        self.locality = locality
        self.localityPart = localityPart
        self.districtNumber = districtNumber
        self.textResult = textResult

    def toXML(self):
        s = ""

        s += "http://www.vugtk.cz/euradin/services/rest"
        s += "/CompileAddress/txt?"
        s += "Street=" + self.street
        s += "&HouseNumber=" + self.houseNumber
        s += "&RecordNumber=" + self.recordNumber
        s += "&OrientationNumber=" + self.orientationNumber
        s += "&ZIPCode=" + self.zipCode
        s += "&Locality=" + self.locality
        s += "&LocalityPart=" + self.localityPart
        s += "&DistrictNumber=" + self.districtNumber
        s += "\n" + self.textResult + "\n"
        return s

addressCompileSamples.append(AddressSample(u"Arnošta Valenty", u"670", u"", u"31", u"19800", u"Praha", u"Černý Most", u"9", u"Arnošta Valenty 670/31\nČerný Most\n198 00 Praha 9"))
addressCompileSamples.append(AddressSample(u"Arnošta Valenty", u"670", u"", u"", u"198 00", u"Praha", u"Černý Most", u"9", u'Arnošta Valenty 670\nČerný Most\n198 00 Praha 9'))
addressCompileSamples.append(AddressSample(u"Medová", u"", u"30", u"", u"10400", u"Praha", u"Křeslice", u"10", u'Medová č. ev. 30\nKřeslice\n104 00 Praha 10'))
addressCompileSamples.append(AddressSample(u"", u"", u"42", u"", u"10400", u"Praha", u"Křeslice", u"10", u'Křeslice č. ev. 42\n104 00 Praha 10'))
addressCompileSamples.append(AddressSample(u"Lhenická", u"1120", u"", u"1", u"37005", u"České Budějovice", u"České Budějovice 2", u"", u'Lhenická 1120/1\nČeské Budějovice 2\n370 05 České Budějovice'))
addressCompileSamples.append(AddressSample(u'Lhenická', u'1120', u'', u'', u'370 05', u'České Budějovice', u'České Budějovice 2', u'', u'Lhenická 1120\nČeské Budějovice 2\n37005 České Budějovice'))
addressCompileSamples.append(AddressSample(u'Lhenická', u'', u'12', u'', u'37005', u'České Budějovice', u'České Budějovice 2', u'', u'Lhenická č. ev. 12\nČeské Budějovice 2\n37005 České Budějovice'))
addressCompileSamples.append(AddressSample(u'Žamberecká', u'339', u'', u'-', u'51601', u'Vamberk', u'Vamberk', u'', u'Žamberecká 339\n51601 Vamberk\n'))
addressCompileSamples.append(AddressSample(u'Žamberecká', u'339', u'', u'1', u'51601', u'Vamberk', u'Vamberk', u'', u'Žamberecká 339/1\n51601 Vamberk'))
addressCompileSamples.append(AddressSample(u'Žamberecká', u'', u'21', u'', u'51601', u'Vamberk', u'Vamberk', u'', u'Žamberecká č. ev. 21\n51601 Vamberk'))
addressCompileSamples.append(AddressSample(u'', u'106', u'', u'', u'53333', u'Pardubice', u'Dražkovice', u'', u'Dražkovice 106\n53333 Pardubice'))
addressCompileSamples.append(AddressSample(u'', u'106', u'', u'12', u'53333', u'Pardubice', u'Dražkovice', u'', u'Dražkovice 106/12\n53333 Pardubice'))
addressCompileSamples.append(AddressSample(u'', u'', u'32', u'', u'53333', u'Pardubice', u'Dražkovice', u'', u'Dražkovice č. ev. 32\n53333 Pardubice'))
addressCompileSamples.append(AddressSample(u'', u'111', u'', u'', u'50333', u'Praskačka', u'Praskačka', u'', u'č. p. 111\n50333 Praskačka'))
addressCompileSamples.append(AddressSample(u'', u'111', u'', u'1', u'53333', u'Praskačka', u'Praskačka', u'', u'č .p. 111/1\n53333 Praskačka'))
addressCompileSamples.append(AddressSample(u'', u'', u'32', u'', u'53333', u'Praskačka', u'Praskačka', u'', u'č .ev. 32\n53333 Pardubice'))

for s in addressCompileSamples:
    print s.toXML()

def main():
    unittest.main()

if __name__ == '__main__':
    main()
