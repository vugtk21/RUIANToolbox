# -*- coding: cp1250 -*-
#-------------------------------------------------------------------------------
# Name:        parseRUIANfile
# Purpose:     Parsování souboru ve formátu výměnného souboru RUIAN
#
# Author:      Radek Augustýn
#
# Created:     27/04/2013
# Copyright:   (c) Radek Augustýn 2013
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import os, xml.parsers.expat
import configRUIAN, DBHandlers, textFile_DBHandler

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

class RUIANParser:
    """ Třída implementující konverzi z exportního formátu RÚIAN. """
    def __init__(self):
        ''' Nastavuje proměnnou databasePath a inicializuje seznam otevřených
        souborů'''
        pass

    def newRecord():
        self.recordValues = {}
        self.columnName = ""
        pass

    def importData(inputFileName, dbHandler):
        self.dbHandler = dbHandler
        self.elemCount = 0
        self.elemPath = []
        self.elemLevel = 0;
        self.elemPathStr = ""
        self.elemName = ""
        self.insideTable = False
        self.tableName = None
        self.allowedColumns = None
        self.recordCloseTagName = ""
        self.removeNamespace = True
        self.recordValues = {}
        self.columnName = ""

        p = xml.parsers.expat.ParserCreate()

        # Assign event handlers to expat parser
        p.StartElementHandler = start_element
        p.EndElementHandler = end_element
        p.CharacterDataHandler = char_data

        # Open and process XML file
        f = open(inputFileName, "rt")
        p.ParseFile(f)
        f.close()

        print (self.elemCount, "xml elements read")
        pass

        def start_element(name, attrs):
            """ Start element Handler. """
            global allowedColumns, recordCloseTagName, removeNamespace, recordValues, columnName,  tableName
            self.elemCount = self.elemCount + 1
            self.elemLevel = self.elemLevel + 1
            self.elemName = name
            name = name.replace("vf:", "")  # remove the namespace prefix

            # Jestliže jsme na úrovni datových tabulek, založíme ji
            if self.elemPathStr == "VymennyFormat\\Data":
                if (configRUIAN.tableDef.has_key(name)):
                    tableName = name
                    self.dbHandler.createTable(tableName, True)
                    self.insideTable = True

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

            elif self.insideTable: # jsme uvnitř tabulky
                if recordCloseTagName == "": # new table record
                    recordCloseTagName = name
                    self.newRecord()
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

            self.elemPath.append(name)
            self.elemPathStr = "\\".join(self.elemPath)

        def end_element(name):
            """ End element Handler """
            global    tableName, allowedColumns, recordCloseTagName, columnName, recordValues
            name = name.replace("vf:", "")  # remove namespace prefix
            if tableName == name:
                self.insideTable = False
                tableName = None
                allowedColumns = None
            elif recordCloseTagName == name:
                recordCloseTagName = ""
                if self.insideTable:
                    self.dbHandler.writeRowToTable(tableName, recordValues)
                    recordValues = {}

            self.elemPath.remove(self.elemPath[len(self.elemPath) - 1])
            self.elemPathStr = "\\".join(self.elemPath)
            self.elemLevel = self.elemLevel - 1
            pass

        def char_data(data):
            global columnName, recordValues
            if columnName != "":
                recordValues[columnName] = repr(data)


vfFileName = "G:\\02_OpenIssues\\07_Euradin\\01_Data\\20130331_OB_539228_UKSH.xml"
#vfFileName = "G:\02_OpenIssues\07_Euradin\01_Data\20130331_OB_554782_UKSH.xml"

parser = RUIANParser()
parser.importData(vfFileName, textFile_DBHandler.Handler("G:\\02_OpenIssues\\07_Euradin\\01_Data\\"))
