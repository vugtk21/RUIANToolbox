# -*- coding: utf-8 -*-
__author__ = 'raugustyn'
#-------------------------------------------------------------------------------
# Name:        RUIANDownload
# Purpose:     Downloads VFR data from http://vdp.cuzk.cz/
#
# Author:      Radek Augustýn
# Copyright:   (c) VUGTK, v.v.i. 2014
# License:     CC BY-SA 4.0
#-------------------------------------------------------------------------------
helpStr = """
Downloads VFR data from http://vdp.cuzk.cz/

Requires: Python 2.7.5 or later

Usage: downloadruian.py [-DownloadFullDatabase {True | False}] [-DataDir data_dir] [-UncompressDownloadedFiles {True | False}][-help]')

       -DownloadFullDatabase        Set to True to download whole RUIAN state data
       -DataDir                     Path to OSGeo4W.bat supproting VFR format, either relative or absolute
       -UncompressDownloadedFiles   Set to True to uncompress *.xml.gz to *.xml files after download
       -RunImporter                 Set to True to run RUIANImporter.bat after download
       -DownloadURLs                Semicolon separated URL masks for downloading state or update file list from VDP
       -IgnoreHistoricalData        Set to True to download only actual month
       -Help                        Print help
"""

import urllib2, os, sys, datetime
import shared; shared.setupPaths()
import sharedtools.log as log
from htmllog import htmlLog
from sharedtools import pathWithLastSlash, RUIANDownloadConfig, RUIANDownloadInfoFile, safeMkDir, getFileExtension, extractFileName, getDataDirFullPath, RUNS_ON_LINUX

infoFile = None
config = None


def ___filePercentageInfo(fileSize, downloadedSize):
    status = r"%10d  [%3.2f%%]" % (downloadedSize, downloadedSize * 100. / fileSize)
    log.logger.info(status)

filePercentageInfo = ___filePercentageInfo


def __fileDownloadInfo(fileName, fileSize):
    pass

fileDownloadInfo = __fileDownloadInfo


class DownloadInfo:
    def __init__(self):
        self.fileName = ""
        self.fileSize = 0
        self.compressedFileSize = 0
        self.downloadTime = 0


def cleanDirectory(folder):
    """ Cleans directory content including subdirectories.

    :param folder: Path to the folder to be cleaned.
    """
    assert isinstance(folder, basestring)

    if os.path.exists(folder):
        for the_file in os.listdir(folder):
            path = os.path.join(folder, the_file)
            try:
                if os.path.isfile(path):
                    os.remove(path)
                else:
                    cleanDirectory(path)
                    os.rmdir(path)

            except Exception, e:
                log.logger.error(e.message, str(e))


def getFileContent(fileName):
    assert isinstance(fileName, basestring)

    log.logger.debug("getFileContent")
    with open(fileName, "r") as f:
        lines = f.read().splitlines()
        f.close()
    return lines


def formatTimeDelta(timeDelta):
    v = str(timeDelta)
    v = v.strip("0")
    if v[0:1] == ".": v = "0" + v
    if v == "": v = "0"
    return v + "s"


def getUpdateURL(url, dateStr):
    assert isinstance(url, basestring)
    assert isinstance(dateStr, basestring)

    url = url.replace("vf.cr=U&", "vf.cr=Z&")
    url = url.replace("vf.up=ST&", "")
    url = url.replace("vf.up=OB&", "")
    url = url.replace("vf.vu=Z&", "")
    url = url.replace("vf.uo=A&", "")
    url += "&vf.pd=" + dateStr
    return url


