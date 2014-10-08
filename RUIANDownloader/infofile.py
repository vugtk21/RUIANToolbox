# -*- coding: utf-8 -*-
__author__ = 'Augustyn'

import os

from shared import setupPaths;setupPaths()

from SharedTools.config import Config

def convertInfoFile(config):
    if config == None: return

    def isTrue(value):
        return value != None and value != "" and value.lower() == "true"

    if config.numPatches == "":
        config.numPatches = 0
    else:
        config.numPatches = isTrue(config.numPatches)

    config.fullDownloadBroken = isTrue(config.fullDownloadBroken)

class InfoFile(Config):
    def __init__(self, fileName, defSubDir = "", moduleFile = ""):
        Config.__init__(self, "info.txt",
            {
                "lastPatchDownload" : "",
                "lastFullDownload" : "",
                "numPatches" : 0,
                "fullDownloadBroken": "false"
            },
            convertInfoFile, "", "RUIANDownloader", moduleFile
        )

    def validFor(self):
        if self.lastPatchDownload != "":
            return self.lastPatchDownload
        else:
            return self.lastFullDownload

    def load(self, fileName):
        self.fileName = fileName
        self.loadFile()

infoFile = InfoFile("")