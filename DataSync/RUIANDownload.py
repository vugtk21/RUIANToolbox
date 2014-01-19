# -*- coding: utf-8 -*-
__author__ = 'raugustyn'

# ####################################
# Standard modules import
# ####################################
import urllib2, gzip, os, sys

# ####################################
# Specific modules import
# ####################################
from log import logger
import config

def getFileExtension(fileName):
    """ Returns fileName extension part dot including (.txt,.png etc.)"""
    return fileName[fileName.rfind("."):]

def ___filePercentageInfo(fileSize, downloadedSize):
    status = r"%10d  [%3.2f%%]" % (downloadedSize, downloadedSize * 100. / fileSize)
    logger.info(status)

filePercentageInfo = ___filePercentageInfo

def __fileDownloadInfo(fileName, fileSize):
    logger.info("Downloading: %s Bytes: %s" % (fileName, fileSize))

fileDownloadInfo = __fileDownloadInfo

class DownloadInfo:
    def __init__(self):
        self.fileName = ""
        self.fileSize = 0
        self.compressedFileSize = 0
        pass

class RUIANDownloader:
    pageURL = "http://vdp.cuzk.cz/vdp/ruian/vymennyformat/vyhledej?vf.pu=S&_vf.pu=on&_vf.pu=on&vf.cr=U&vf.up=ST&vf.ds=K&_vf.vu=on&vf.vu=G&_vf.vu=on&vf.vu=H&_vf.vu=on&_vf.vu=on&search=Vyhledat"
    FULL_LIST_URL = "http://vdp.cuzk.cz/vdp/ruian/vymennyformat/seznamlinku?vf.pu=S&_vf.pu=on&_vf.pu=on&vf.cr=U&vf.up=ST&vf.ds=K&_vf.vu=on&vf.vu=G&_vf.vu=on&vf.vu=H&_vf.vu=on&_vf.vu=on&search=Vyhledat"
    UPDATE_PAGE_URL = 'http://vdp.cuzk.cz/vdp/ruian/vymennyformat/vyhledej?vf.pu=S&_vf.pu=on&_vf.pu=on&vf.cr=Z&vf.ds=K&_vf.vu=on&vf.vu=G&_vf.vu=on&vf.vu=H&_vf.vu=on&_vf.vu=on&search=Vyhledat&vf.pd='
    VALID_START_ID = '<div class="platnost">Platnost dat ISUI k:<br/>'
    VALID_END_ID   = '</div>'


    def __init__(self, aTargetDir = ""):
        self._targetDir = ""
        self.setTargetDir(aTargetDir)
        self.downloadInfos = []
        self.downloadInfo = None
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
        vf = open(config.validForFileName(), "w")
        vf.write(validHTML)
        vf.close()

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
        if fromDate == "" or os.path.exists(config.validForFileName()):
            dateStr = open(config.validForFileName(), "r").read().split(" ")[0]
            logger.debug("Date:%s", dateStr)
            return self.getList(self.UPDATE_PAGE_URL + dateStr)
        else:
            return []

    def downloadURLList(self, list, uncompress = True):
        logger.debug("RUIANDownloader.downloadURLList")
        self.downloadInfos = []
        for href in list:
            self.downloadInfo = DownloadInfo()
            self.downloadInfos.append(self.downloadInfo)
            fileName = self.downloadURLtoFile(href)
            self.uncompressFile(fileName, True)

        htmlResult = ""

        def addCol(value):
            global htmlResult
            htmlResult += "<td>" + value + "</td>"

        for info in self.downloadInfos:
            htmlResult += "<tr>"
            addCol(info.fileName)
            addCol(info.compressedFileSize)
            addCol(info.fileSize)
            htmlResult += "</tr>"
        with open("log.html", "w") as outFile:
            outFile.write(htmlResult)
            outFile.close()

        pass

    def downloadURLtoFile(self, url):
        logger.debug("RUIANDownloader.downloadURLtoFile")
        file_name = self.targetDir + url.split('/')[-1]
        print "Dodnloading", url, " ->", file_name
        #return file_name

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
        logger.debug("RUIANDownloader.uncompressFile")
        ext = getFileExtension(fileName).lower()
        if ext == ".gz":
            outFileName = fileName[:-len(ext)]
            logger.info("Uncompressing " + fileName + "->" + outFileName)
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

def Usage():
    print('Usage: RUIANDownload.py [-mode {full | update}] [-workDir work_dir] [-configDir config_dir] [--help-general]')
    print('')

def main(argv = sys.argv):
    if (argv is None) or (len(argv) == 0):
        print('Unrecognised command option: %s' % arg)
        Usage()
        sys.exit(0)
    else:
        fullMode = True
        workDir = config.tempDir
        configDir = config.dataDir

        i = 1
        while i < len(argv):
            arg = argv[i].lower()

            if arg == "-mode":
                i = i + 1
                arg = argv[i].lower()
                fullMode = arg == "full"
            elif arg == "-workDir":
                i = i + 1
                workDir = argv[i]
            elif arg == "-configDir":
                i = i + 1
                configDir = argv[i]
            else:
                print('Unrecognised command option: %s' % arg)
                Usage()
                sys.exit( 1 )

            i = i + 1
            # while exit

        logger.info("Working dir = %s", workDir)
        logger.info("Config dir = %s", configDir)

        config.tempDir = workDir
        config.configDir = configDir

        downloader = RUIANDownloader(workDir)
        if fullMode:
            logger.info("Running in full mode")
            l = downloader.getFullSetList()
        else:
            logger.info("Running in update mode")
            l = downloader.getUpdateList()

        downloader.downloadURLList(l)

if __name__ == '__main__':
    sys.exit(main())
