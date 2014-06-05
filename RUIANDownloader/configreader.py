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
    DATADIR_ID = "datadir"
    DOWNLOADFULLDATABASE_ID = "downloadfulldatabase"
    UNCOMPRESSDOWNLOADEDFILES_ID = "uncompressdownloadedfiles"
    TRUE_ID = "true"
    RUNIMPORTER_ID = "runimporter"
    AUTOMATIC_DOWNLOAD_ID = "automaticdownloadtime"
    DOWNLOAD_URL_ID = "downloadurl"

    dataDir = ""
    uncompressDownloadedFiles = True
    downloadFullDatabase = True
    runImporter = False
    automaticDownloadTime = ""
    downloadURL = "http://vdp.cuzk.cz/vdp/ruian/vymennyformat/vyhledej?vf.pu=S&_vf.pu=on&_vf.pu=on&vf.cr=U&vf.up=ST&vf.ds=K&_vf.vu=on&vf.vu=G&_vf.vu=on&vf.vu=H&_vf.vu=on&_vf.vu=on&search=Vyhledat"

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
            valuePos = line.find("=")
            if valuePos < 0:
                continue
            else:
                value = ""
                name = line[:valuePos].lower()
                value = line[valuePos+1:]

            if name == self.DATADIR_ID:
                self.dataDir = pathWithLastSlash(value)
            elif name == self.DOWNLOADFULLDATABASE_ID:
                self.downloadFullDatabase = value == self.TRUE_ID
            elif name == self.UNCOMPRESSDOWNLOADEDFILES_ID:
                self.uncompressDownloadedFiles = value == self.TRUE_ID
            elif name == self.RUNIMPORTER_ID:
                self.runimporter = value == self.TRUE_ID
            elif name == self.AUTOMATIC_DOWNLOAD_ID:
                self.automaticDownloadTime = value
            elif name == self.DOWNLOAD_URL_ID:
                self.downloadURL = value

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
