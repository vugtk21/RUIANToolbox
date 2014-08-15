# -*- coding: utf-8 -*-
from cgitb import html

__author__ = 'raugustyn'

# ####################################
# Standard modules import
# ####################################
import urllib2
import gzip
import os
import sys
import datetime


# ####################################
# Specific modules import
# ####################################
from log import logger, clearLogFile
from infofile import infoFile
from htmllog import htmlLog

# Setup path to RUIANToolbox
import os.path, sys
basePath = os.path.join(os.path.dirname(__file__), "../..")
if not basePath in sys.path: sys.path.append(basePath)

from SharedTools.Config import pathWithLastSlash
from SharedTools.Config import Config

def convertImportRUIANCfg(config):
    if config == None: return

    def isTrue(value):
        return value != None and value.lower() == "true"

    config.downloadFullDatabase = isTrue(config.downloadFullDatabase)
    config.uncompressDownloadedFiles = isTrue(config.uncompressDownloadedFiles)
    config.runImporter = isTrue(config.runImporter)
    config.dataDir = pathWithLastSlash(config.dataDir)
    infoFile.load(config.dataDir + "info.txt")
    pass

config = Config("RUIANDownload.cfg",
            {
                "downloadFullDatabase" : False,
                "uncompressDownloadedFiles" : True,
                "runImporter" : False,
                "dataDir" : "DownloadedData\\",
                "automaticDownloadTime" : "",
                "downloadURL" : "http://vdp.cuzk.cz/vdp/ruian/vymennyformat/vyhledej?vf.pu=S&_vf.pu=on&_vf.pu=on&vf.cr=U&vf.up=OB&vf.ds=K&_vf.vu=on&_vf.vu=on&_vf.vu=on&_vf.vu=on&vf.uo=A&search=Vyhledat"
            },
           convertImportRUIANCfg)

def extractFileName(fileName):
    lastDel = fileName.rfind(os.sep)
    return fileName[lastDel + 1:]


def getFileExtension(fileName):
    """ Returns fileName extension part dot including (.txt,.png etc.)"""
    return fileName[fileName.rfind("."):]


def ___filePercentageInfo(fileSize, downloadedSize):
    status = r"%10d  [%3.2f%%]" % (downloadedSize, downloadedSize * 100. / fileSize)
    logger.info(status)

filePercentageInfo = ___filePercentageInfo


def __fileDownloadInfo(fileName, fileSize):
    logger.info("Downloading: %s Bytes: %s" % (extractFileName(fileName), fileSize))

fileDownloadInfo = __fileDownloadInfo


class DownloadInfo:
    def __init__(self):
        self.fileName = ""
        self.fileSize = 0
        self.compressedFileSize = 0
        self.downloadTime = ""
        pass


def cleanDirectory(folder):
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
                logger.error(e.message, str(e))


def getFileContent(fileName):
    logger.debug("getFileContent")
    with open(fileName, "r") as f:
        lines = f.read().splitlines()
        f.close()
    return lines


def formatTimeDelta(timeDelta):
    v = str(timeDelta)

    #s = timeDelta.seconds
    #hours = s // 3600
    # remaining seconds
    #s = s - (hours * 3600)
    # minutes
    #minutes = s // 60
    # remaining seconds
    #seconds = s - (minutes * 60)

    v = v.strip("0")
    if v[0:1] == ".":
        v = "0" + v
    return v + "s"


