# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        config
# Purpose:     Config files persistency classes implementations.
#
# Author:      Radek Augustýn
# Copyright:   (c) VUGTK, v.v.i. 2014
# License:     CC BY-SA 4.0
#-------------------------------------------------------------------------------

import os, codecs, sys
import log
import base

x_RUIANDownloadConfig = None
x_RUIANImporterConfig = None
x_RUIANDownloadInfoFile = None
x_RUIANToolboxPath = None
x_RUIANDownloadInfoFile = None

TRUE_ID = "true"


def boolToStr(v):
    if v:
        return TRUE_ID
    else:
        return "false"


def strTo127(s):
    result = ""
    for index in range(len(s)):
        ch = s[index:index + 1]
        if ord(ch) >= 32 and ord(ch) <= 127:
            result += ch
    return result


def isTrue(value):
    return value != None and value.lower() == TRUE_ID



def getSubDirPath(subDir):
    path = os.path.dirname(__file__)
    masterPath = os.path.split(path)[0]
    return base.pathWithLastSlash(os.path.join(masterPath, subDir))


def getParentPath(moduleFile):
    if moduleFile == "": moduleFile = __file__
    path = os.path.dirname(moduleFile)
    parentPath = os.path.split(path)[0]
    return base.pathWithLastSlash(parentPath)


def getMasterPath(moduleFile):
    path = getParentPath(moduleFile)
    masterPath = os.path.split(path)[0]
    return base.pathWithLastSlash(masterPath)


class Config:
    def __init__(self, fileName, attrs = {}, afterLoadProc = None, basePath = "", defSubDir = "", moduleFile = "", createIfNotFound = True):
        if basePath != "":
            basePath = base.pathWithLastSlash(basePath)
            if not os.path.exists(basePath):
                log.logger.error("Config.__init__, cesta " + basePath + " neexistuje.")
                basePath = ""

        self.fileName = basePath + fileName
        self.afterLoadProc = afterLoadProc
        self.attrs = attrs # Tabulka vsech atributu, jak nactenych, tak povolenych
        self._remapTable = {} # Tabulka mapovani downloadfulldatabase -> downloadFullDatabase
        self.moduleFile = moduleFile
        self.createIfNotFound = createIfNotFound
        self.isDefault = True

        if attrs != None:
            for key in attrs:
                setattr(self, key, attrs[key])
                if key != key.lower():
                    self._remapTable[key.lower()] = key

        if os.path.exists(basePath + fileName):
            self.fileName = basePath + fileName
        else:
            path = base.normalizePathSep(os.path.dirname(__file__))
            pathItems = path.split(os.sep)
            for i in range(0, len(pathItems)):
                path = os.sep.join(pathItems[0:i]) + os.sep + fileName
                if os.path.exists(path):
                    self.fileName = path
                    break

        if self.fileName == "":
            self.fileName = basePath + fileName
            if createIfNotFound:
                msg = u"Konfigurační soubor %s nebyl nenalezen." % (base.pathWithLastSlash(basePath) + self.fileName)
                log.logger.error(msg)
                self.save()
                log.logger.error(u"Soubor byl vytvořen ze šablony. Nastavte prosím jeho hodnoty a spusťte program znovu.")
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
                self.setAttr(name, value)
                pass

            file.close()
            if self.afterLoadProc != None:
                self.afterLoadProc(self)
            self.isDefault = False


    def setAttr(self, name, value):
        name = self._getAttrName(name)
        setattr(self, name, value)
        self.attrs[name] = value

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


        pathParts = self.fileName.split(os.sep)
        base.safeMkDir(os.sep.join(pathParts[:len(pathParts) - 1]))

        outFile = codecs.open(self.fileName, "w", "utf-8")
        for key in self.attrs:
            name = self._getAttrName(key)
            value = getattr(self, name)
            outFile.write(name + "=" + str(value) + "\n")
        outFile.close()

    def loadFromCommandLine(self, argv, usageMessage):
        if (argv is not None) or (len(argv) > 1):
            i = 1
            while i < len(argv):
                arg = argv[i].lower()
                if arg.startswith("-"):
                    command = arg[1:]
                    foundCommand = False
                    i = i + 1
                    if i < len(argv):
                        for attrKey in self.attrs:
                            if attrKey == command:
                                self.attrs[attrKey] = argv[i]
                                foundCommand = True

                    if not foundCommand:
                        log.logger.warning('Unrecognised command option: %s' % arg)
                        log.logger.info(usageMessage)
                        sys.exit()
                i = i + 1
        pass


def convertInfoFile(config):
    if config == None: return

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
            convertInfoFile, "", "RUIANDownloader", moduleFile, False
        )

    def validFor(self):
        if self.lastPatchDownload != "":
            return self.lastPatchDownload
        else:
            return self.lastFullDownload

    def load(self, fileName):
        self.fileName = fileName
        self.loadFile()

def RUIANDownloadInfoFile():
    global x_RUIANDownloadInfoFile

    if x_RUIANDownloadInfoFile == None:
        x_RUIANDownloadInfoFile = InfoFile("")
    return x_RUIANDownloadInfoFile

