# -*- coding: utf-8 -*-
from distutils.command.install_egg_info import install_egg_info

__author__ = 'raugustyn'

# ####################################
# Standard modules import
# ####################################
import urllib2, gzip, os, sys, datetime

# ####################################
# Specific modules import
# ####################################
from log import logger
from infofile import infoFile
from htmllog import htmlLog

def pathWithLastSlash(path):
    if path != "" and path[len(path) - 1:] != os.sep:
        path = path + os.sep

    return path

def extractFileName(fileName):
    lastDel = fileName.rfind(os.sep)
    return fileName[lastDel + 1:]

class Config:
    ADMIN_NAME = 'admin'
    ADMIN_PASSWORD = 'bar67gux7hd6f5ge6'
    dataDir = ""
    uncompressDownloadedFiles = True

    def __init__(self, configFileName):
        inFile = open(configFileName, "r")
        lines = inFile.readlines()
        inFile.close()

        for line in lines:
            # Using "#" character as comment identifier -> remove everything after this
            if line.find("#") >= 0:
                    line = line[:line.find("#") - 1]
            line = line.rstrip()
            lineParts = line.split("=")
            name = lineParts[0].lower()
            if len(lineParts) > 1:
                value = lineParts[1]
            else:
                value = ""

            if name == "datadir":
                self.dataDir = pathWithLastSlash(value)
            elif name == "uncompressdownloadedfiles":
                self.uncompressDownloadedFiles = value == "True"

        infoFile.load(self.dataDir + "Info.txt")


config = Config("RUIANDownload.cfg")

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
        pass

def formatListURL(patternURL, fullList, fromDate):
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

            except Exception, e:
                logger.error(e.message, str(e))
        os.rmdir(folder)

