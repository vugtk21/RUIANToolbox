# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        config_tests
# Purpose:     Module config testing routines.
#
# Author:      Radek Augustýn
# Copyright:   (c) VUGTK, v.v.i. 2014
# License:     CC BY-SA 4.0
#-------------------------------------------------------------------------------

import sharedtools.config

print sharedtools.config.RUIANDownloadInfoFile()

config = sharedtools.config.Config("RUIANDownload.cfg",
                                   {
                "downloadFullDatabase" : False,
                "uncompressDownloadedFiles" : False,
                "runImporter" : False,
                "dataDir" : "DownloadedData\\",
                "automaticDownloadTime" : "",
                "downloadURLs" : "http://vdp.cuzk.cz/vdp/ruian/vymennyformat/vyhledej?vf.pu=S&_vf.pu=on&_vf.pu=on&vf.cr=" + \
                                 "U&vf.up=ST&vf.ds=K&vf.vu=Z&_vf.vu=on&_vf.vu=on&vf.vu=H&_vf.vu=on&_vf.vu=on&search=Vyhledat;" + \
                                 "http://vdp.cuzk.cz/vdp/ruian/vymennyformat/vyhledej?vf.pu=S&_vf.pu=on&_vf.pu=on&vf.cr=U&" +\
                                 "vf.up=OB&vf.ds=K&vf.vu=Z&_vf.vu=on&_vf.vu=on&_vf.vu=on&_vf.vu=on&vf.uo=A&search=Vyhledat",
                "ignoreHistoricalData": True
            },
                                   None,
                                   defSubDir = "RUIANDownloader")

print "File name:", config.fileName
print "Ignore historical data:", config.ignoreHistoricalData
