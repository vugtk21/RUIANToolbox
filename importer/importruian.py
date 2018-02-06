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

Usage: importruian.py [-dbname <database name>] [-host <host name>] [-port <database port>] [-user <user name>]
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

DEMO_MODE = False # If set to true, there will be just few rows in every state database import lines applied.

import os
import sys
from os.path import join
from subprocess import call

import shared; shared.setupPaths()

from sharedtools import pathWithLastSlash, RUIANImporterConfig, getDataDirFullPath, extractFileName, RUNS_ON_WINDOWS, RUNS_ON_LINUX, COMMAND_FILE_EXTENSION
import sharedtools.log as log
import buildhtmllog

RUIAN2PG_LIBRARY_ZIP_URL = [
    "http://www.vugtk.cz/euradin/VFRLibrary/OSGeo4W_vfr_1.9.73.zip",
    "https://github.com/ctu-geoforall-lab/gdal-vfr/archive/master.zip"
][RUNS_ON_LINUX]
LIST_FILE_TAIL = "_list.txt"


config = None


def createCommandFile(fileNameBase, commands):
    """Creates either fileNameBase.bat file or fileNameBase.sh file, depending on the operating system.
    If runs on Linux, then chmod 777 fileName is applied.

    :param fileNameBase: Base of the command script file name.
    :param commands: Context of the command file.
    :return:
    """
    assert isinstance(fileNameBase, basestring)
    assert isinstance(commands, basestring)

    fileName = fileNameBase + COMMAND_FILE_EXTENSION
    file = open(fileName, "w")

    if RUNS_ON_LINUX:file.write("#!/usr/bin/env bash\n")
    file.write(commands)
    if RUNS_ON_LINUX:os.chmod(fileName, 0o777)

    file.close()

    return fileName


def joinPaths(basePath, relativePath):
    assert isinstance(basePath, basestring)
    assert isinstance(relativePath, basestring)

    basePath = basePath.replace("/", os.sep)
    relativePath = relativePath.replace("/", os.sep)
    if (os.path.exists(relativePath)):
        return relativePath
    else:
        basePathItems = basePath.split(os.sep)
        relativePathItems = relativePath.split(os.sep)
        endBaseIndex = len(basePathItems)
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
    if RUNS_ON_WINDOWS:
        path = config.WINDOWS_os4GeoPath
    else:
        path = config.LINUX_vfr2pgPath

    return joinPaths(os.path.dirname(__file__), path)


def convertFileToDownloadLists(HTTPListName):
    assert isinstance(HTTPListName, basestring)

    result = []

    inFile = open(HTTPListName, "r")
    try:
        fileName = (HTTPListName[:HTTPListName.find(".txt")]) + LIST_FILE_TAIL
        outFile = open(fileName, "w")
        result.append(fileName)
        linesInFile = 0
        for line in inFile:
            linesInFile = linesInFile + 1
            if DEMO_MODE and linesInFile > 3: continue

            line = line[line.rfind("/") + 1:line.find("\n")]
            outFile.write(line + "\n")

        outFile.close()
    finally:
        inFile.close()
    return result


def buildDownloadBatch(fileListFileName, fileNames):
    assert isinstance(fileListFileName, basestring)
    assert os.path.exists(fileListFileName)
    assert isinstance(fileNames, list)

    path = os.path.dirname(fileListFileName)
    os4GeoPath = getOSGeoPath()

    (VFRlogFileName, VFRerrFileName) = buildhtmllog.getLogFileNames(fileListFileName)
    commands = "cd %s\n" % path
    overwriteCommand = "--o"
    for fileName in fileNames:

        vfrCommand = "vfr2pg --file %s --host %s --dbname %s --user %s --passwd %s --schema %s %s" % (extractFileName(fileName), config.host, config.dbname, config.user, config.password, config.schemaName, overwriteCommand)

        if RUNS_ON_WINDOWS:
            importCmd = "call %s %s" % (os4GeoPath, vfrCommand)
        else:
            importCmd = "%s%s  2>>%s 3>>%s" % (os4GeoPath, vfrCommand, VFRlogFileName, VFRerrFileName)

        if config.layers != "": importCmd += " --layer " + config.layers

        log.logger.debug(importCmd)
        commands += importCmd + "\n"
        overwriteCommand = "--append"

        commandFileName = createCommandFile(path + os.sep + "Import", commands)

    return (commandFileName, VFRlogFileName, VFRerrFileName)


def deleteFilesInLists(path, fileLists, extension):
    assert isinstance(path, basestring)
    assert os.path.exists(path)
    assert isinstance(fileLists, list)
    assert isinstance(extension, basestring)

    path = pathWithLastSlash(path)
    for fileList in fileLists:
        listFile = open(fileList, "r")
        i = 0
        for line in listFile:
            i += 1
            fileName = path + line.rstrip() + extension
            if os.path.exists(fileName):
                os.remove(fileName)
            log.logger.debug(str(i), ":", fileName)
        listFile.close()
        os.remove(fileList)


