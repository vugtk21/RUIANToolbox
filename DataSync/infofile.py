# -*- coding: utf-8 -*-
__author__ = 'Augustyn'

import os

class InfoFile:
    def __init__(self):
        self.fileName = ""
        self.lastPatchDownload = ""
        self.lastFullDownload = ""
        self.numPatches = 0

    def load(self, fileName):
        self.fileName = fileName
        if os.path.exists(fileName):
            file = open(fileName, "r")
            self.lastPatchDownload = file.readline().strip()
            self.lastFullDownload = file.readline().strip()
            self.numPatches = int(file.readline().strip())
            file.close()
        else:
            self.lastFullDownload = ""
            self.lastPatchDownload = ""

    def save(self):
        file = open(self.fileName, "w")
        file.write(self.lastPatchDownload + "\n")
        file.write(self.lastFullDownload + "\n")
        file.write(str(self.numPatches) + "\n")
        file.close()

    def validFor(self):
        if self.lastPatchDownload != "":
            return self.lastPatchDownload
        else:
            return self.lastFullDownload

infoFile = InfoFile()