class RUIANDownloader:
    def __init__(self, targetDir = ""):
        assert isinstance(targetDir, basestring)

        self.dataDir = ""
        self._targetDir = ""
        self.assignTargetDir(targetDir)
        self.downloadInfos = []
        self.downloadInfo = None
        self._fullDownload = True
        self.pageURLs = config.downloadURLs
        self.ignoreHistoricalData = config.ignoreHistoricalData


    @property
    def targetDir(self):
        return self._targetDir


    @targetDir.setter
    def setTargetDir(self, targetDir):
        self.assignTargetDir(targetDir)


    def assignTargetDir(self, targetDir):
        """Assign value to the targetDir property. Creates this directory if not exists, including data sub directory.

        :param targetDir: Target directory path.
        """
        assert isinstance(targetDir, basestring)

        if targetDir != "":
            targetDir = os.path.normpath(targetDir)
            if targetDir.rfind(os.sep) != len(targetDir) - 1:
                targetDir += os.sep
            if not os.path.exists(targetDir):
                os.makedirs(targetDir)

        self.dataDir = targetDir
        if RUNS_ON_LINUX:
            self.dataDir += "data/"
            if not os.path.exists(self.dataDir):
                os.makedirs(self.dataDir)

        self._targetDir = targetDir


    def getFullSetList(self):
        log.logger.debug("RUIANDownloader.getFullSetList")
        self._fullDownload = True
        return self.getList(self.pageURLs, False)


    def getList(self, urls, isPatchList):
        assert isinstance(urls, basestring)
        assert isinstance(isPatchList, bool)

        urls = urls.split(";")
        result = []
        for url in urls:
            url = url.replace("vyhledej", "seznamlinku")
            log.logger.info("Downloading file list from " + url)
            content = urllib2.urlopen(url).read()
            lines = content.splitlines()
            result.extend(lines)

        if self.ignoreHistoricalData and not isPatchList:
            newResult = []
            stateMonth = datetime.date.today().month - 1
            stateYear = datetime.date.today().year
            if stateMonth == 0:
                stateYear = stateYear - 1
                stateMonth = 12

            for url in result:
                date = url[url.rfind("/") + 1:]
                date = date[:date.find("_")]
                month = int(date[4:6])
                year = int(date[:4])
                if year == stateYear and month >= stateMonth:
                    newResult.append(url)
            result = newResult

        return result


    def getUpdateList(self, fromDate = ""):
        assert isinstance(fromDate, basestring)

        log.logger.debug("RUIANDownloader.getUpdateList since %s", infoFile.validFor())
        self._fullDownload = False
        if fromDate == "" or infoFile.validFor() != "":
            v = infoFile.validFor()
            dateStr = v[8:10] + "." + v[5:7] + "." + v[0:4]
            firstPageURL = self.pageURLs.split(";")[0]
            return self.getList(getUpdateURL(firstPageURL, dateStr), True)
        else:
            return []


    def buildIndexHTML(self):
        def addCol(value, tags = ""):
            htmlLog.addCol(value, tags)

        def addDownloadHeader():
            if self._fullDownload:
                headerText = "Stažení stavových dat"
            else:
                headerText = "Stažení aktualizací k "
            v = str(datetime.datetime.now())
            htmlLog.addHeader(headerText + " " + v[8:10] + "." + v[5:7] + "." + v[0:4])

        def addTableHeader():
            htmlLog.openTable()
            htmlLog.htmlCode += "<tr><th align='left' valign='bottom'>Soubor</th><th>Staženo<br>[Bajtů]</th>"
            if config.uncompressDownloadedFiles:
                htmlLog.htmlCode += "<th></th><th>Rozbaleno<br>[Bajtů]</th>"
            htmlLog.htmlCode += "<th valign='bottom'>Čas</th></tr>"


        def calcSumValues():
            calcInfo = DownloadInfo()
            calcInfo.downloadTime = 0
            for info in self.downloadInfos:
                if info.downloadTime == "":
                    return
                elif info.fileName != "":
                    if info.fileSize:
                        calcInfo.fileSize += info.fileSize
                        calcInfo.compressedFileSize += info.compressedFileSize
                        time = float(info.downloadTime[:len(info.downloadTime) - 1])
                        calcInfo.downloadTime = calcInfo.downloadTime + time
                else:
                    info.fileSize = calcInfo.fileSize
                    info.compressedFileSize = calcInfo.compressedFileSize
                    info.downloadTime = calcInfo.downloadTime
                    return

            calcInfo.downloadTime = str(calcInfo.downloadTime) + "s"
            self.downloadInfos.append(calcInfo)


        def intToStr(intValue):
            if int == 0:
                return ""
            else:
                return str(intValue)


        def addTableContent():
            altColor = True
            for info in self.downloadInfos:
                if altColor:
                    tags = 'class="altColor"'
                else:
                    tags = ''
                altColor = not altColor
                htmlLog.openTableRow(tags)

                addCol(extractFileName(info.fileName))

                addCol(intToStr(info.compressedFileSize), 'align="right"')

                if config.uncompressDownloadedFiles and info.fileSize != 0:
                    addCol("->")
                else:
                    addCol("")

                if config.uncompressDownloadedFiles:
                    addCol(intToStr(info.fileSize), "align=right")

                addCol(info.downloadTime, "align=right")
                htmlLog.closeTableRow()
            htmlLog.closeTable()

        htmlLog.clear()
        addDownloadHeader()
        addTableHeader()
        calcSumValues()
        addTableContent()
        htmlLog.save(config.dataDir + "Index.html")


    def downloadURLList(self, urlList):

        def buildDownloadInfosList():
            self.downloadInfos = []
            for href in urlList:
                self.downloadInfo = DownloadInfo()
                self.downloadInfo.fileName = href.split('/')[-1]
                self.downloadInfos.append(self.downloadInfo)

        log.logger.debug("RUIANDownloader.downloadURLList")
        buildDownloadInfosList()
        for href, index in zip(urlList, range(len(urlList))):
            if not config.DEBUG_MAX_FILECOUNT or index < config.DEBUG_MAX_FILECOUNT:
                self.downloadInfo = self.downloadInfos[index]
                fileName = self.downloadURLtoFile(href, index, len(urlList))
                if config.uncompressDownloadedFiles:
                    self.uncompressFile(fileName, not config.runImporter)


    def downloadURLtoFile(self, url, fileIndex, filesCount):
        """ Downloads to temporary file. If suceeded, then rename result. """
        tmpFileName = pathWithLastSlash(self.dataDir) + "tmpfile.bin"
        log.logger.debug("RUIANDownloader.downloadURLtoFile")
        file_name = self.dataDir + url.split('/')[-1]
        startTime = datetime.datetime.now()

        if os.path.exists(file_name):
            log.logger.info("File " + extractFileName(file_name) + " is already downloaded, skipping it.")
            fileSize = os.stat(file_name).st_size
        else:
            req = urllib2.urlopen(url)
            meta = req.info()
            fileSize = int(meta.getheaders("Content-Length")[0])
            log.logger.info("Downloading file %s [%d/%d %d Bytes]" % (extractFileName(file_name), fileIndex, filesCount, fileSize))
            fileDownloadInfo(file_name, fileSize)
            CHUNK = 1024*1024
            file_size_dl = 0
            with open(tmpFileName, 'wb') as fp:
                while True:
                    chunk = req.read(CHUNK)
                    if not chunk:
                        break
                    fp.write(chunk)
                    file_size_dl += len(chunk)
                    log.logger.info(r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100.0 / fileSize))
                    self.downloadInfo.compressedFileSize = file_size_dl
                    #self.buildIndexHTML()
            fp.close()
            os.rename(tmpFileName, file_name)

        self.downloadInfo.downloadTime = formatTimeDelta(str(datetime.datetime.now() - startTime)[5:])
        self.downloadInfo.fileName = file_name
        self.downloadInfo.compressedFileSize = fileSize
        return file_name


    def uncompressFile(self, fileName, deleteSource = True):
        """
        Tato metoda rozbalí soubor s názvem fileName.

        @param fileName: Název souboru k dekompresi
        @param deleteSource: Jestliže True, komprimovaný soubor bude vymazán.
        @return: Vrací název expandovaného souboru.
        """
        log.logger.debug("RUIANDownloader.uncompressFile")
        ext = getFileExtension(fileName).lower()
        if ext == ".gz":
            outFileName = fileName[:-len(ext)]
            log.logger.info("Uncompressing " + extractFileName(fileName) + " -> " + extractFileName(outFileName))
            import gzip

            bufferSize = 1024*1024*20
            size = 0
            with gzip.open(fileName, 'rb') as inputFile:
                with open(outFileName, 'wb') as outputFile:
                    while True:
                        data = inputFile.read(bufferSize)
                        size = size + len(data)
                        if len(data) == 0 :
                            break
                        outputFile.write(data)
                        outputFile.flush()
                    outputFile.close()
                inputFile.close()


            self.downloadInfo.fileSize = os.path.getsize(outFileName)
            if deleteSource:
                os.remove(fileName)
            return outFileName
        else:
            return fileName


    def download(self):
        def wasItToday(dateTimeStr):
            if dateTimeStr == "":
                return False
            else:
                return str(datetime.datetime.now().date()) == dateTimeStr.split(" ")[0]

        if not infoFile.fullDownloadBroken:
            if wasItToday(infoFile.lastFullDownload):
                log.logger.warning("Process stopped! Nothing to download. Last full download was done Today " + infoFile.lastFullDownload)
                return
            elif not self._fullDownload and wasItToday(infoFile.lastPatchDownload):
                log.logger.warning("Process stopped! Nothing to download. Last patch was downloaded Today " + infoFile.lastPatchDownload)
                return

        startTime = datetime.datetime.now()

        callUpdate = False;
        if self._fullDownload or infoFile.lastFullDownload == "":
            log.logger.info("Running in full mode")
            if not infoFile.fullDownloadBroken:
                log.logger.info("Cleaning directory " + config.dataDir)
                cleanDirectory(config.dataDir)
                infoFile.fullDownloadBroken = True
                infoFile.save()

            safeMkDir(config.dataDir)

            l = self.getFullSetList()
            d = datetime.date.today()
            infoFile.lastFullDownload = '{:04d}'.format(d.year) + "-" + '{:02d}'.format(d.month) + "-01 14:07:13.084000"
            infoFile.lastPatchDownload = ""
            callUpdate = True

        else:
            log.logger.info("Running in update mode")
            l = self.getUpdateList()
            infoFile.lastPatchDownload = str(datetime.datetime.now())

        self.buildIndexHTML()

        if len(l) > 0:   # stahujeme jedině když není seznam prázdný
            self.downloadURLList(l)
            infoFile.save()
            self.saveFileList(l)
        else:
            log.logger.warning("Nothing to download, list is empty.")

        self.buildIndexHTML()
        htmlLog.closeSection(config.dataDir + "Index.html")

        infoFile.fullDownloadBroken = False
        infoFile.save()

        if callUpdate:
            self._fullDownload = False
            self.download()


    def saveFileList(self, fileList):
        infoFile.numPatches = infoFile.numPatches + 1
        v = str(datetime.datetime.now())
        fileName = v[0:4] + "." + v[5:7] + "." + v[8:10] + ".txt"
        if self._fullDownload:
            fileName = "Download_" + fileName
        else:
            fileName = "Patch_" + fileName
        outFile = open(config.dataDir + fileName, "w")
        for line in fileList:
            outFile.write(line + "\n")
        outFile.close()


    def _downloadURLtoFile(self, url):
        log.logger.debug("RUIANDownloader._downloadURLtoFile")
        log.logger.info("Downloading " + url)
        file_name = url.split('/')[-1]
        log.logger.info(file_name)
        u = urllib2.urlopen(url)
        f = open(self.targetDir + file_name, 'wb')
        meta = u.info()
        file_size = int(meta.getheaders("Content-Length")[0])
        log.logger.info("Downloading %s Bytes: %s" % (file_name, file_size))

        file_size_dl = 0
        block_sz = 8192
        while True:
            blockBuffer = u.read(block_sz)
            if not blockBuffer:
                break

            file_size_dl += len(blockBuffer)
            f.write(blockBuffer)
            filePercentageInfo(file_size, file_size_dl)
        f.close()