def createStateDatabase(path, fileListFileName):
    assert isinstance(path, basestring)
    assert isinstance(fileListFileName, basestring)

    log.logger.info("Načítám stavovou databázi ze seznamu " + fileListFileName)
    GDALFileListNames = convertFileToDownloadLists(fileListFileName)
    downloadBatchFileName, VFRlogFileName, VFRerrFileName = buildDownloadBatch(fileListFileName, GDALFileListNames)

    log.logger.info("Spouštím %s, průběh viz. %s a %s." % (downloadBatchFileName, VFRlogFileName, VFRerrFileName))
    call(downloadBatchFileName)
    deleteFilesInLists(path, GDALFileListNames, ".xml.gz")
    os.remove(downloadBatchFileName)
    renameFile(fileListFileName, "__")


def extractDatesAndType(patchFileList):
    isinstance(patchFileList, basestring)

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
    assert isinstance(fileName, basestring)
    assert isinstance(prefix, basestring)

    parts = fileName.split(os.sep)
    resultParts = parts[:len(parts) - 1]
    resultParts.append(prefix + parts[len(parts) - 1])

    newFileName = os.sep.join(resultParts)
    if os.path.exists(newFileName): os.remove(newFileName)

    os.rename(fileName, newFileName)
    return newFileName


def updateDatabase(updateFileList):
    assert isinstance(updateFileList, basestring)

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

    log.logger.info("Importing update data from " + updateFileList)

    (startDate, endDate, type) = extractDatesAndType(updateFileList)
    log.logger.info("\tPočáteční datum:" + startDate)
    log.logger.info("\tKonečné datum:" + endDate)
    log.logger.info("\tTyp dat:" + type)

    os4GeoPath = getOSGeoPath()

    if sys.platform.lower().startswith('win'):
        os4GeoPath = os4GeoPath + " "

    os4GeoPath = os4GeoPath + "vfr2pg"

    (VFRlogFileName, VFRerrFileName) = buildhtmllog.getLogFileNames(updateFileList)

    params = ' '.join([os4GeoPath,
                "--host", config.host,
                "--dbname", config.dbname,
                "--user ", config.user,
                "--passwd ", config.password,
                "--schema ", config.schemaName,
                "--date", startDate + ":" + endDate,
                "--type", type])

    if config.layers != "":
        params += " --layer " + config.layers

    if RUNS_ON_WINDOWS:
        params += " >%s 2>%s" % (VFRlogFileName, VFRerrFileName)
    else:
        params += " 2>%s 3>%s" % (VFRlogFileName, VFRerrFileName)

    commands = "cd " + os.path.dirname(os.path.abspath(updateFileList)) + "\n"
    commands += params + "\n"
    batchFileName = createCommandFile(os.path.dirname(os.path.abspath(updateFileList)) + os.sep + "Import" , commands)

    call(batchFileName)
    os.remove(batchFileName)
    removeDataFiles()

    renameFile(updateFileList, "__")
    log.logger.info("Import update data done.")


def processDownloadedDirectory(path):
    assert isinstance(path, basestring)

    log.logger.info("Načítám stažené soubory do databáze...")
    log.logger.info("--------------------------------------")
    log.logger.info("Zdrojová data : " + path)

    path = pathWithLastSlash(path)
    stateFileList = ""
    updatesFileList = []
    for file in os.listdir(path):
        if file.endswith(".txt"):
            if file.startswith("Download_") and not file.endswith(LIST_FILE_TAIL):
                stateFileList = join(path, file)
            elif file.startswith("Patch_"):
                updatesFileList.append(join(path, file))

    result = False
    if stateFileList != "":
        createStateDatabase(path, stateFileList)
        result = True
    else:
        log.logger.info("Stavová data nejsou obsahem zdrojových dat.")

    if len(updatesFileList) == 0:
        log.logger.info("Denní aktualizace nejsou obsahem zdrojových dat.")
    else:
        result = True
        for updateFileName in updatesFileList:
            updateDatabase(updateFileName)

    log.logger.info(u"Generuji sestavu importů.")
    buildhtmllog.buildHTMLLog()

    log.logger.info("Načítání stažených souborů do databáze - hotovo.")
    return result


def getFullPath(configFileName, path):
    assert isinstance(configFileName, basestring)
    assert isinstance(path, basestring)

    if not os.path.exists(path):
        path = pathWithLastSlash(configFileName) + path
    return path


def doImport(argv):
    global config
    
    from sharedtools import setupUTF
    setupUTF()

    config = RUIANImporterConfig()
    config.loadFromCommandLine(argv, helpStr)
    log.createLogger(getDataDirFullPath() + "Download.log")
    log.logger.info("Importing VFR data to database.")

    osGeoPath = getOSGeoPath()
    if not os.path.exists(osGeoPath):
        print "Error: RUIAN import library %s doesn't exist" % osGeoPath
        print "Download file %s, expand it into RUIANToolbox base directory and run script again." % RUIAN2PG_LIBRARY_ZIP_URL

        sys.exit()

    rebuildAuxiliaryTables = processDownloadedDirectory(getDataDirFullPath())

    if config.buildServicesTables and rebuildAuxiliaryTables:
        from RUIANServices.services.auxiliarytables import buildAll, buildServicesTables
        if config.buildAutocompleteTables:
            buildAll()
        else:
            buildServicesTables()

    from RUIANServices.services.RUIANConnection import saveRUIANVersionDateToday
    saveRUIANVersionDateToday()


if __name__ == "__main__":
    doImport(sys.argv)