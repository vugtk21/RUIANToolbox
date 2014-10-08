# -*- coding: utf-8 -*-
__author__ = 'Augustyn'

import codecs
import sys
import os
from os import listdir
from os.path import isfile, join
from subprocess import call

from shared import setupPaths;setupPaths()

from SharedTools.config import pathWithLastSlash
from SharedTools.config import Config
from SharedTools.log import logger, clearLogFile

config = Config("importRUIAN.cfg",
            {
                "dbname" : "euradin",
                "host" : "localhost",
                "port" : "5432",
                "user" : "postgres",
                "password" : "postgres",
                "schemaName" : "",
                "layers" : "",
                "os4GeoPath": ".\\OSGeo4W_vfr\\OSGeo4W.bat"
            },
            defSubDir = "RUIANImporter",
            moduleFile = __file__
           )


def convertFileToDownloadList(HTTPListName):
    inFile = open(HTTPListName, "r")
    filesListName = HTTPListName[:HTTPListName.find(".txt")] + "_list.txt"
    outFile = open(filesListName, "w")
    for line in inFile:
        line = line[line.rfind("/") + 1:line.find(".xml.gz")]
        outFile.write(line + "\n")
    inFile.close()
    outFile.close()
    return filesListName

def buildDownloadBatch(fileList):
    params = ' '.join([config.os4GeoPath, "vfr2pg",
                "--file", fileList,
                "--dbname", config.dbname,
                "--user", config.user,
                "--passwd", config.password,
                "--o"])
    logger.debug(params)

    result = os.path.dirname(os.path.abspath(fileList)) + os.sep + "download.bat"
    file = open(result, "w")
    file.write("cd " + os.path.dirname(os.path.abspath(fileList)) + "\n")
    file.write(params)
    file.close()

    return result

def deleteFilesInList(path, fileList, extension):
    path = pathWithLastSlash(path)
    listFile = open(path + fileList, "r")
    i = 0
    for line in listFile:
        i += 1
        fileName = path + line.rstrip() + extension
        if os.path.exists(fileName):
            os.remove(fileName)
        logger.debug(str(i), ":", fileName)

    pass

def createStateDatabase(path, fileList):
    logger.info("Načítám stavovou databázi ze seznamu " + fileList)
    GDALFileList = convertFileToDownloadList(fileList)
    downloadBatchFileName = buildDownloadBatch(GDALFileList)

    call(downloadBatchFileName)
    deleteFilesInList(path, GDALFileList, ".xml.gz")
    os.remove(GDALFileList)
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
    files = [ f for f in listdir(path) if isfile(join(path, f)) ]
    stateFileList = ""
    updatesFileList = []
    for fileName in files:
        if fileName[len(fileName) - 4:] == ".txt":
            if fileName.lower().find("download_") == 0:
                stateFileList = join(path, fileName)
            elif fileName.lower().find("patch_") == 0:
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

    logger.info("Hotovo.")

def getFullPath(configFileName, path):
    if not os.path.exists(path):
        path = pathWithLastSlash(configFileName) + path
    return path

def doImport():
    from RUIANDownloader.RUIANDownload import getDataDirFullPath
    processDownloadedDirectory(getDataDirFullPath())

from SharedTools.sharetools import setupUTF
setupUTF()

if __name__ == "__main__":
    doImport()