def convertRUIANDownloadCfg(config):
    if config == None: return

    config.downloadFullDatabase = isTrue(config.downloadFullDatabase)
    config.uncompressDownloadedFiles = isTrue(config.uncompressDownloadedFiles)
    config.runImporter = isTrue(config.runImporter)
    config.dataDir = config.dataDir.replace("/", os.sep)
    config.dataDir = config.dataDir.replace("\\", os.sep)
    config.dataDir = base.pathWithLastSlash(config.dataDir)
    if not os.path.isabs(config.dataDir):
        result = os.path.dirname(config.moduleFile) + os.path.sep + config.dataDir
        result = os.path.normpath(result)
        config.dataDir = base.pathWithLastSlash(result)

    config.ignoreHistoricalData = isTrue(config.ignoreHistoricalData)
    RUIANDownloadInfoFile().load(config.dataDir + "Info.txt")
    pass

def RUIANDownloadConfig():
    global x_RUIANDownloadConfig

    if x_RUIANDownloadConfig == None:
        x_RUIANDownloadConfig = Config("DownloadRUIAN.cfg",
            {
                "downloadFullDatabase" : False,
                "uncompressDownloadedFiles" : False,
                "runImporter" : False,
                "dataDir" : "..\\DownloadedData\\",
                "downloadURLs" : "http://vdp.cuzk.cz/vdp/ruian/vymennyformat/vyhledej?vf.pu=S&_vf.pu=on&_vf.pu=on&vf.cr=" + \
                                 "U&vf.up=ST&vf.ds=K&vf.vu=Z&_vf.vu=on&_vf.vu=on&vf.vu=H&_vf.vu=on&_vf.vu=on&search=Vyhledat;" + \
                                 "http://vdp.cuzk.cz/vdp/ruian/vymennyformat/vyhledej?vf.pu=S&_vf.pu=on&_vf.pu=on&vf.cr=U&" +\
                                 "vf.up=OB&vf.ds=K&vf.vu=Z&_vf.vu=on&_vf.vu=on&_vf.vu=on&_vf.vu=on&vf.uo=A&search=Vyhledat",
                "ignoreHistoricalData": True

            },
           convertRUIANDownloadCfg,
           defSubDir = "downloader",
           moduleFile = __file__,
           basePath = getRUIANDownloaderPath()
        )
    return x_RUIANDownloadConfig


def convertRUIANImporterConfig(config):
    if config == None: return

    config.buildServicesTables = isTrue(config.buildServicesTables)
    config.buildAutocompleteTables = isTrue(config.buildAutocompleteTables)


def RUIANImporterConfig():
    global x_RUIANImporterConfig

    if x_RUIANImporterConfig == None:
        x_RUIANImporterConfig = Config("ImportRUIAN.cfg",
            {
                "dbname" : "euradin",
                "host" : "localhost",
                "port" : "5432",
                "user" : "postgres",
                "password" : "postgres",
                "schemaName" : "",
                "layers" : "AdresniMista,Ulice,StavebniObjekty,CastiObci,Obce,Mop,Momc",
                "WINDOWS_os4GeoPath" : "..\\..\\OSGeo4W_vfr\\OSGeo4W.bat",
                "LINUX_vfr2pgPath": "../gdal-vfr-master/",
                "buildServicesTables" : "True",
                "buildAutocompleteTables" : "False"
            },
            convertRUIANImporterConfig,
            defSubDir = "importer",
            moduleFile = __file__,
            basePath = getRUIANImporterPath()
           )
    return x_RUIANImporterConfig


def getRUIANToolboxPath():
    global x_RUIANToolboxPath

    if x_RUIANToolboxPath == None:
        x_RUIANToolboxPath = base.pathWithLastSlash(os.path.split(os.path.dirname(__file__))[0])
        x_RUIANToolboxPath = x_RUIANToolboxPath.replace("/", os.sep)
        x_RUIANToolboxPath = x_RUIANToolboxPath.replace("\\", os.sep)
    return x_RUIANToolboxPath


def getRUIANImporterPath():
    return getRUIANToolboxPath() + "importer" + os.sep


def getRUIANDownloaderPath():
    return getRUIANToolboxPath() + "downloader" + os.sep


def getRUIANServicesBasePath():
    return getRUIANToolboxPath() + "RUIANServices" + os.sep


def getRUIANServicesPath():
    return getRUIANToolboxPath() + "RUIANServices" + os.sep + "services" + os.sep


def getRUIANServicesHTMLPath():
    return getRUIANToolboxPath() + "RUIANServices" + os.sep + "HTML" + os.sep


def getRUIANServicesSQLScriptsPath():
    return getRUIANToolboxPath() + "RUIANServices" + os.sep + "SqlScripts" + os.sep


def getDataDirFullPath():
    result = RUIANDownloadConfig().dataDir
    if not os.path.isabs(result):
        result = getRUIANDownloaderPath() + result
        result = os.path.normpath(result)
        result = base.pathWithLastSlash(result)
    return result


def main():
    print "This module is a library, it can't be run as an application."

    if True:
        print "Download Config:", RUIANDownloadConfig().fileName
        print "Importer Config:", RUIANImporterConfig().fileName
        print "getRUIANToolboxPath:", getRUIANToolboxPath()
        print "getRUIANImporterPath:", getRUIANImporterPath()
        print "getRUIANServicesBasePath:", getRUIANServicesBasePath()
        print "getRUIANServicesPath:", getRUIANServicesPath()
        print "getRUIANServicesHTMLPath:", getRUIANServicesHTMLPath()
        print "getRUIANServicesSQLScriptsPath:", getRUIANServicesSQLScriptsPath()


if __name__ == '__main__':
    main()