class RUIANDownloader:
    pageURL         = "http://vdp.cuzk.cz/vdp/ruian/vymennyformat/vyhledej?vf.pu=S&_vf.pu=on&_vf.pu=on&vf.cr=U&vf.up=ST&vf.ds=K&_vf.vu=on&vf.vu=G&_vf.vu=on&vf.vu=H&_vf.vu=on&_vf.vu=on&search=Vyhledat"
    FULL_LIST_URL   = "http://vdp.cuzk.cz/vdp/ruian/vymennyformat/seznamlinku?vf.pu=S&_vf.pu=on&_vf.pu=on&vf.cr=U&vf.up=ST&vf.ds=K&_vf.vu=on&vf.vu=G&_vf.vu=on&vf.vu=H&_vf.vu=on&_vf.vu=on&search=Vyhledat"
    UPDATE_PAGE_URL = 'http://vdp.cuzk.cz/vdp/ruian/vymennyformat/vyhledej?vf.pu=S&_vf.pu=on&_vf.pu=on&vf.cr=Z&vf.ds=K&_vf.vu=on&vf.vu=G&_vf.vu=on&vf.vu=H&_vf.vu=on&_vf.vu=on&search=Vyhledat&vf.pd='

    def __init__(self, aTargetDir = ""):
        self._targetDir = ""
        self.setTargetDir(aTargetDir)
        self.downloadInfos = []
        self.downloadInfo = None
        self._fullDownload = True
        self.pageURL = config.downloadURL
        pass

    def getTargetDir(self):
        return self._targetDir

    def setTargetDir(self, aTargetDir):
        if aTargetDir != "":
            if aTargetDir.rfind("\\") != len(aTargetDir) - 1:
                aTargetDir += "\\"
            if not os.path.exists(aTargetDir):
                os.makedirs(aTargetDir)
        self._targetDir = aTargetDir
        pass

    targetDir = property(fget = getTargetDir, fset = setTargetDir)

    def getFullSetList(self):
        logger.debug("RUIANDownloader.getFullSetList")
        self._fullDownload = True
        return self.getList(self.pageURL)

    def getList(self, url):
        logger.info("Downloading list of files from " + url)
        html = urllib2.urlopen(url).read()
        result = []

        tablePos = html.find('<table id="i"')
        if tablePos >= 0:
            refTable = html[tablePos:]
            refTable = refTable[refTable.find('<tbody>'):]
            refTable = refTable[:refTable.find("</table>")]
            hrefs = refTable.split('href="')
            for line in hrefs:
                if line[:5] == 'http:':
                    href = line[:line.find('"')]
                    result.append(href)
        return result

    def getUpdateList(self, fromDate = ""):
        logger.debug("RUIANDownloader.getUpdateList since %s", infoFile.validFor())
        self._fullDownload = False
        if fromDate == "" or infoFile.validFor() != "":
            v = infoFile.validFor()
            dateStr = v[8:10] + "." + v[5:7] + "." + v[0:4]
            return self.getList(self.UPDATE_PAGE_URL + dateStr)
        else:
            return []

    def buildIndexHTML(self):
        def addCol(value, tags = ""):
            htmlLog.addCol(value, tags)

        def addDownloadHeader():
            if self._fullDownload:
                headerText = "Úplné stažení dat"
            else:
                headerText = "Stažení aktualizací"
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
        htmlLog.save(config.dataDir + "index.html")
        pass

    def downloadURLList(self, urlList):

        def buildDownloadInfosList():
            self.downloadInfos = []
            for href in urlList:
                self.downloadInfo = DownloadInfo()
                self.downloadInfo.fileName = href.split('/')[-1]
                self.downloadInfos.append(self.downloadInfo)

        logger.debug("RUIANDownloader.downloadURLList")
        buildDownloadInfosList()
        index = 0
        for href in urlList:
            self.downloadInfo = self.downloadInfos[index]
            index = index + 1
            fileName = self.downloadURLtoFile(href)
            if config.uncompressDownloadedFiles:
                self.uncompressFile(fileName, True)
            self.buildIndexHTML()
        pass

    def downloadURLtoFile(self, url):
        logger.debug("RUIANDownloader.downloadURLtoFile")
        file_name = self.targetDir + url.split('/')[-1]
        logger.info("Dodnloading " + url + " -> " + extractFileName(file_name))

        startTime = datetime.datetime.now()
        req = urllib2.urlopen(url)
        meta = req.info()
        fileSize = int(meta.getheaders("Content-Length")[0])
        fileDownloadInfo(file_name, fileSize)
        CHUNK = 1024*1024
        file_size_dl = 0
        with open(file_name, 'wb') as fp:
            while True:
                chunk = req.read(CHUNK)
                if not chunk:
                    break
                fp.write(chunk)
                file_size_dl += len(chunk)
                logger.info(r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100.0 / fileSize))
                self.downloadInfo.compressedFileSize = file_size_dl
                self.buildIndexHTML()
            fp.close()
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
        logger.debug("RUIANDownloader.uncompressFile")
        ext = getFileExtension(fileName).lower()
        if ext == ".gz":
            outFileName = fileName[:-len(ext)]
            logger.info("Uncompressing " + extractFileName(fileName) + " -> " + extractFileName(outFileName))
            f = gzip.open(fileName, 'rb')
            # @TODO tady by se melo cist po kouskach
            fileContent = f.read()
            f.close()
            out = open(outFileName, "wb")
            out.write(fileContent)
            self.downloadInfo.fileSize = len(fileContent)
            out.close()
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
                return datetime.datetime.strptime(dateTimeStr, "%Y-%m-%d %H:%M:%S.%f").date() == datetime.datetime.now().date()

        if wasItToday(infoFile.lastFullDownload):
            logger.warning("Process stopped! Nothing to download. Last full download was done Today " + infoFile.lastFullDownload)
            return
        elif not self._fullDownload and wasItToday(infoFile.lastPatchDownload):
            logger.warning("Process stopped! Nothing to download. Last patch was downloaded Today " + infoFile.lastPatchDownload)
            return

        startTime = datetime.datetime.now()

        if self._fullDownload or infoFile.lastFullDownload == "":
            logger.info("Running in full mode")
            logger.info("Cleaning directory " + config.dataDir)
            cleanDirectory(config.dataDir)
            if config.dataDir != "" and not os.path.exists(config.dataDir):
                os.mkdir(config.dataDir)

            l = self.getFullSetList()
            infoFile.lastFullDownload = str(datetime.datetime.now())
            infoFile.lastPatchDownload = ""
        else:
            logger.info("Running in update mode")
            l = self.getUpdateList()
            infoFile.lastPatchDownload = str(datetime.datetime.now())

        if len(l) > 0:   # stahujeme jedině když není seznam prázdný
            self.downloadURLList(l)
            infoFile.save()
            self.saveFileList(l)
        else:
            logger.warning("Nothing to download, list is empty.")

        self.buildIndexHTML()  # informaci o pokusu downloadovat ale vytváříme stejně
        htmlLog.closeSection(config.dataDir + "index.html")

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
        logger.debug("RUIANDownloader._downloadURLtoFile")
        logger.info("Dodnloading " + url)
        file_name = url.split('/')[-1]
        logger.info(file_name)
        u = urllib2.urlopen(url)
        f = open(self.targetDir + file_name, 'wb')
        meta = u.info()
        file_size = int(meta.getheaders("Content-Length")[0])
        logger.info("Downloading %s Bytes: %s" % (file_name, file_size))

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
        pass


