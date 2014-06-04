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

def downloadURL(url):
    return ""

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

    def testCompileAddress(self):  #upraveny testy podle posledních připomínek z ČÚZK, promítnuto i v nové verzi metodiky
        self.assertEqual(
            buildCompileAddress(u"Arnošta Valenty", u"670", u"", u"31", u"", u"19800", u"Praha", u"Černý Most", u"9"),
            u"Arnošta Valenty 670/31\nČerný Most\n19800 Praha 9"
        )
        self.assertEqual(
            buildCompileAddress(u"Arnošta Valenty", u"670", u"", u"", u"", u"198 00", u"Praha", u"Černý Most", u"9"),
            u"Arnošta Valenty 670\nČerný Most\n19800 Praha 9"
        )
        self.assertEqual(
            buildCompileAddress(u"Medová", u"", u"30", u"", u"", u"10400", u"Praha", u"Křeslice", u"10"),
            u"Medová č.ev. 30\nKřeslice\n10400 Praha 10"
        )
        self.assertEqual(
            buildCompileAddress(u"", u"", u"42", u"", u"", u"10400", u"Praha", u"Křeslice", u"10"),
            u"Křeslice č.ev. 42\n10400 Praha 10"
        )
        self.assertEqual(
            buildCompileAddress(u"Lhenická", u"1120", u"", u"1", u"", u"37005", u"České Budějovice", u"České Budějovice 2", u""),
            u"Lhenická 1120/1\nČeské Budějovice 2\n37005 České Budějovice"
        )
        self.assertEqual(
            buildCompileAddress(u"Holická", u"568", u"", u"31", u"y", u"779 00", u"Olomouc", u"Hodolany", u""),
            u"Holická 568/31y\nHodolany\n77900 Olomouc"
        )
        self.assertEqual(
            buildCompileAddress(u"Lhenická", u"1120", u"", u"", u"", u"370 05", u"České Budějovice", u"České Budějovice 2", u""),
            u"Lhenická 1120\nČeské Budějovice 2\n37005 České Budějovice"
        )
        self.assertEqual(
            buildCompileAddress(u"Lhenická", u"", u"12", u"", u"", u"37005", u"České Budějovice", u"České Budějovice 2", u""),
            u"Lhenická č.ev. 12\nČeské Budějovice 2\n37005 České Budějovice"
        )
        self.assertEqual(
            buildCompileAddress(u"Žamberecká", u"339", u"", u"", u"", u"51601", u"Vamberk", u"Vamberk", u""),
            u"Žamberecká 339\n51601 Vamberk\n"
        )
        self.assertEqual(
            buildCompileAddress(u"Žamberecká", u"339", u"", u"1", u"", u"51601", u"Vamberk", u"Vamberk", u""),
            u"Žamberecká 339/1\n51601 Vamberk"
        )
        self.assertEqual(
            buildCompileAddress(u"Lidická", u"2858", u"", u"49", u"F", u"78701", u"Šumperk", u"Šumperk", u""),
            u"Lidická 2858/49F\n78701 Šumperk"
        )
        self.assertEqual(
            buildCompileAddress(u"Žamberecká", u"", u"21", u"", u"", u"51601", u"Vamberk", u"Vamberk", u""),
            u"Žamberecká č.ev. 21\n51601 Vamberk"
        )
        self.assertEqual(
            buildCompileAddress(u"", u"106", u"", u"", u"", u"53333", u"Pardubice", u"Dražkovice", u""),
            u"Dražkovice 106\n53333 Pardubice"
        )
        self.assertEqual(
            buildCompileAddress(u"", u"", u"32", u"", u"", u"53333", u"Pardubice", u"Dražkovice", u""),
            u"Dražkovice č.ev. 32\n53333 Pardubice"
        )
        self.assertEqual(
            buildCompileAddress(u"", u"111", u"", u"", u"", u"50333", u"Praskačka", u"Praskačka", u""),
            u"č.p. 111\n50333 Praskačka"
        )
        self.assertEqual(
            buildCompileAddress(u"", u"", u"86", u"", u"", u"53943", u"Krouna", u"Krouna", u""),
            u"č.ev. 86\n53943 Krouna"
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

    def testValidate(self):

        self.assertEqual(downloadURL("/Validate/txt/Severní/Kladno/507"), "ANO")

        self.assertEqual(downloadURL("/Validate/txt/Severní/Kladno/507?ZIPCode=27204&LocalityPart=Kladno"), "ANO")

        self.assertEqual(downloadURL("/Validate/txt/Severní/Kladno/507?ZIPCode=27206&LocalityPart=Kladno"), "NE")

        self.assertEqual(downloadURL("/Validate/txt/Severní/Kladno/120"), "NE")
        pass

    def testValidateAddressId(self):

        self.assertEqual(downloadURL("/ValidateAddressId/txt/1408739"), "ANO")

        self.assertEqual(downloadURL("/ValidateAddressId/txt/18480"), "NE")

        pass

    def testNearByAddresses(self):

        self.assertEqual(downloadURL("/NearbyAddresses/txt/1033000/766500/1000"), "Mládežnická 841, 272 04 Kladno", "Mládežnická 842, 272 04 Kladno")

        pass


if __name__ == '__main__':
    unittest.main()

