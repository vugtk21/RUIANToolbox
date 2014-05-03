__author__ = 'raugustyn'

import codecs
import os
from infofile import infoFile


def strTo127(s):
    result = ""
    for index in range(len(s)):
        ch = s[index:index + 1]
        if ord(ch) >= 32 and ord(ch) <= 127:
            result += ch
    return result


def pathWithLastSlash(path):
    if path != "" and path[len(path) - 1:] != os.sep:
        path = path + os.sep

    return path


class Config:
    ADMIN_NAME = 'admin'
    ADMIN_PASSWORD = 'bar67gux7hd6f5ge6'
    dataDir = ""
    uncompressDownloadedFiles = True
    downloadFullDatabase = True
    DATADIR_ID = "datadir"
    DOWNLOADFULLDATABASE_ID = "downloadfulldatabase"
    UNCOMPRESSDOWNLOADEDFILES_ID = "uncompressdownloadedfiles"
    TRUE_ID = "true"

    def __init__(self, configFileName):
        self._configFileName = configFileName
        inFile = codecs.open(configFileName, "r", "utf-8")
        lines = inFile.readlines()
        inFile.close()

        for line in lines:
            # Using "#" character as comment identifier -> remove everything after this
            if line.find("#") >= 0:
                    line = line[:line.find("#") - 1]
            line = strTo127(line.strip())
            lineParts = line.split("=")
            name = lineParts[0].lower()
            if len(lineParts) > 1:
                value = lineParts[1]
            else:
                value = ""

            if name == self.DATADIR_ID:
                self.dataDir = pathWithLastSlash(value)
            elif name == self.DOWNLOADFULLDATABASE_ID:
                self.downloadFullDatabase = value == self.TRUE_ID
            elif name == self.UNCOMPRESSDOWNLOADEDFILES_ID:
                self.uncompressDownloadedFiles = value == self.TRUE_ID

        infoFile.load(self.dataDir + "Info.txt")

    def save(self, configFileName = ""):
        if configFileName != "":
            self._configFileName = configFileName

        def boolToStr(v):
            if v:
                return self.TRUE_ID
            else:
                return "false"

        outFile = codecs.open(self._configFileName, "w", "utf-8")
        outFile(self.DATADIR_ID + "=" + self.dataDir)
        outFile(self.DOWNLOADFULLDATABASE_ID + "=" + boolToStr(self.downloadFullDatabase))
        outFile(self.UNCOMPRESSDOWNLOADEDFILES_ID + "=" + boolToStr(self.uncompressDownloadedFiles))
        outFile.close()

config = Config("RUIANDownload.cfg")
