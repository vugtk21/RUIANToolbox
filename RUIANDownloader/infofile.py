# -*- coding: utf-8 -*-
__author__ = 'Augustyn'

import os

# Setup path to RUIANToolbox
import os.path, sys
basePath = os.path.join(os.path.dirname(__file__), "../..")
if not basePath in sys.path: sys.path.append(basePath)

from SharedTools.config import Config

def convertInfoFile(config):
    if config == None: return

    def isTrue(value):
        return value != None and value.lower() == "true"

    if config.numPatches == "":
        config.numPatches = 0
    else:
        config.numPatches = isTrue(config.numPatches)

class InfoFile(Config):
    def __init__(self, fileName, defSubDir = "", moduleFile = ""):
        Config.__init__(self, "info.txt",
            {
                "lastPatchDownload" : "",
                "lastFullDownload" : "",
                "numPatches" : 0
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