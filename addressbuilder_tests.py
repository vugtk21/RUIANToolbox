# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        addressbuilder_tests
# Purpose:     Testuje knihovnu addressbuilder
#
# Author:      Radek Augustýn
#
# Created:     14/02/2014
# Copyright:   (c) Radek Augustýn 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------
__author__ = 'raugustyn'

import unittest
import addressbuilder

class TestGlobalFunctions(unittest.TestCase):

    def setUp(self):
        self.htmlFormater = addressbuilder.TextFormater()
        pass

    def tearDown(self):
        pass

    def testgetAddressFromStr_Pattern1(self):
        a = addressbuilder.Address(
            street=u"Arnošta Valenty",
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
            u"Arnošta Valenty 670/31<br>Černý Most<br>19800 Praha 9",
            u"1.Adresní místo v Praze s ulicí, číslem popisným a orientačním")
        pass

    def testgetAddressFromStr_Pattern2(self):
        a = addressbuilder.Address(
            street=u"Arnošta Valenty",
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
            u"Arnošta Valenty 670<br>Černý Most<br>19800 Praha 9",
            u"2.Adresní místo v Praze s ulicí a číslem popisným")
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
            u"3.Adresní místo v Praze s ulicí a číslem evidenčním")
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
            u"4.Adresní místo v Praze s číslem evidenčním")
        pass

    def testgetAddressFromStr_Pattern5(self):
        a = addressbuilder.Address(
            street = u"Lhenická",
            descNumber = u"1120",
            recordNumber = u"",
            orientationNumber = u"1",
            ZIPCode = u"370 05",
            town = u"České Budějovice",
            district = u"České Budějovice 2",
            districtNumber = u""
        )
        self.assertEqual(
            a.toAddressString(self.htmlFormater),
            u"Lhenická 1120/1<br>České Budějovice 2<br>37005 České Budějovice<br>",
            u"5. Adresní místo mimo Prahu s ulicí, číslem popisným a orientačním, název obce a její části nejsou shodné")
        pass

if __name__ == '__main__':
    unittest.main()