def printUsageInfo():
    log.logger.info(helpStr)
    sys.exit(1)


if __name__ == '__main__':
    config = RUIANDownloadConfig()
    config.loadFromCommandLine(sys.argv, helpStr)

    log.createLogger(config.dataDir + "Download.log")
    infoFile = RUIANDownloadInfoFile()

    if config.downloadFullDatabase:
        log.clearLogFile()

    log.logger.info("RUIAN Downloader")
    log.logger.info("#############################################")
    log.logger.info("Data directory : %s", config.dataDir)
    log.logger.info("Data directory full path : %s", getDataDirFullPath())
    log.logger.info("Download full database : %s", str(config.downloadFullDatabase))
    if not config.downloadFullDatabase:
        log.logger.info("Last full download  : %s", infoFile.lastFullDownload)
        log.logger.info("Last patch download : %s", infoFile.lastPatchDownload)
    log.logger.info("---------------------------------------------")

    downloader = RUIANDownloader(config.dataDir)
    downloader._fullDownload = config.downloadFullDatabase or infoFile.fullDownloadBroken
    downloader.download()

    log.logger.info("Download done.")
    if config.runImporter:
        log.logger.info("Executing importer.importruian.doImport().")
        from importer.importruian import doImport
        doImport(sys.argv)
        log.logger.info("Done - importer.importruian.doImport().")