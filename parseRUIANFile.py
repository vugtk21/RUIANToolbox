# -*- coding: cp1250 -*-
#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Radecek
#
# Created:     27/04/2013
# Copyright:   (c) Radecek 2013
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import xml.parsers.expat
#import euradinConfig
import configRUIAN, DBHandlers, textFile_DBHandler
import os

elemCount = 0
elemPath = []
elemLevel = 0;
elemPathStr = ""
elemName = ""
vfFileName = "G:\\02_OpenIssues\\07_Euradin\\01_Data\\20130331_OB_539228_UKSH.xml"
#vfFileName = "G:\02_OpenIssues\07_Euradin\01_Data\20130331_OB_554782_UKSH.xml"

insideTable = False
tableName = None
allowedColumns = None
recordCloseTagName = ""
removeNamespace = True
recordValues = {}
columnName = ""

dbHandler = textFile_DBHandler.Handler("G:\\02_OpenIssues\\07_Euradin\\01_Data\\")

class ExpatNode:
    def __init__(self, aLevel):
        self.level = aLevel
        pass

def getTabs(numTabs):
    result = ""
    for i in range(1, numTabs):
        result = result + "\t"

    return result

def removeFileExt(fileName):
    lastDotIndex = fileName.rfind(".")
    if lastDotIndex >= 0:
        return fileName[0:lastDotIndex]
    else:
        return fileName

def newRecord():
    global recordValues, columnName
    recordValues = {}
    columnName = ""
    pass

# ##############################################################################
# Start element Handler
# ##############################################################################
def start_element(name, attrs):
    global elemCount, elemLevel, elemPath, elemPathStr, elemName, allowedColumns, recordCloseTagName, removeNamespace, recordValues, columnName, insideTable, tableName
    elemCount = elemCount + 1
    elemLevel = elemLevel + 1
    elemName = name
    name = name.replace("vf:", "")  # remove namespace prefix

    # Jestliže jsme na úrovni datových tabulek, založíme ji
    if elemPathStr == "VymennyFormat\\Data":
        if (configRUIAN.tableDef.has_key(name)):
            tableName = name
            dbHandler.createTable(tableName, True)
            insideTable = True

            config = configRUIAN.tableDef[name]
            removeNamespace = config["skipNamespacePrefix"]

            # Najdeme sloupce k importu
            if config.has_key("field"):
                 fieldDefs = config["field"]
                 allowedColumns = fieldDefs.keys()
            else:
                allowedColumns = None
            print "allowedColumns:", allowedColumns

            recordCloseTagName = ""
        else:
            print name, "properties are not configured."

    elif insideTable: # jsme uvnitř tabulky
        if recordCloseTagName == "": # new table record
            recordCloseTagName = name
            newRecord()
        elif (allowedColumns != None):
            if removeNamespace:
                doubleDotPos = name.find(":")
                if doubleDotPos >= 0:
                    name = name[doubleDotPos + 1:]

            if name in allowedColumns: # start of allowed column
                columnName = name
    else:
        # Skipped tags
        pass

    elemPath.append(name)
    elemPathStr = "\\".join(elemPath)


# ##############################################################################
# End element Handler
# ##############################################################################
def end_element(name):
    global elemLevel, elemPath, elemPathStr, insideTable, tableName, allowedColumns, recordCloseTagName, columnName, recordValues
    name = name.replace("vf:", "")  # remove namespace prefix
    if tableName == name:
        insideTable = False
        tableName = None
        allowedColumns = None
    elif recordCloseTagName == name:
        recordCloseTagName = ""
        if insideTable:
            dbHandler.writeRowToTable(tableName, recordValues)
            recordValues = {}

    elemPath.remove(elemPath[len(elemPath) - 1])
    elemPathStr = "\\".join(elemPath)
    elemLevel = elemLevel - 1
    pass

def char_data(data):
    global columnName, recordValues
    if columnName != "":
        recordValues[columnName] = repr(data)

# MAIN ROUTINE
p = xml.parsers.expat.ParserCreate()

# Assign event handlers to expat parser
p.StartElementHandler = start_element
p.EndElementHandler = end_element
p.CharacterDataHandler = char_data

# Open and process XML file
f = open(vfFileName, "rt")
p.ParseFile(f)
f.close()

print (elemCount, "xml elements read")