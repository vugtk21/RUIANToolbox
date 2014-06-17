# -*- coding: utf-8 -*-
__author__ = 'Augustyn'

import codecs
import sys

from SharedTools.config import pathWithLastSlash
from SharedTools.config import Config

config = Config("importRUIAN.cfg",
            {
                "dbname" : "euradin",
                "host" : "localhost",
                "port" : "5432",
                "user" : "postgres",
                "password" : "postgres",
                "schemaName" : "",
                "layers" : ""
            }
           )


def buildImportBatFile():
	print "Building VFR to PostGIS batch file"
	content = '@python "%OSGEO4W_ROOT%\\bin\\vfr2pg.py"'
	content += " --file "
	if len(sys.argv) == 2:
		content += sys.argv[1]
	else:
		content += "ListFiles.txt"
	content += " --user " + config.user
	content += " --passwd " + config.password
	if config.layers != "":
		content += " --layer " + config.layers
	content += " --append"

	file = open("download.bat", "w")
	file.write(content)
	file.close()

	print content


def doImport():
    buildImportBatFile()
    #print "Calling GDAL/OGR import...."
    #import subprocess

    #filePath = "download.bat"
    #p = subprocess.Popen(filePath, shell=True, stdout = subprocess.PIPE)

    #stdout, stderr = p.communicate()
    #print p.returncode # is 0 if success


#@python "%OSGEO4W_ROOT%\bin\vfr2pg.py" --file ListFiles3.txt --dbname euradin_full --user postgres --passwd ahoj --layer Obce,CastiObci,Zsj,AdresniMista --append

if __name__ == "__main__":
    doImport()

