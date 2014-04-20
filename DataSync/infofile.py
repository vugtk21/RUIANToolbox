# -*- coding: utf-8 -*-
__author__ = 'Augustyn'

import os

class InfoFile:
    def __init__(self):
        self.fileName = ""
        self.lastPatchDownload = ""
        self.lastFullDownload = ""

    def load(self, fileName):
        self.fileName = fileName
        if os.path.exists(fileName):
            infoFile = open(fileName, "r")
            self.lastPatchDownload = infoFile.readline().strip()
            self.lastFullDownload = infoFile.readline().strip()
            infoFile.close()
        else:
            self.lastFullDownload = ""
            self.lastPatchDownload = ""

    def save(self):
        infoFile = open(self.fileName, "w")
        infoFile.write(self.lastPatchDownload + "\n")
        infoFile.write(self.lastFullDownload + "\n")
        infoFile.close()

    def validFor(self):
        if self.lastPatchDownload != "":
            return self.lastPatchDownload
        else:
            return self.lastFullDownload

infoFile = InfoFile()