class RUIANDownloader:
    pageURL         = "http://vdp.cuzk.cz/vdp/ruian/vymennyformat/vyhledej?vf.pu=S&_vf.pu=on&_vf.pu=on&vf.cr=U&vf.up=ST&vf.ds=K&_vf.vu=on&vf.vu=G&_vf.vu=on&vf.vu=H&_vf.vu=on&_vf.vu=on&search=Vyhledat"
    FULL_LIST_URL   = "http://vdp.cuzk.cz/vdp/ruian/vymennyformat/seznamlinku?vf.pu=S&_vf.pu=on&_vf.pu=on&vf.cr=U&vf.up=ST&vf.ds=K&_vf.vu=on&vf.vu=G&_vf.vu=on&vf.vu=H&_vf.vu=on&_vf.vu=on&search=Vyhledat"
    UPDATE_PAGE_URL = 'http://vdp.cuzk.cz/vdp/ruian/vymennyformat/vyhledej?vf.pu=S&_vf.pu=on&_vf.pu=on&vf.cr=Z&vf.ds=K&_vf.vu=on&vf.vu=G&_vf.vu=on&vf.vu=H&_vf.vu=on&_vf.vu=on&search=Vyhledat&vf.pd='
    VALID_START_ID  = '<div class="platnost">Platnost dat ISUI k:<br/>'
    VALID_END_ID    = '</div>'


    def __init__(self, aTargetDir = ""):
        self._targetDir = ""
        self.setTargetDir(aTargetDir)
        self.downloadInfos = []
        self.downloadInfo = None
        self._fullDownload = True
        pass

    def getTargetDir(self):
        return self._targetDir

    def setTargetDir(self, aTargetDir):
        if aTargetDir != "":
            if aTargetDir.rfind("\\") != len(aTargetDir) - 1:
                aTargetDir = aTargetDir + "\\"
            if not os.path.exists(aTargetDir):
                os.makedirs(aTargetDir)
        self._targetDir = aTargetDir
        pass

    targetDir = property(fget = getTargetDir, fset = setTargetDir)

    def getFullSetList(self):
        logger.debug("RUIANDownloader.getFullSetList")
        self._fullDownload = True
        return self.getList(self.pageURL)

    def getFileContent(self, fileName):
        logger.debug("RUIANDownloader.getFileContent")
        f = open(fileName, "r")
        lines = f.read().splitlines()
        f.close()
        return lines

    def getList(self, url):
        logger.debug("RUIANDownloader.getList")
        html = urllib2.urlopen(url).read()
        result = []

        validStart = html.find(self.VALID_START_ID)
        validHTML = html[validStart + len(self.VALID_START_ID):]
        validHTML = validHTML[:validHTML.find(self.VALID_END_ID)]
        logger.debug("Valid:%s", validHTML)
        # write valid for info

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
        logger.debug("RUIANDownloader.getUpdateList")
        self._fullDownload = False
        if fromDate == "" or infoFile.validFor() != "":
            logger.debug("Date:%s", infoFile.validFor())
            return self.getList(self.UPDATE_PAGE_URL + infoFile.validFor())
        else:
            return []

    def buildIndexHTML(self):
        htmlLog.clear()

        def addCol(value):
            htmlLog.addCol(value)

        if self._fullDownload:
            htmlLog.addHeader("Úplné stažení dat")
        else:
            htmlLog.addHeader("Stažení aktualizace")

        htmlLog.openTable()
        htmlLog.htmlCode += "<tr><th>Soubor</th><th>Staženo</th><th>Velikost</th></tr>"
        for info in self.downloadInfos:
            htmlLog.closeTableRow()
            addCol(extractFileName(info.fileName))
            addCol(info.compressedFileSize)
            addCol(info.fileSize)
            htmlLog.closeTableRow()
        htmlLog.closeTable()

        htmlLog.save(config.dataDir + "index.html")

        pass

    def downloadURLList(self, list, uncompress = True):
        logger.debug("RUIANDownloader.downloadURLList")
        self.downloadInfos = []
        for href in list:
            self.downloadInfo = DownloadInfo()
            self.downloadInfos.append(self.downloadInfo)
            #fileName = self.downloadURLtoFile(href)
            #if config.uncompressDownloadedFiles:
            #    self.uncompressFile(fileName, True)
            self.buildIndexHTML()

        self.buildIndexHTML()

        pass

    def downloadURLtoFile(self, url):
        logger.debug("RUIANDownloader.downloadURLtoFile")
        file_name = self.targetDir + url.split('/')[-1]
        logger.info("Dodnloading" + url + " ->" + extractFileName(file_name))

        req = urllib2.urlopen(url)
        meta = req.info()
        fileSize = int(meta.getheaders("Content-Length")[0])
        #logger.info("Downloading: %s %s Bytes" % (file_name, fileSize))
        fileDownloadInfo(file_name, fileSize)
        CHUNK = 1024*1024
        file_size_dl = 0
        with open(file_name, 'wb') as fp:
            while True:
                chunk = req.read(CHUNK)
                if not chunk: break
                fp.write(chunk)
                file_size_dl += len(chunk)
                logger.info(r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / fileSize))
            fp.close()
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
            logger.info("Uncompressing " + extractFileName(fileName) + "->" + extractFileName(outFileName))
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

        if self._fullDownload:
            logger.info("Running in full mode")
            if wasItToday(infoFile.lastFullDownload):
                logger.info("Nothing to download. Last full download was done Today")
                return
            else:
                logger.info("Cleaning directory " + config.dataDir)
                cleanDirectory(config.dataDir)
                os.mkdir(config.dataDir)

                l = self.getFullSetList()
                infoFile.lastFullDownload = str(datetime.datetime.now())
                infoFile.lastPatchDownload = ""
        else:
            if wasItToday(infoFile.lastPatchDownload):
                logger.info("Nothing to download. Last patch was downloaded Today")
                return
            else:
                logger.info("Running in update mode")
                l = self.getUpdateList()
                infoFile.lastPatchDownload = str(datetime.datetime.now())

        self.downloadURLList(l)
        infoFile.save()

    def _downloadURLtoFile(self, url):
        logger.debug("RUIANDownloader._downloadURLtoFile")
        logger.info("Dodnloading" + url)
        file_name = url.split('/')[-1]
        logger.info(file_name)
        u = urllib2.urlopen(url)
        f = open(self.targetDir + file_name, 'wb')
        meta = u.info()
        file_size = int(meta.getheaders("Content-Length")[0])
        logger.info("Downloading: %s Bytes: %s" % (file_name, file_size))

        file_size_dl = 0
        block_sz = 8192
        while True:
            buffer = u.read(block_sz)
            if not buffer:
                break

            file_size_dl += len(buffer)
            f.write(buffer)
            filePercentageInfo(file_size, file_size_dl)

        f.close()
        pass

def printUsageInfo():
    logger.info('Usage: RUIANDownload.py [-mode {full | update}] [-datadir data_dir] [-help]')
    logger.info('')
    sys.exit( 1 )

def main(argv = sys.argv):
    fullMode = True
    if (argv != None) or (len(argv) > 1):

        i = 1
        while i < len(argv):
            arg = argv[i].lower()

            if arg == "-mode":
                i = i + 1
                fullMode = argv[i].lower() == "full"
            elif arg == "-datadir":
                i = i + 1
                config.dataDir = pathWithLastSlash(argv[i])
                if not os.path.exists(config.dataDir):
                    logger.error("DataDir %s does not exist", config.dataDir)
                    printUsageInfo()
            else:
                logger.error('Unrecognised command option: %s' % arg)
                printUsageInfo()

            i = i + 1
            # while exit

        logger.info("Data directory : %s",      config.dataDir)
        logger.info("Full mode : %s",           str(fullMode))
        logger.info('Last full download : %s',  infoFile.lastFullDownload)
        logger.info('Last patch download : %s', infoFile.lastPatchDownload)

        downloader = RUIANDownloader(config.dataDir)
        downloader.download()

if __name__ == '__main__':
    sys.exit(main())