def printUsageInfo():
    logger.info(u'Použití: RUIANDownload.py [-DownloadFullDatabase {True | False}] [-DataDir data_dir] [-UncompressDownloadedFiles {True | False}][-help]')
    logger.info('')
    sys.exit(1)


def main(argv = sys.argv):
    if (argv is not None) or (len(argv) > 1):
        i = 1
        while i < len(argv):
            arg = argv[i].lower()

            if arg == "-downloadfulldatabase":
                i = i + 1
                config.downloadFullDatabase = argv[i].lower() == "True"
            elif arg == "-datadir":
                i = i + 1
                config.dataDir = pathWithLastSlash(argv[i])
                if not os.path.exists(config.dataDir):
                    logger.error("DataDir %s does not exist", config.dataDir)
                    printUsageInfo()
            elif arg == "-uncompressdownloadedfiles":
                i = i + 1
                config.uncompressDownloadedFiles = argv[i].lower() == "True"
            else:
                logger.error('Unrecognised command option: %s' % arg)
                printUsageInfo()

            i = i + 1
            # while exit

        if config.downloadFullDatabase:
            clearLogFile()

        logger.info("RUIANDownloader")
        logger.info("#############################################")
        logger.info("Data directory : %s",         config.dataDir)
        logger.info("Download full database : %s", str(config.downloadFullDatabase))
        if not config.downloadFullDatabase:
            logger.info("Last full download  : %s", infoFile.lastFullDownload)
            logger.info("Last patch download : %s", infoFile.lastPatchDownload)
        logger.info("---------------------------------------------")

        downloader = RUIANDownloader(config.dataDir)
        downloader._fullDownload = config.downloadFullDatabase
        downloader.download()

        logger.info("Download done.")
        if config.runImporter:
            from RUIANImporter.importRUIAN import doImport
            doImport()


if __name__ == '__main__':
    sys.exit(main())