# -*- coding: utf-8 -*-
__author__ = 'raugustyn'

import unittest
import RUIANServices.services.compileaddress_UnitTests

SERVER_URL = "http://www.vugtk.cz/euradin/services"

def buildCompileAddress(street, houseNumber, recordNumber, orientationNumber, zipCode, locality, localityPart, districtNumber):
    result = SERVER_URL + "/CompileAddress?"
    params = {
        "Street" : street,
        "HouseNumber" : houseNumber,
        "RecordNumber" : recordNumber,
        "OrientationNumber" : orientationNumber,
        "ZipCode" : zipCode,
        "Locality" : locality,
        "LocalityPart" : localityPart,
        "DistrictNumber" : districtNumber
    }

    for key in params:
        result += key + "=" + params[key] + "&"
    return result

class TestGlobalFunctions(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testGeocode(self):

        pass

    def testCompileAddress(self):
        self.assertEqual(
            buildCompileAddress(u"Arnošta Valenty", u"670", u"", u"31", u"19800", u"Praha", u"Černý Most", u"9"),
            u"Arnošta Valenty 670/31\nČerný Most\n198 00 Praha 9"
        )
        self.assertEqual(
            buildCompileAddress(u"Arnošta Valenty", u"670", u"", u"", u"198 00", u"Praha", u"Černý Most", u"9"),
            u'Arnošta Valenty 670\nČerný Most\n198 00 Praha 9'
        )
        self.assertEqual(
            buildCompileAddress(u"Medová", u"", u"30", u"", u"10400", u"Praha", u"Křeslice"),
            u"10", u'Medová č. ev. 30\nKřeslice\n104 00 Praha 10'
        )
        self.assertEqual(
            buildCompileAddress(u"", u"", u"42", u"", u"10400", u"Praha", u"Křeslice", u"10"),
            u'Křeslice č. ev. 42\n104 00 Praha 10'
        )
        self.assertEqual(
            buildCompileAddress(u"Lhenická", u"1120", u"", u"1", u"37005", u"České Budějovice", u"České Budějovice 2", u""),
            u'Lhenická 1120/1\nČeské Budějovice 2\n370 05 České Budějovice'
        )
        self.assertEqual(
            buildCompileAddress(u'Lhenická', u'1120', u'', u'', u'370 05', u'České Budějovice', u'České Budějovice 2', u''),
            u'Lhenická 1120\nČeské Budějovice 2\n37005 České Budějovice'
        )
        self.assertEqual(
            buildCompileAddress(u'Lhenická', u'', u'12', u'', u'37005', u'České Budějovice', u'České Budějovice 2', u''),
            u'Lhenická č. ev. 12\nČeské Budějovice 2\n37005 České Budějovice'
        )
        self.assertEqual(
            buildCompileAddress(u'Žamberecká', u'339', u'', u'-', u'51601', u'Vamberk', u'Vamberk', u''),
            u'Žamberecká 339\n51601 Vamberk\n'
        )
        self.assertEqual(
            buildCompileAddress(u'Žamberecká', u'339', u'', u'1', u'51601', u'Vamberk', u'Vamberk', u''),
            u'Žamberecká 339/1\n51601 Vamberk'
        )
        self.assertEqual(
            buildCompileAddress(u'Žamberecká', u'', u'21', u'', u'51601', u'Vamberk', u'Vamberk', u''),
            u'Žamberecká č. ev. 21\n51601 Vamberk'
        )
        self.assertEqual(
            buildCompileAddress(u'', u'106', u'', u'', u'53333', u'Pardubice', u'Dražkovice', u''),
            u'Dražkovice 106\n53333 Pardubice'
        )
        self.assertEqual(
            buildCompileAddress(u'', u'106', u'', u'12', u'53333', u'Pardubice', u'Dražkovice', u''),
            u'Dražkovice 106/12\n53333 Pardubice'
        )
        self.assertEqual(
            buildCompileAddress(u'', u'', u'32', u'', u'53333', u'Pardubice', u'Dražkovice', u''),
            u'Dražkovice č. ev. 32\n53333 Pardubice'
        )
        self.assertEqual(
            buildCompileAddress(u'', u'111', u'', u'', u'50333', u'Praskačka', u'Praskačka', u''),
            u'č. p. 111\n50333 Praskačka'
        )
        self.assertEqual(
            buildCompileAddress(u'', u'111', u'', u'1', u'53333', u'Praskačka', u'Praskačka', u''),
            u'č .p. 111/1\n53333 Praskačka'
        )
        self.assertEqual(
            buildCompileAddress(u'', u'', u'32', u'', u'53333', u'Praskačka', u'Praskačka', u''),
            u'č .ev. 32\n53333 Pardubice'
        )

        pass

    def testFullTextSearch(self):
        pass

    def testValidate(self):
        pass

    def testValidateAddressId(self):
        pass

    def testNearByAddresses(self):
        pass


if __name__ == '__main__':
    unittest.main()

