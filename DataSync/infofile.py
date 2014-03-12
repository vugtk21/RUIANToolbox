# -*- coding: utf-8 -*-
__author__ = 'Augustyn'

import os

class InfoFile:
    def __init__(self, fileName):
        self._fileName = fileName
        if os.path.exists(fileName):
            infoFile = open(fileName, "r")
            self.lastPatchDownload = infoFile.readline().strip()
            self.lastFullDownload = infoFile.readline().strip()
            infoFile.close()
        else:
            self.lastPatchDownload = ""
            self.lastFullDownload = ""

    def save(self):
        infoFile = open(self._fileName, "w")
        infoFile.write(self.lastPatchDownload + "\n")
        infoFile.write(self.lastFullDownload + "\n")
        infoFile.close()