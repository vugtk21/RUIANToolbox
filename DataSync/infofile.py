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
            inFile = open(fileName, "r")
            self.lastPatchDownload = inFile.readline().strip()
            self.lastFullDownload = inFile.readline().strip()
            self.numPatches = int(inFile.readline().strip())
            inFile.close()
        else:
            self.lastFullDownload = ""
            self.lastPatchDownload = ""

    def save(self):
        outFile = open(self.fileName, "w")
        outFile.write(self.lastPatchDownload + "\n")
        outFile.write(self.lastFullDownload + "\n")
        outFile.write(str(self.numPatches) + "\n")
        outFile.close()

    def validFor(self):
        if self.lastPatchDownload != "":
            return self.lastPatchDownload
        else:
            return self.lastFullDownload

infoFile = InfoFile()