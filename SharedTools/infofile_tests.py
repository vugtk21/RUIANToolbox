# -*- coding: utf-8 -*-
__author__ = 'Augustyn'

import unittest
import config, os

infofile = config.RUIANDownloadInfoFile()

class TestInfoFile(unittest.TestCase):
    FILENAME = "test.txt"
    LASTFULLDOWNLOAD_VALUE = "lastfulldownload"
    LASTPATCHDOWNLOAD_VALUE = "lastpatchdownload"

    def tearDown(self):
        os.remove(self.FILENAME)
        pass

    def testSave(self):
        """ Tests Save and consequently Init """
        f = infofile.InfoFile(self.FILENAME)
        f.lastFullDownload = self.LASTFULLDOWNLOAD_VALUE
        f.lastPatchDownload = self.LASTPATCHDOWNLOAD_VALUE
        f.save()

        f = infofile.InfoFile(self.FILENAME)
        self.assertEqual(f.lastFullDownload,  self.LASTFULLDOWNLOAD_VALUE,  "lastFullDownload not read correctly")
        self.assertEqual(f.lastPatchDownload, self.LASTPATCHDOWNLOAD_VALUE, "lastPatchDownload not read correctly")
        pass

if __name__ == '__main__':
    unittest.main()

