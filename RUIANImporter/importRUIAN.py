# -*- coding: utf-8 -*-
__author__ = 'Augustyn'

import codecs

def strTo127(s):
    result = ""
    for index in range(len(s)):
        ch = s[index:index + 1]
        if ord(ch) >= 32 and ord(ch) <= 127:
            result += ch
    return result

class Config:
    DATABASENAME_KEY = 'dbname'
    HOST_KEY         = 'host'
    PORT_KEY         = 'port'
    USER_KEY         = 'user'
    PASWORD_KEY      = 'password'
    SCHEMANAME_KEY   = 'schemaName'
    LAYERS_KEY       = 'layers'

    databaseName = "euradin"
    host = "localhost"
    port = ""
    user = "postgres"
    password = "ahoj"
    schema = "default"
    layers = ""


    def __init__(self, fileName):
        inFile = codecs.open(fileName, "r", "utf-8")
        lines = inFile.readlines()
        inFile.close()

        for line in lines:
            # Using "#" character as comment identifier -> remove everything after this
            if line.find("#") >= 0:
                    line = line[:line.find("#") - 1]
            line = strTo127(line.strip())
            lineParts = line.split("=")
            name = lineParts[0].lower()
            if len(lineParts) > 1:
                value = lineParts[1]
            else:
                value = ""

            if name == self.DATABASENAME_KEY:
                self.databaseName = value
            elif name == self.HOST_KEY:
                self.host = value
            elif name == self.PORT_KEY:
                self.port = value
            elif name == self.USER_KEY:
                self.user = value
            elif name == self.PASWORD_KEY:
                self.password = value
            elif name == self.SCHEMANAME_KEY:
                self.schema = value
            elif name == self.LAYERS_KEY:
                self.layers = value

config = Config("importruian.cfg")

def buildImportBatFile():
	print "Building VFR to PostGIS batch file"
	content = '@python "%OSGEO4W_ROOT%\\bin\\vfr2pg.py"'
	content += " --file " + "ListFiles3.txt"
	content += " --user " + config.user
	content += " --passwd " + config.password
	if config.layers != "":
		content += " --layer " + config.password
	content += " --append"

	file = open("download.bat", "w")
	file.write(content)
	file.close()
	print "Done."


#@python "%OSGEO4W_ROOT%\bin\vfr2pg.py" --file ListFiles3.txt --dbname euradin_full --user postgres --passwd ahoj --layer Obce,CastiObci,Zsj,AdresniMista --append

buildImportBatFile()