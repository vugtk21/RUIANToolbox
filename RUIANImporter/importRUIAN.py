# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        importRUIAN
# Purpose:     Imports VFR data downloaded directory
#
# Author:      Radek Augustýn
# Copyright:   (c) VUGTK, v.v.i. 2014
# License:     CC BY-SA 4.0
#-------------------------------------------------------------------------------
helpStr = """
Import VFR data to database.

Requires: Python 2.7.5 or later
          OS4Geo with WFS Support (http://geo1.fsv.cvut.cz/landa/vfr/OSGeo4W_vfr.zip)

Usage: importRUIAN.py [-dbname <database name>] [-host <host name>] [-port <database port>] [-user <user name>]
                      [-password <database password>] [-layers layer1,layer2,...] [-os4GeoPath <path>]
                      [-buildServicesTables <{True} {False}>] [-buildAutocompleteTables <{True} {False}>] [-help]')

       -dbname
       -host
       -port
       -user
       -password
       -layers
       -os4GeoPath
       -buildServicesTables
       -buildAutocompleteTables
       -Help         Print help
"""

DEMO_MODE = False # If set to true, there will be just 50 rows in every state database import lines applied.

import os
import sys
from os.path import join
from subprocess import call

import shared; shared.setupPaths()

from SharedTools.config import pathWithLastSlash
from SharedTools.config import RUIANImporterConfig
from SharedTools.log import logger
import buildhtmllog

config = RUIANImporterConfig()

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

def getOSGeoPath():
    return joinPaths(os.path.dirname(__file__), config.os4GeoPath)

def convertFileToDownloadLists(HTTPListName):
    result = []

    inFile = open(HTTPListName, "r")
    try:
        fileName = "%s_list.txt" % (HTTPListName[:HTTPListName.find(".txt")])
        outFile = open(fileName, "w")
        result.append(fileName)
        linesInFile = 0
        for line in inFile:
            linesInFile = linesInFile + 1
            if DEMO_MODE and linesInFile > 3: continue

            line = line[line.rfind("/") + 1:line.find(".xml.gz")]
            outFile.write(line + "\n")

        outFile.close()
    finally:
        inFile.close()
    return result


def buildDownloadBatch(fileListFileName, fileNames):
    path = os.path.dirname(fileListFileName)
    os4GeoPath = joinPaths(os.path.dirname(__file__), config.os4GeoPath)
    result = path + os.sep + "Import.bat"
    file = open(result, "w")
    file.write("cd %s\n" % path)
    overwriteCommand = "--o"
    for fileName in fileNames:
        (VFRlogFileName, VFRerrFileName) = buildhtmllog.getLogFileNames(fileListFileName)

        importCmd = "call %s vfr2pg --file %s --dbname %s --user %s --passwd %s %s" % (os4GeoPath, fileName, config.dbname, config.user, config.password, overwriteCommand)

        if config.layers != "": importCmd += " --layer " + config.layers

        importCmd += " >%s 2>%s\n" % (VFRlogFileName, VFRerrFileName)

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
    downloadBatchFileName = buildDownloadBatch(fileListFileName, GDALFileListNames)

    call(downloadBatchFileName)
    deleteFilesInLists(path, GDALFileListNames, ".xml.gz")
    os.remove(downloadBatchFileName)
    renameFile(fileListFileName, "__")
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

    def removeDataFiles():
        dataPath = pathWithLastSlash(os.path.split(updateFileList)[0])
        inFile = open(updateFileList, "r")
        try:
            for line in inFile:
                fileName = os.path.basename(line)
                if os.path.exists(dataPath + fileName):
                    os.remove(dataPath + fileName)
        finally:
            inFile.close()
        pass

    logger.info("Importing update data from " + updateFileList)

    (startDate, endDate, type) = extractDatesAndType(updateFileList)
    logger.info("\tPočáteční datum:" + startDate)
    logger.info("\tKonečné datum:" + endDate)
    logger.info("\tTyp dat:" + type)

    os4GeoPath = joinPaths(os.path.dirname(__file__), config.os4GeoPath)

    (VFRlogFileName, VFRerrFileName) = buildhtmllog.getLogFileNames(updateFileList)

    params = ' '.join([os4GeoPath, "vfr2pg",
                "--dbname", config.dbname,
                "--user ", config.user,
                "--passwd ", config.password,
                "--date", startDate + ":" + endDate,
                "--type", type])
    if config.layers != "": params += " --layer " + config.layers
    params += " >%s 2>%s" % (VFRlogFileName, VFRerrFileName)

    batchFileName = os.path.dirname(os.path.abspath(updateFileList)) + os.sep + "Import.bat"
    file = open(batchFileName, "w")
    file.write("cd " + os.path.dirname(os.path.abspath(updateFileList)) + "\n")
    file.write(params)
    file.close()

    call(batchFileName)
    os.remove(batchFileName)
    removeDataFiles()

    renameFile(updateFileList, "__")
    logger.info("Import update data done.")
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

    result = False
    if stateFileList != "":
        createStateDatabase(path, stateFileList)
        result = True
    else:
        logger.info("Stavová data nejsou obsahem zdrojových dat.")

    if len(updatesFileList) == 0:
        logger.info("Denní aktualizace nejsou obsahem zdrojových dat.")
    else:
        result = True
        for updateFileName in updatesFileList:
            updateDatabase(updateFileName)

    logger.info(u"Generuji sestavu importů.")
    buildhtmllog.buildHTMLLog()

    logger.info("Načítání stažených souborů do databáze - hotovo.")
    return result

def getFullPath(configFileName, path):
    if not os.path.exists(path):
        path = pathWithLastSlash(configFileName) + path
    return path

def doImport(argv):
    logger.info("Importing VFR data to database.")
    config.loadFromCommandLine(argv, helpStr)

    osGeoPath = getOSGeoPath()
    if not os.path.exists(osGeoPath):
        print "Error: Batch file %s doesn't exist" % osGeoPath
        print "Download file http://geo1.fsv.cvut.cz/landa/vfr/OSGeo4W_vfr.zip, expand it and run script again."
        sys.exit()

    from RUIANDownloader.RUIANDownload import getDataDirFullPath
    rebuildAuxiliaryTables = processDownloadedDirectory(getDataDirFullPath())

    if config.buildServicesTables and rebuildAuxiliaryTables:
        from RUIANServices.services.auxiliarytables import buildAll, buildServicesTables
        if config.buildAutocompleteTables:
            buildAll()
        else:
            buildServicesTables()

    from RUIANServices.services.RUIANConnection import saveRUIANVersionDateToday
    saveRUIANVersionDateToday()

from SharedTools.sharetools import setupUTF
setupUTF()

if __name__ == "__main__":
    doImport(sys.argv)