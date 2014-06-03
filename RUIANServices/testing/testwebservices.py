# -*- coding: utf-8 -*-
__author__ = 'raugustyn'

import unittest
import urllib2
import urllib
import codecs
#import RUIANServices.services.compileaddress_UnitTests

SERVER_URL = "http://www.vugtk.cz/euradin/services/rest.py"

def downloadURL(url):
    return urllib2.urlopen(url).read()

def downloadCompiledAddress(street, houseNumber, recordNumber, orientationNumber, zipCode, locality, localityPart, districtNumber):
    url = u"/CompileAddress?"
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
        url += key + "=" + params[key] + "&"

    url = codecs.encode(url, "utf-8")
    url = SERVER_URL + url
    return downloadURL(url)

class TestGlobalFunctions(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testGeocode(self):
        self.assertEqual(downloadURL("/Geocode/txt?AddressPlaceId=1408739"), "1033052.61, 766195.05")
        self.assertEqual(downloadURL("/Geocode/txt?SearchText=Hromadova%202741%20Kladno"), "1033052.61, 766195.05")
        self.assertEqual(downloadURL("/Geocode/txt?Street=Hromadova&Locality=Kladno&HouseNumber=2741&ZIPCode=27201&LocalityPart=Kladno"), "1033052.61, 766195.05")
        pass

    def old_testCompileAddress(self):
        self.assertEqual(
            downloadCompiledAddress(u"Arnošta Valenty", u"670", u"", u"31", u"19800", u"Praha", u"Černý Most", u"9"),
            u"Arnošta Valenty 670/31\nČerný Most\n198 00 Praha 9"
        )
        self.assertEqual(
            downloadCompiledAddress(u"Arnošta Valenty", u"670", u"", u"", u"198 00", u"Praha", u"Černý Most", u"9"),
            u'Arnošta Valenty 670\nČerný Most\n198 00 Praha 9'
        )
        self.assertEqual(
            downloadCompiledAddress(u"Medová", u"", u"30", u"", u"10400", u"Praha", u"Křeslice"),
            u"10", u'Medová č. ev. 30\nKřeslice\n104 00 Praha 10'
        )
        self.assertEqual(
            downloadCompiledAddress(u"", u"", u"42", u"", u"10400", u"Praha", u"Křeslice", u"10"),
            u'Křeslice č. ev. 42\n104 00 Praha 10'
        )
        self.assertEqual(
            downloadCompiledAddress(u"Lhenická", u"1120", u"", u"1", u"37005", u"České Budějovice", u"České Budějovice 2", u""),
            u'Lhenická 1120/1\nČeské Budějovice 2\n370 05 České Budějovice'
        )
        self.assertEqual(
            downloadCompiledAddress(u'Lhenická', u'1120', u'', u'', u'370 05', u'České Budějovice', u'České Budějovice 2', u''),
            u'Lhenická 1120\nČeské Budějovice 2\n37005 České Budějovice'
        )
        self.assertEqual(
            downloadCompiledAddress(u'Lhenická', u'', u'12', u'', u'37005', u'České Budějovice', u'České Budějovice 2', u''),
            u'Lhenická č. ev. 12\nČeské Budějovice 2\n37005 České Budějovice'
        )
        self.assertEqual(
            downloadCompiledAddress(u'Žamberecká', u'339', u'', u'-', u'51601', u'Vamberk', u'Vamberk', u''),
            u'Žamberecká 339\n51601 Vamberk\n'
        )
        self.assertEqual(
            downloadCompiledAddress(u'Žamberecká', u'339', u'', u'1', u'51601', u'Vamberk', u'Vamberk', u''),
            u'Žamberecká 339/1\n51601 Vamberk'
        )
        self.assertEqual(
            downloadCompiledAddress(u'Žamberecká', u'', u'21', u'', u'51601', u'Vamberk', u'Vamberk', u''),
            u'Žamberecká č. ev. 21\n51601 Vamberk'
        )
        self.assertEqual(
            downloadCompiledAddress(u'', u'106', u'', u'', u'53333', u'Pardubice', u'Dražkovice', u''),
            u'Dražkovice 106\n53333 Pardubice'
        )
        self.assertEqual(
            downloadCompiledAddress(u'', u'106', u'', u'12', u'53333', u'Pardubice', u'Dražkovice', u''),
            u'Dražkovice 106/12\n53333 Pardubice'
        )
        self.assertEqual(
            downloadCompiledAddress(u'', u'', u'32', u'', u'53333', u'Pardubice', u'Dražkovice', u''),
            u'Dražkovice č. ev. 32\n53333 Pardubice'
        )
        self.assertEqual(
            downloadCompiledAddress(u'', u'111', u'', u'', u'50333', u'Praskačka', u'Praskačka', u''),
            u'č. p. 111\n50333 Praskačka'
        )
        self.assertEqual(
            downloadCompiledAddress(u'', u'111', u'', u'1', u'53333', u'Praskačka', u'Praskačka', u''),
            u'č .p. 111/1\n53333 Praskačka'
        )
        self.assertEqual(
            downloadCompiledAddress(u'', u'', u'32', u'', u'53333', u'Praskačka', u'Praskačka', u''),
            u'č .ev. 32\n53333 Pardubice'
        )
        pass

    def testFullTextSearch(self):
        self.assertEqual(downloadURL("/FullTextSearch/txt/?SearchText=Severn%C3%AD%20Kladno"), "Severní 507, 272 04 Kladno", "Severní 508, 272 04 Kladno", "Severní 509, 272 04 Kladno")
        self.assertEqual(downloadURL("/FullTextSearch/txt/?SearchText=Severni%20Kladno"), "Severní 507, 272 04 Kladno", "Severní 508, 272 04 Kladno", "Severní 509, 272 04 Kladno")
        self.assertEqual(downloadURL("/FullTextSearch/txt/?SearchText=Sev.%20Kladno"), "Severní 507, 272 04 Kladno", "Severní 508, 272 04 Kladno", "Severní 509, 272 04 Kladno")
        self.assertEqual(downloadURL("/FullTextSearch/txt/?SearchText=Severni%20Klad"), "Severní 507, 272 04 Kladno", "Severní 508, 272 04 Kladno", "Severní 509, 272 04 Kladno")
        self.assertEqual(downloadURL("/FullTextSearch/txt/?SearchText=Ml%C3%A1de%C5%BEnick%C3%A1%20Kladno"), "Mládežnická 841, 272 04 Kladno", "Mládežnická 842, 272 04 Kladno")
        self.assertEqual(downloadURL("/FullTextSearch/txt/?SearchText=Mladeznicka%20Kladno"), "Mládežnická 841, 272 04 Kladno", "Mládežnická 842, 272 04 Kladno")
        self.assertEqual(downloadURL("/FullTextSearch/txt/?SearchText=Kladruby"), "č.ev. 11, Kladruby, 258 01", "č.p. 95, Kladruby, 258 01")
        self.assertEqual(downloadURL("/FullTextSearch/txt/?SearchText=V.%20Dub%C3%AD%20Kladno"), "V. Sembdnera 611, Dubí, 272 03 Kladno", "V. Špály 571, Dubí, 272 03 Kladno")
        self.assertEqual(downloadURL("/FullTextSearch/txt/?SearchText=V%C3%A1c%20Kladno"), "Václava Řacha 1352, Švermov, 273 09 Kladno", "Václavova 1678, 272 01 Kladno", "Václava Millera 163, Rozdělov, 272 04 Kladno")
        self.assertEqual(downloadURL("/FullTextSearch/txt/?SearchText=V%20Kladno%20Kladno"), "Václavova 1678, 272 01 Kladno", "V. Burgra 131, 272 04 Kladno", "V. Burgra 132, 272 04 Kladno")
        pass

    def old_testValidate(self):
        self.assertEqual(downloadURL("/Validate/txt/Severní/Kladno/507"), "ANO")
        self.assertEqual(downloadURL("/Validate/txt/Severní/Kladno/507?ZIPCode=27204&LocalityPart=Kladno"), "ANO")
        self.assertEqual(downloadURL("/Validate/txt/Severní/Kladno/507?ZIPCode=27206&LocalityPart=Kladno"), "NE")
        self.assertEqual(downloadURL("/Validate/txt/Severní/Kladno/120"), "NE")
        pass

    def old_testValidateAddressId(self):
        self.assertEqual(downloadURL("/ValidateAddressId/txt/1408739"), "ANO")
        self.assertEqual(downloadURL("/ValidateAddressId/txt/18480"), "NE")
        pass

    def old_testNearByAddresses(self):
        self.assertEqual(downloadURL("/NearbyAddresses/txt/1033000/766500/1000"), "Mládežnická 841, 272 04 Kladno", "Mládežnická 842, 272 04 Kladno")
        pass


if __name__ == '__main__':
    unittest.main()

