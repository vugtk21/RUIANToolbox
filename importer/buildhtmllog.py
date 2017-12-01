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
from sharedtools.config import getDataDirFullPath, RUIANImporterConfig
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
        <title>Detaily importů z databáze RÚIAN</title>
        <style>
	        body {
	            font-family: Arial;
			    font-size: small;
			    color: #575757;
			    margin: 10 10 10 10;
	        }

			a {
                color: #1370AB;
		    }

            tr, td, th {
                vertical-align:top;
				font-size:small;
			}

            th {
                background-color: #1370AB;
                color : #fff;
            }


			h1, h2 {
				font-size:large;
				color: #2c4557;
				font-weight:normal;
				padding: 10px 0px 0px 0px;
				margin: 0px 0px 0px 0px;
			}

            h1 {
                color: #1370AB;
			    border-bottom: 1 solid #B6B6B6;
            }

            table {
                border-collapse: collapse;
        	    font-size: small;
                border: 1px solid #4F81BD;
            }

            td, th {
                vertical-align:top;
				padding: 2px 5px 2px 5px;
            }

            th {
                border: 1px solid #4F81BD;
            }

            td {
                border-left: 1px solid #4F81BD;
                border-right: 1px solid #4F81BD;
            }

			.altColor {
				background-color:#C6D9F1;
			}

        </style>
    </head>
    <body>
        <h1>Detaily importů do databáze RÚIAN</h1>
        <br>Databáze <b><a href="../dbdetails">#DATABASE_NAME#</a></b> je aktuální k #DATABASE_DATE#.
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


    oddRow = False
    importsTable = u"<table>"
    importsTable += u'<tr valign="bottom"><th>Datum</th><th>Import</th><th>Konverze<br>VFR</th><th>Chyby</th></tr>'
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
                        importsTable += '<tr %s><td>%s</td><td><a href="%s">%s</a></td>' % (["", 'class="altColor"'][int(oddRow)], dateStr, prefix + dateStr + TXT_EXTENSION, IMPORT_TYPES[isDownload])
                        for detail in DETAILS:
                            detailName = prefix + dateStr + detail + LOG_EXTENSION
                            fileName = dataPath + detailName
                            caption = ""
                            if os.path.exists(fileName) and os.path.getsize(fileName) != 0:
                                caption = "Info"
                            importsTable += u'<td align="center"><a href="%s">%s</a></td>' % (detailName, caption)

                        importsTable += "</tr>"
                        oddRow = not oddRow
                isDownload = False

    importsTable += "</table>"
    log = log.replace(IMPORTS_TABLE_ID, importsTable)

    outF = codecs.open(dataPath + "Import.html", "w", "utf-8")
    try:
        outF.write(log)
    finally:
        outF.close()


def main(argv = sys.argv):
    from sharedtools.config import RUIANDownloadConfig
    config = RUIANDownloadConfig()
    config.loadFromCommandLine(argv, helpStr)
    print "Building import HTML Log file."
    buildHTMLLog()
    print "Done."

if __name__ == '__main__':
    main()