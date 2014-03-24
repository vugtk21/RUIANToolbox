# -*- coding: utf-8 -*-

import unittest
import addressbuilder
import addressbuilder_testdict

class TestGlobalFunctions(unittest.TestCase):

    def setUp(self):
        self.htmlFormater = addressbuilder.TextFormater()
        pass

    def tearDown(self):
        pass

    def testGetRestFromStr(self):
        dictionary = addressbuilder_testdict.dictionary
        for key in dictionary:
            params = dictionary[key]
            self.assertEqual(unicode(params.address.toRestString(),"utf-8"), params.returnValue, params.errMsg)


if __name__ == '__main__':
    unittest.main()