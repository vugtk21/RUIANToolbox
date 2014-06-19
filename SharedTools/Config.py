__author__ = 'raugustyn'

import os
import codecs
import sys
from log import logger

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
    TRUE_ID = "true"

    def __init__(self, fileName, attrs = {}, afterLoadProc = None):
        self.fileName = fileName
        self.afterLoadProc = afterLoadProc
        self.attrs = attrs # Tabulka vsech atributu, jak nactenych, tak povolenych
        self._remapTable = {} # Tabulka mapovani downloadfulldatabase -> downloadFullDatabase

        if attrs != None:
            for key in attrs:
                setattr(self, key, attrs[key])
                if key != key.lower():
                    self._remapTable[key.lower()] = key

        if not os.path.exists(self.fileName):
            tempCfgFileName = "c:/temp/" + self.fileName
            if os.path.exists(tempCfgFileName):
                logger.warning("Configuration file " + self.fileName + " not found.")
                logger.warning("File was found at c:/temp, using it.")
                self.fileName = tempCfgFileName
                self.loadFile()
            else:
                self.save()
                logger.error("Configuration file " + self.fileName + " not found.")
                logger.error("File has been created from template. Please edit configuration file and run program again.")
                import sys
                sys.exit()
        else:
            self.loadFile()


    def loadFile(self):
        file = codecs.open(self.fileName, "r", "utf-8")
        for line in file:
            if line.find("#") >= 0:
                line = line[:line.find("#") - 1]
            line = strTo127(line.strip())
            delPos = line.find("=")
            name = self._getAttrName(line[:delPos])
            value = line[delPos + 1:]
            setattr(self, name, value)
            self.attrs[name] = value
            pass
        file.close()
        if self.afterLoadProc != None:
            self.afterLoadProc(self)


    def _getAttrName(self, name):
        name = name.lower()
        if name in self._remapTable:
            return self._remapTable[name]
        else:
            return name


    def getValue(self, name, defValue = ""):
        name = self._getAttrName(name)
        if self.attrs.has_key(name):
            return self.attrs[name]
        else:
            return defValue


    def save(self, configFileName = ""):
        if configFileName != "":
            self.fileName = configFileName

        def boolToStr(v):
            if v:
                return self.TRUE_ID
            else:
                return "false"

        outFile = codecs.open(self.fileName, "w", "utf-8")
        for key in self.attrs:
            name = self._getAttrName(key)
            value = getattr(self, name)
            outFile.write(name + "=" + str(value) + "\n")
        outFile.close()

def convertImportRUIANCfg(config):
    if config == None: return

    def isTrue(value):
        return value != None and value.lower() == "true"

    config.downloadFullDatabase = isTrue(config.downloadFullDatabase)
    config.uncompressDownloadedFiles = isTrue(config.uncompressDownloadedFiles)
    config.runImporter = isTrue(config.runImporter)
    config.dataDir = pathWithLastSlash(config.dataDir)
    pass


def main():
    config = Config("C:\\Users\\raugustyn\\Desktop\\RUIANToolbox\\RUIANDownloader\\RUIANDownload.cfg",
            {
                "downloadFullDatabase" : False,
                "uncompressDownloadedFiles" : True,
                "runImporter" : False,
                "dataDir" : "Downloads\\",
                "automaticDownloadTime" : "",
                "downloadURL" : ""
            },
           convertImportRUIANCfg)

    config.save("C:\\Users\\raugustyn\\Desktop\\RUIANToolbox\\RUIANDownloader\\RUIANDownloadSaved.cfg")

if __name__ == '__main__':
    main()