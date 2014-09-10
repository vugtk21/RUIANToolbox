# -*- coding: utf-8 -*-
__author__ = 'Augustyn'

import importRUIAN

# Setup path to RUIANToolbox
import os.path, sys
basePath = os.path.join(os.path.dirname(__file__), "../..")
if not basePath in sys.path: sys.path.append(basePath)

from RUIANDownloader.infofile import infoFile

#infoFile.load("C:\\Users\\raugustyn\\Desktop\\RUIANToolbox\\RUIANDownloader\\DownloadedData\\info.txt")
#print infoFile.validFor()

#(startDate, endDate, type) = importRUIAN.extractDates("C:\\Users\\raugustyn\\Desktop\\RUIANToolbox\\RUIANDownloader\\DownloadedData\\Patch_2014.08.27.txt")

print importRUIAN.renameFile("C:\\Users\\raugustyn\\Desktop\\RUIANToolbox\\RUIANDownloader\\DownloadedData\\Patch_2014.08.27.txt", "__")