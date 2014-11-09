# -*- coding: utf-8 -*-
__author__ = 'raugustyn'

import os
import codecs
import sys
from log import logger
import sharetools

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

def getSubDirPath(subDir):
    path = os.path.dirname(__file__)
    masterPath = os.path.split(path)[0]
    return pathWithLastSlash(os.path.join(masterPath, subDir))

def getParentPath(moduleFile):
    if moduleFile == "": moduleFile = __file__
    path = os.path.dirname(moduleFile)
    parentPath = os.path.split(path)[0]
    return pathWithLastSlash(parentPath)

def getMasterPath(moduleFile):
    path = getParentPath(moduleFile)
    masterPath = os.path.split(path)[0]
    return pathWithLastSlash(masterPath)

class Config:
    TRUE_ID = "true"

    def __init__(self, fileName, attrs = {}, afterLoadProc = None, basePath = "", defSubDir = "", moduleFile = "", createIfNotFound = True):
        if basePath != "":
            basePath = pathWithLastSlash(basePath)
            if not os.path.exists(basePath):
                logger.warning("Config.__init__, cesta " + basePath + " neexistuje.")
                basePath = ""

        self.fileName = basePath + fileName
        self.afterLoadProc = afterLoadProc
        self.attrs = attrs # Tabulka vsech atributu, jak nactenych, tak povolenych
        self._remapTable = {} # Tabulka mapovani downloadfulldatabase -> downloadFullDatabase
        self.moduleFile = moduleFile
        self.createIfNotFound = createIfNotFound

        if attrs != None:
            for key in attrs:
                setattr(self, key, attrs[key])
                if key != key.lower():
                    self._remapTable[key.lower()] = key

        searchFileNames = [self.fileName, getParentPath(moduleFile) + fileName, getMasterPath(moduleFile) + fileName]
        if defSubDir != "":
            searchFileNames.append(getSubDirPath(defSubDir) + fileName)
        searchFileNames.append("c:/temp/" + fileName)

        self.fileName = ""
        i = 0
        for fName in searchFileNames:
            if os.path.exists(fName):
                self.fileName = fName
                if i == 3:
                    logger.warning(u"Konfigurační soubor " + fileName + u" nebyl nenalezen.")
                    logger.warning(u"Soubor byl nalezen a použit z c:/temp.")
                break
            i = i + 1

        if self.fileName == "":
            self.fileName = basePath + fileName
            if createIfNotFound:
                msg = u"Konfigurační soubor %s nebyl nenalezen." % (pathWithLastSlash(basePath) + self.fileName)
                logger.error(msg)
                self.save()
                logger.error(u"Soubor byl vytvořen ze šablony. Nastavte prosím jeho hodnoty a spusťte program znovu.")
                import sys
                sys.exit()
        else:
            self.loadFile()

    def loadFile(self):
        if os.path.exists(self.fileName):
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

        pathParts = self.fileName.split(os.sep)
        sharetools.safeMkDir(os.sep.join(pathParts[:len(pathParts)-1]))

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
    config = Config("C:\\Users\\raugustyn\\Desktop\\RUIANToolbox\\RUIANDownloader\\__RUIANDownload.cfg",
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