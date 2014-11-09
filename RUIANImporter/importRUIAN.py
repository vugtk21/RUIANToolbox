# -*- coding: utf-8 -*-

__author__ = 'Augustyn'

DEMO_MODE = False # If set to true, there will be just 50 rows in every state database import lines applied.

import os
from os.path import join
from subprocess import call

import shared; shared.setupPaths()

from SharedTools.config import pathWithLastSlash
from SharedTools.config import Config
from SharedTools.log import logger

def convertRUIANImporterCfg(config):
    if config == None: return

    def isTrue(value):
        return value != None and value.lower() == "true"

    config.buildServicesTables = isTrue(config.buildServicesTables)
    pass

config = Config("importRUIAN.cfg",
            {
                "dbname" : "euradin",
                "host" : "localhost",
                "port" : "5432",
                "user" : "postgres",
                "password" : "postgres",
                "schemaName" : "",
                "layers" : "",
                "os4GeoPath": "..\\..\\OSGeo4W_vfr\\OSGeo4W.bat",
                "buildServicesTables" : "False"
            },
            convertRUIANImporterCfg,
            defSubDir = "RUIANImporter",
            moduleFile = __file__
           )

def joinPaths(basePath, relativePath):
    basePath = basePath.replace("/", os.sep)
    relativePath = relativePath.replace("/", os.sep)
    basePathItems = basePath.split(os.sep)
    relativePathItems = relativePath.split(os.sep)
    endBaseIndex = len(basePathItems) + 1
    startRelative = 0
    for subPath in relativePathItems:
        if subPath == "..":
            endBaseIndex = endBaseIndex - 1
            startRelative = startRelative + 1
        elif subPath == ".":
            startRelative = startRelative + 1
        else:
            break

    fullPath = os.sep.join(basePathItems[:endBaseIndex]) + os.sep + os.sep.join(relativePathItems[startRelative:])
    return fullPath

def convertFileToDownloadLists(HTTPListName):
    result = []

    def getNextFile():
        fileName = "%s_list_%d.tmp" % (HTTPListName[:HTTPListName.find(".txt")], len(result))
        outFile = open(fileName, "w")
        result.append(fileName)
        return outFile

    inFile = open(HTTPListName, "r")
    try:
        outFile = getNextFile()
        linesInFile = 0
        for line in inFile:
            if linesInFile >= 500:
                linesInFile = 0
                outFile.close()
                outFile = getNextFile()

            linesInFile = linesInFile + 1
            if DEMO_MODE and linesInFile > 3: continue

            line = line[line.rfind("/") + 1:line.find(".xml.gz")]
            outFile.write(line + "\n")

        outFile.close()
    finally:
        inFile.close()
    return result

def buildDownloadBatch(path, fileNames):
    os4GeoPath = joinPaths(os.path.dirname(__file__), config.os4GeoPath)
    result = path + os.sep + "download.bat"
    file = open(result, "w")
    file.write("cd %s\n" % path)
    overwriteCommand = "--o"
    for fileName in fileNames:
        importCmd = "call %s vfr2pg --file %s --dbname %s --user %s --passwd %s %s\n" % (os4GeoPath, fileName, config.dbname, config.user, config.password, overwriteCommand)
        logger.debug(importCmd)
        file.write(importCmd)
        overwriteCommand = "--append"
    file.close()

    return result

def deleteFilesInLists(path, fileLists, extension):
    path = pathWithLastSlash(path)
    for fileList in fileLists:
        listFile = open(fileList, "r")
        i = 0
        for line in listFile:
            i += 1
            fileName = path + line.rstrip() + extension
            if os.path.exists(fileName):
                os.remove(fileName)
            logger.debug(str(i), ":", fileName)
        listFile.close()
        os.remove(fileList)

    pass

def createStateDatabase(path, fileListFileName):
    logger.info("Načítám stavovou databázi ze seznamu " + fileListFileName)
    GDALFileListNames = convertFileToDownloadLists(fileListFileName)
    downloadBatchFileName = buildDownloadBatch(os.path.dirname(fileListFileName), GDALFileListNames)

    call(downloadBatchFileName)
    deleteFilesInLists(path, GDALFileListNames, ".xml.gz")
    os.remove(downloadBatchFileName)
    pass

def extractDatesAndType(patchFileList):

    def getDate(line):
        result = line[line.rfind("/") + 1:]
        result = result[:result.find("_")]
        return result

    def getType(line):
        type = line[line.rfind("/") + 1:]
        type = type[type.find("_") + 1:type.find(".")]
        return type

    startDate = ""
    endDate = ""
    type = ""

    inFile = open(patchFileList, "r")
    firstLine = True
    for line in inFile:
        if firstLine:
            endDate = getDate(line)
            type = getType(line)
            firstLine = False
        else:
            startDate = getDate(line)
    inFile.close()

    return (startDate, endDate, type)

def renameFile(fileName, prefix):
    parts = fileName.split(os.sep)
    resultParts = parts[:len(parts) - 1]
    resultParts.append(prefix + parts[len(parts) - 1])

    newFileName = os.sep.join(resultParts)
    if os.path.exists(newFileName): os.remove(newFileName)

    os.rename(fileName, newFileName)
    return newFileName

def updateDatabase(updateFileList):
    logger.info("Načítám denní aktualizace ze souboru " + updateFileList)

    (startDate, endDate, type) = extractDatesAndType(updateFileList)
    logger.info("\tPočáteční datum:" + startDate)
    logger.info("\tKonečné datum:" + endDate)
    logger.info("\tTyp dat:" + type)

    params = ' '.join([config.os4GeoPath, "vfr2pg",
                "--dbname", config.dbname,
                "--user ", config.user,
                "--passwd ", config.password,
                "--date", startDate + ":" + endDate,
                "--type", type])

    batchFileName = os.path.dirname(os.path.abspath(updateFileList)) + os.sep + "download.bat"
    file = open(batchFileName, "w")
    file.write("cd " + os.path.dirname(os.path.abspath(updateFileList)) + "\n")
    file.write(params)
    file.close()

    call(batchFileName)
    os.remove(batchFileName)

    renameFile(updateFileList, "__")
    pass

def processDownloadedDirectory(path):
    logger.info("Načítám stažené soubory do databáze...")
    logger.info("--------------------------------------")
    logger.info("Zdrojová data : " + path)

    path = pathWithLastSlash(path)
    stateFileList = ""
    updatesFileList = []
    for file in os.listdir(path):
        fileName = file.lower()
        if file.endswith(".txt"):
            if fileName.startswith("download_"):
                stateFileList = join(path, fileName)
            elif fileName.startswith("patch_"):
                updatesFileList.append(join(path, fileName))

    if stateFileList != "":
        createStateDatabase(path, stateFileList)
    else:
        logger.info("Stavová data nejsou obsahem zdrojových dat.")

    if len(updatesFileList) == 0:
        logger.info("Denní aktualizace nejsou obsahem zdrojových dat.")
    else:
        for updateFileName in updatesFileList:
            updateDatabase(updateFileName)

    logger.info("Načítání stažené soubory do databáze - hotovo.")

def getFullPath(configFileName, path):
    if not os.path.exists(path):
        path = pathWithLastSlash(configFileName) + path
    return path

def doImport():
    from RUIANDownloader.RUIANDownload import getDataDirFullPath
    processDownloadedDirectory(getDataDirFullPath())

    if config.buildServicesTables:
        from RUIANServices.services import auxiliarytables
        auxiliarytables.createAll()

from SharedTools.sharetools import setupUTF
setupUTF()

if __name__ == "__main__":
    doImport()