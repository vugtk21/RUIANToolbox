# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        HTTPShared_Tests
# Purpose:     Module HTTPShared tests implementation.
#
# Author:      Radek Augustýn
# Copyright:   (c) VUGTK, v.v.i. 2014
# License:     CC BY-SA 4.0
#-------------------------------------------------------------------------------

import HTTPShared
import unittest

class TestGlobalFunctions(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass


    def testnoneToString(self):
        self.assertEqual(HTTPShared.noneToString(None), "", "None must be converted to string.")
        self.assertEqual(HTTPShared.noneToString("34"), "34", "String must be converted to string.")
        self.assertEqual(HTTPShared.noneToString(34), "34", "Int must be converted to string.")
        self.assertEqual(HTTPShared.noneToString([34, "44"]), ["34", "44"], "List must be converted to list of strings.")
        self.assertEqual(HTTPShared.noneToString(("34", None, 15, "ff")), ("34", "", "15", "ff"), "Tuple must be converted to tuple strings.")
        pass

def main():
    unittest.main()

if __name__ == '__main__':
    main()
