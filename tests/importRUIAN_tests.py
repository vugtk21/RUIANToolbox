# -*- coding: utf-8 -*-

import unittest
from RUIANImporter.ImportRUIAN import *

class TestGlobalFunctions(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testJoinPaths(self):
        self.assertEqual(joinPaths(os.path.dirname(__file__), "c:\\temp\\"), "c:\\temp\\", "Parametr zadaný absolutní cestou")
        self.assertEqual(joinPaths(os.path.dirname(__file__), "Downloads\\"), os.path.dirname(__file__) + "\\Downloads\\", "Parametr zadaný relativní cestou")

        fileItems = os.path.dirname(__file__).split(os.sep)

        expectedResult = "\\".join(fileItems[:len(fileItems)-1]) + "\\temp\\"
        self.assertEqual(joinPaths(os.path.dirname(__file__), "..\\temp\\"), expectedResult, "Parametr zadaný relativní cestou o adresář výše")

        expectedResult = "\\".join(fileItems[:len(fileItems)-2]) + "\\temp\\"
        self.assertEqual(joinPaths(os.path.dirname(__file__), "..\\..\\temp\\"), expectedResult, "Parametr zadaný relativní cestou o dva adresáře výše")
        pass



if __name__ == '__main__':
    unittest.main()

