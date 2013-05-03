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
import tableDef
import DBTools
import os

# CONSTANTS
GML_FILEEXT = ".gml"

elemCount = 0
elemPath = []
elemLevel = 0;
elemPathStr = ""
elemName = ""
maxPrintLevel = 0
vfFileName = "20130331_OB_539228_UKSH.xml"
vfFileName = "20130331_OB_554782_UKSH.xml"

outXML = None
tableCloseTagName = None
allowedColumns = None
recordCloseTagName = ""
removeNamespace = True
recordValues = {}
columnName = ""


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

def gmlFileName(tableName):
    return tableName + GML_FILEEXT

def newRecord():
    global recordValues, columnName
    recordValues = {}
    columnName = ""
    pass

# ##############################################################################
# Start element Handler
# ##############################################################################
def start_element(name, attrs):
    global elemCount, elemLevel, elemPath, elemPathStr, elemName, outXML, allowedColumns, recordCloseTagName, removeNamespace, recordValues, columnName
    elemCount = elemCount + 1
    elemLevel = elemLevel + 1
    elemName = name
    name = name.replace("vf:", "")  # remove namespace prefix

    # Jestliže jsme na úrovni datových tabulek, založíme ji
    if elemPathStr == "VymennyFormat\\Data":
        if (tableDef.tableDef.has_key(name)):
            config = tableDef.tableDef[name]
            removeNamespace = config["skipNamespacePrefix"]
            if config.has_key("field"):
                 fieldDefs = config["field"]
                 allowedColumns = fieldDefs.keys()
            else:
                allowedColumns = None
            print "allowedColumns:", allowedColumns
            tableCloseTagName = name
            recordCloseTagName = ""
            gmlFileName = removeFileExt(vfFileName) + "_" + name + GML_FILEEXT
            print (name + "->" + gmlFileName)
            if os.path.exists(gmlFileName):
                fileMode = "w" # musí být nastaveno na "a"
            else:
                fileMode = "w"
            outXML = open(gmlFileName, fileMode)
        else:
            print "Table", name, " is not defined."
    elif outXML: # jsme uvnitř tabulky
        if recordCloseTagName == "": # new table record
            recordCloseTagName = name
            newRecord()
            #outXML.write(name + ":")
        elif (allowedColumns != None):
            if removeNamespace:
                doubleDotPos = name.find(":")
                if doubleDotPos >= 0:
                    name = name[doubleDotPos + 1:]

            if name in allowedColumns: # start of allowed column
                #outXML.write(name + ":")
                columnName = name
    else:
        # Skipped tags
        pass

    elemPath.append(name)
    elemPathStr = "\\".join(elemPath)

    if elemLevel < maxPrintLevel:
        print (getTabs(elemLevel) + "<" + name + ">") #+ " (" + elemPathStr +  ")"

# ##############################################################################
# End element Handler
# ##############################################################################
def end_element(name):
    global elemLevel, elemPath, elemPathStr, outXML, tableCloseTagName, allowedColumns, recordCloseTagName, columnName, recordValues
    name = name.replace("vf:", "")  # remove namespace prefix
    if tableCloseTagName == name:
        outXML.close()
        outXML == None
        tableCloseTagName = None
        allowedColumns = None
    elif recordCloseTagName == name:
        recordCloseTagName = ""
        if outXML:
            outXML.write(str(recordValues) + "\n")
            recordValues = {}

    elemPath.remove(elemPath[len(elemPath) - 1])
    elemPathStr = "\\".join(elemPath)
    if elemLevel < maxPrintLevel:
        print (getTabs(elemLevel) + "</" + name + ">")
    elemLevel = elemLevel - 1
    pass

def char_data(data):
    global columnName, recordValues
    if columnName != "":
        recordValues[columnName] = repr(data)
        #columnName = ""

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