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
import os, xml.parsers.expat, gzip, math
import configRUIAN, DBHandlers, textFile_DBHandler, postGIS_DBHandler, configGUI
import sharedTools

# @TODO Dořešit duplicitní vnořené názvy coi:Kod vs obi:Kod
# @TODO Jak vyřešit UTF-8

removeTables = True
DATA_XML_PATH = "VymennyFormat/Data"
XML_PATH_SEPARATOR = "/"

def normalizeTagName(name):
    # Remove namespace prefix, if needed
    if configRUIAN.SKIPNAMESPACEPREFIX:
        doubleDotPos = name.find(":")
        if doubleDotPos >= 0:
            name = name[doubleDotPos + 1:]

    return name

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

def attrDictToStr(attrs):
    if len(attrs) > 0:
        attrArray = []
        for key in attrs:
            attrArray.append(key + '="' + attrs[key] + '"')
        return " " + " ".join(attrArray)

    return ""

def getFieldDef(tableName, fieldName):
    tableDef = configRUIAN.tableDef[tableName]
    if tableDef:
        return tableDef[configRUIAN.FIELDS_KEY_NAME][fieldName]
    else:
        return None

def getGeometryColumnNames(tableName):
    fieldDefs = configRUIAN.tableDef[tableName][configRUIAN.FIELDS_KEY_NAME]
    result = []
    for fieldName in fieldDefs:
        fieldValue = fieldDefs[fieldName]
        if fieldValue[configRUIAN.FIELDTYPE_KEYNAME].find("Multi") == 0:
            result.append(fieldName)

    return result

class RUIANParser:
    """ Třída implementující konverzi z exportního formátu RÚIAN. """
    def __init__(self):
        ''' Nastavuje proměnnou databasePath a inicializuje seznam otevřených
        souborů'''
        self.buildXMLSubPaths()
        pass

    def buildXMLSubPaths(self):
        ''' Vytvoří vlastnost xmlSubPath pro každou definici položky v každé tabulce.
        Zároveň vytvoří pole se seznamem xmlSubPath-s pro každou tabulku.
        '''
        for tableDef in configRUIAN.tableDef.values():
            xmlSubPaths = {}
            fieldDefs = tableDef[configRUIAN.FIELDS_KEY_NAME]
            for fieldName in fieldDefs:
                fieldDef = fieldDefs[fieldName]
                if not fieldDef.has_key(configRUIAN.XMLSUBPATH_KEYNAME):
                    fieldDef[configRUIAN.XMLSUBPATH_KEYNAME] = fieldName
                xmlSubPaths[fieldDef[configRUIAN.XMLSUBPATH_KEYNAME]] = fieldName
            tableDef[configRUIAN.XMLSUBPATH_KEYNAME] = xmlSubPaths
        pass

    def processNewRecordTag(self, recordName):
        self.recordTagName = recordName
        self.recordValues = {}
        self.columnName = ""
        pass

    def processTableOpeningTag(self, dbHandler, name, attrs):
        self.insideImportedTable = sharedTools.isImportedTable(name) # configRUIAN.tableDef.has_key(name)
        self.tableName = name
        self.insideTable = True
        self.xmlSubPaths = {}
        if self.insideImportedTable:
            dbHandler.createTable(self.tableName, removeTables)
            config = configRUIAN.tableDef[name]
            self.xmlSubPaths = config[configRUIAN.XMLSUBPATH_KEYNAME]
            self.recordTagName = ""

            # Najdeme sloupce k importu
            if config.has_key(configRUIAN.FIELDS_KEY_NAME):
                 fieldDefs = config[configRUIAN.FIELDS_KEY_NAME]
                 self.allowedColumns = fieldDefs.keys()
            else:
                self.allowedColumns = None

            self.geometryNames = getGeometryColumnNames(self.tableName)
            self.tableRecordCount = 0
            print "            Importuji tabulku ", self.tableName, ":", self.allowedColumns
        else:
            print name, "properties are not configured."
        pass

    def logTableRecordProgress(self):
        if 1000*math.floor(self.tableRecordCount/1000) == self.tableRecordCount:
            print self.tableRecordCount, "records"

    def logElemCount(self):
        if 50000*math.floor(self.elemCount/50000) == self.elemCount:
            print self.elemCount, "tags"

    def importData(self, inputFileName, dbHandler):
        """ Tato procedura importuje data ze souboru ve formátu výměnného souboru
            RUIAN inputFileName a uloží jednotlivé záznamy pomocí ovladače dbHandler.

            @param {String} inputFileName Vstupní soubor ve formátu výměnného souboru RÚIAN.
            @param {String} inputFileName Vstupní soubor ve formátu výměnného souboru RÚIAN.
        """
        self.elemCount = 0
        self.elemPath = []
        self.elemLevel = 0;
        self.elemPathStr = ""
        self.insideImportedTable = False # True, jestliže právě zpracovávanou tabulku máme zaškrtnutu importovat
        self.tableName = None
        self.allowedColumns = None
        self.recordTagName = ""
        self.recordValues = {}
        self.columnName = ""
        self.columnLevel = -1
        self.xmlSubPaths = {}
        self.tableRecordCount = 0
        self.subXML = []
        self.isGeometry = False
        self.geometryNames = []

        def start_element(name, attrs):
            """ Start element Handler. """
            self.elemCount = self.elemCount + 1
            self.elemLevel = self.elemLevel + 1
            self.logElemCount()

            name = name.replace("vf:", "")  # remove the namespace prefix


            # Jestliže jsme na úrovni datových tabulek, založíme ji
            if self.elemPathStr == DATA_XML_PATH:
                self.processTableOpeningTag(dbHandler, name, attrs)

            elif self.insideImportedTable: # jsme uvnitř tabulky
                if self.recordTagName == "": # new table record
                    self.processNewRecordTag(name)
                elif (self.allowedColumns != None):
                    tagName = name
                    name = normalizeTagName(name)

                    columnPath = self.elemPathStr[len(DATA_XML_PATH + XML_PATH_SEPARATOR + self.tableName + XML_PATH_SEPARATOR + self.recordTagName + XML_PATH_SEPARATOR):]
                    if columnPath <> "":
