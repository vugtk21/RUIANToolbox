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
import addressbuilder_testdict

class TestGlobalFunctions(unittest.TestCase):

    def setUp(self):
        self.htmlFormater = addressbuilder.TextFormater()
        pass

    def tearDown(self):
        pass

    def testgetAddressFromStr(self):
        dictionary = addressbuilder_testdict.dictionary
        for key in dictionary:
            params = dictionary[key]
            self.assertEqual(params.address.toAddressString(self.htmlFormater), params.returnValue, params.errMsg)


if __name__ == '__main__':
    unittest.main()
