# -*- coding: utf-8 -*-

import unittest
import addressbuilder

class TestGlobalFunctions(unittest.TestCase):

    def setUp(self):
        self.htmlFormater = addressbuilder.HTMLTextFormater()
        pass

    def tearDown(self):
        pass

    def testgetAddressFromStr_Pattern1(self):
        a = addressbuilder.Address(
            street = u"ArnoÅ¡ta Valenty",
            descNumber = u"670",
            recordNumber = u"",
            orientationNumber = u"31",
            ZIPCode = u"198 00",
            town = u"Praha",
            district = u"Černý most",
            districtNumber = u"9"
        )
        self.assertEqual(
            a.toAddressString(self.htmlFormater),
            u"ArnoÅ¡ta Valenty 670/31<br>Černý Most<br>19800 Praha 9",
            u"Adresní místo v Praze s ulicí, číslem popisným a orientačním")
        pass

    def testgetAddressFromStr_Pattern2(self):
        a = addressbuilder.Address(
            street = u"ArnoÅ¡ta Valenty",
            descNumber = u"670",
            recordNumber = u"",
            orientationNumber = u"",
            ZIPCode = u"198 00",
            town = u"praha",
            district = u"Černý most",
            districtNumber = u"9"
        )
        self.assertEqual(
            a.toAddressString(self.htmlFormater),
            u"ArnoÅ¡ta Valenty 670<br>Černý Most<br>19800 Praha 9",
            u"Adresní místo v Praze s ulicí a číslem popisným")
        pass

    def testgetAddressFromStr_Pattern3(self):
        a = addressbuilder.Address(
            street = u"Medová",
            descNumber = u"",
            recordNumber = u"30",
            orientationNumber = u"",
            ZIPCode = u"104 00",
            town = u"Praha",
            district = u"Křeslice",
            districtNumber = u"10"
        )
        self.assertEqual(
            a.toAddressString(self.htmlFormater),
            u"Medová č. ev. 30<br>Křeslice<br>10400 Praha 10",
            u"Adresní místo v Praze s ulicí a číslem evidenčním")
        pass

    def testgetAddressFromStr_Pattern4(self):
        a = addressbuilder.Address(
            street = u"",
            descNumber = u"",
            recordNumber = u"42",
            orientationNumber = u"",
            ZIPCode = u"104 00",
            town = u"Praha",
            district = u"Křeslice",
            districtNumber = u"10"
        )
        self.assertEqual(
            a.toAddressString(self.htmlFormater),
            u"Křeslice č. ev. 42<br>10400 Praha 10",
            u"Adresní místo v Praze s číslem evidenčním")
        pass

if __name__ == '__main__':
    unittest.main()