##                        fieldDefs = configRUIAN.tableDef[self.tableName][configRUIAN.FIELDS_KEY_NAME]
##                        fieldName = fieldDefs.keys()[0]
                        columnPath = columnPath + XML_PATH_SEPARATOR + name
                    else:
                        columnPath = name

                    #if name in self.allowedColumns and self.elemLevel == 5: # start of allowed column
                    if columnPath in self.xmlSubPaths:
                        self.columnName = self.xmlSubPaths[columnPath]
                        self.subXML = []
                        self.isGeometry = self.columnName in self.geometryNames
                    elif self.columnName <> "":
                        # tagy podrizene aktualnimu = GML obsah
                        self.subXML.append("<" + tagName + attrDictToStr(attrs) + ">")
                    else:
                        self.columnName = ""

            else:
                # Skipped tags
                pass

            self.elemPath.append(name)
            self.elemPathStr = XML_PATH_SEPARATOR.join(self.elemPath)

        def end_element(name):
            """ End element Handler """
            name = name.replace("vf:", "")          # remove namespace prefix
            normalizedTagName = normalizeTagName(name)
            # jsme uvnitř importované tabulky
            if self.insideImportedTable:
                # close table
                if self.insideImportedTable and self.tableName == name and self.elemLevel == 3:
                    self.insideImportedTable = False
                    self.tableName = None
                    self.allowedColumns = None
                    print "            Načteno", self.tableRecordCount, "záznamů."

                # close record
                elif self.recordTagName == name:
                    self.recordTagName = ""
                    self.tableRecordCount = self.tableRecordCount + 1
                    self.logTableRecordProgress()
                    #self.tableRecordCount
                    if self.insideImportedTable:
##                        if self.tableName == 'Parcely' and self.recordValues['Id'] == '141':
##                            pass    # ********************* poriznuta, blbe parsovana hodnota  ***********************
                        dbHandler.writeRowToTable(self.tableName, self.recordValues)
                        self.recordValues = {}

                # Close attribute column
                elif self.columnName == normalizedTagName:
                    if len(self.subXML) <> 0 and self.isGeometry:
                        self.recordValues[self.columnName] = "".join(self.subXML)
                        #print "".join(self.subXML)

                    self.subXML = []
                    self.columnName = ""

                # tagy podrizene aktualnimu = GML obsah
                elif (self.columnName <> ""):
                    self.subXML.append("</" + name + ">")
                else:
                    pass
                    # unused tags = errors

            # leave all tags outside imported tables
            else:
                pass

            self.elemPath.remove(self.elemPath[len(self.elemPath) - 1])
            self.elemPathStr = XML_PATH_SEPARATOR.join(self.elemPath)
            self.elemLevel = self.elemLevel - 1
            pass

        def char_data(data):
            if self.columnName <> "":
                if self.recordValues.has_key(self.columnName):
                    self.recordValues[self.columnName] = self.recordValues[self.columnName] + data
                else:
                    self.recordValues[self.columnName] = data
                if len(self.subXML) <> 0:
                    self.subXML.append(data)

        p = xml.parsers.expat.ParserCreate()

        # Assign event handlers to expat parser
        p.StartElementHandler = start_element
        p.EndElementHandler = end_element
        p.CharacterDataHandler = char_data

        # Open and process XML file
        suffix = inputFileName.split('.')[-1]
        if suffix == 'xml':
            f = open(inputFileName, "rt")
        elif suffix == 'gz':
            f = gzip.open(inputFileName, "rb")
        else:
            print "Unexpected file format."

        p.ParseFile(f)
        f.close()

        print self.elemCount, "xml elements read"
        pass

import unittest

class TestRUIANParser(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testimportData(self):
        vfDataPath = "..\\01_Data\\"
        vfFileName = vfDataPath + "20130331_OB_539228_UKSH.xml"
        #vfFileName = vfDataPath + "20130331_OB_554782_UKSH.xml"
        #vfFileName = vfDataPath + "20130331_OB_554782_UZSZ.xml"

        #vfDataPath = "..\\source\\"
        #vfFileName = vfDataPath + "20130331_OB_539228_UKSH.xml"
        #vfFileName = vfDataPath + "20130515_ST_ZZSZ.xml.gz"
        ##vfFileName = vfDataPath + "test_parcely.xml"

        parser = RUIANParser()
        ##db=postGIS_DBHandler.Handler("dbname=euradin host=localhost port=5432 user=postgres password=postgres","public")
        ##parser.importData(vfFileName, db)
        parser.importData(vfFileName, textFile_DBHandler.Handler(vfDataPath, ","))
        pass

class TestGlobalFunctions(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testgetTabs(self):
        pass

    def testremoveFileExt(self):
        pass

if __name__ == '__main__':
    unittest.main()
