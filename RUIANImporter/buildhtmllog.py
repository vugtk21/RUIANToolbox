# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        buildhtmllog
# Purpose:     Builds HTML log file in imported directory.
#
# Author:      Radek Augustýn
# Copyright:   (c) VUGTK, v.v.i. 2014
# License:     CC BY-SA 4.0
#-------------------------------------------------------------------------------
helpStr = """
Builds import HTML Log file.

Requires: Python 2.7.5 or later

Usage: buildhtmllog.py

"""

TXT_EXTENSION = ".txt"
LOG_EXTENSION = ".log"

DATE_STR_EXAMPLE = "2014.11.09"
DETAILS = [".VFRlog", ".VFRerr"]

import shared; shared.setupPaths()
from SharedTools.config import getDataDirFullPath, RUIANImporterConfig
import sys, codecs, os, time

def getLogFileNames(fileName):
    result = []

    fileName = os.path.basename(fileName)
    fileName = fileName[:len(fileName) - len(TXT_EXTENSION)]
    fileName = fileName.lower()
    isDownload = True
    for prefix in ["download_", "patch_"]:
        if fileName.startswith(prefix):
            dateStr = fileName[len(prefix):]
            if len(dateStr) == len(DATE_STR_EXAMPLE):
                for detail in DETAILS:
                    result.append("__" + prefix + dateStr + detail + LOG_EXTENSION)
        isDownload = False

    return result

htmlTemplate = u"""<html>
    <head>
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
        <title>Detaily importů do databáze RÚIAN</title>
        <style>
            body {
                font-family:Tahoma;
				color:#353833;
				font-size:small;
				margin: 0px 20px 0px 20px;
            }

			tr, td, th {
                vertical-align:top;
				font-size:small;
			}

			h1, h2 {
				font-size:large;
				color: #2c4557;
				font-weight:normal;
				padding: 10px 0px 0px 0px;
				margin: 0px 0px 0px 0px;
			}

			h1 {
				font-size:larger;
				font-weight:bold;
			}

			th {
				color: #353833;
				padding: 3px 5px 3px 5px;
				margin:0px 0px 0px 0px;
				border-top-color: #9eadc0;
				border-top-width: 1px;
				border-bottom-color: #9eadc0;
				border-bottom-width: 1px;
				background-color:rgb(222, 227, 233);
			}

			table td {
				padding: 2px 5px 2px 5px;
			}

			.altColor {
				background-color:rgb(238, 238, 239);
			}

        </style>
    </head>
    <body>
        <h1>Detaily importů do databáze RÚIAN</h1>
        <br>Databáze <b>#DATABASE_NAME#</b> na serveru #DATABASE_SERVER#:#DATABASE_PORT# je aktuální k #DATABASE_DATE#.
        #LAYERS_DETAILS#
        <br><br>
        #IMPORTS_TABLE_ID#
    </body>
</html>
"""

DATABASE_SERVER_ID = "#DATABASE_SERVER#"
DATABASE_PORT_ID   = "#DATABASE_PORT#"
DATABASE_NAME_ID   = "#DATABASE_NAME#"
IMPORTS_TABLE_ID   = "#IMPORTS_TABLE_ID#"
DATABASE_DATE_ID   = "#DATABASE_DATE#"
LAYERS_DETAILS_ID  = "#LAYERS_DETAILS#"

def buildHTMLLog():
    IMPORT_TYPES = [u"Aktualizace", u"Stavová databáze"]
    dataPath = getDataDirFullPath()
    config = RUIANImporterConfig()
    log = htmlTemplate

    log = log.replace(DATABASE_SERVER_ID, config.host)
    log = log.replace(DATABASE_PORT_ID, config.port)
    log = log.replace(DATABASE_NAME_ID, config.dbname)
    log = log.replace(DATABASE_DATE_ID, time.strftime("%d.%m.20%y"))

    if config.layers == "":
        msg = u"Do databáze jsou načteny všechny vrstvy."
    else:
        msg = u"Do databáze jsou načteny vrstvy %s." % config.layers
    log = log.replace(LAYERS_DETAILS_ID, msg)


    importsTable = u"<table>"
    importsTable += u'<tr valign="bottom"><th>Datum</th><th>Typ importu</th><th>Konverze<br>VFR</th><th>Chyby</th></tr>'
    for file in os.listdir(dataPath):
        fileName = file.lower()
        if fileName.endswith(TXT_EXTENSION):
            fileName = fileName[:len(fileName) - len(TXT_EXTENSION)]
            date = ""
            isDownload = True
            for prefix in ["__download_", "__patch_"]:
                if fileName.startswith(prefix):
                    dateStr = fileName[len(prefix):]
                    if len(dateStr) == len("2014.11.09"):
                        importsTable += '<tr><td>%s</td><td><a href="%s">%s</a></td>' % (dateStr, prefix + dateStr + TXT_EXTENSION, IMPORT_TYPES[isDownload])
                        for detail in DETAILS:
                            detailName = prefix + dateStr + detail + LOG_EXTENSION
                            fileName = dataPath + detailName
                            caption = ""
                            if os.path.exists(fileName) and os.path.getsize(fileName) != 0:
                                caption = "Info"
                            importsTable += u'<td align="center"><a href="%s">%s</a></td>' % (detailName, caption)

                        importsTable += "</tr>"
                isDownload = False

    importsTable += "</table>"
    log = log.replace(IMPORTS_TABLE_ID, importsTable)

    outF = codecs.open(dataPath + "Import.html", "w", "utf-8")
    try:
        outF.write(log)
    finally:
        outF.close()


def main(argv = sys.argv):
    from SharedTools.config import RUIANDownloadConfig
    config = RUIANDownloadConfig()
    config.loadFromCommandLine(argv, helpStr)
    print "Building import HTML Log file."
    buildHTMLLog()
    print "Done."

if __name__ == '__main__':
    main()