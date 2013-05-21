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
import os, xml.parsers.expat, gzip
import configRUIAN, DBHandlers, textFile_DBHandler, postGIS_DBHandler

# @TODO Dořešit duplicitní vnořené názvy coi:Kod vs obi:Kod
# @TODO Jak vyřešit UTF-8

removeTables = True

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
        self.buildXMLSubPaths()
        pass

    def buildXMLSubPaths(self):
        ''' Vytvoří vlastnost xmlSubPath pro každou definici položky v každé tabulce.
        Zároveň vytvoří pole se seznamem xmlSubPath-s pro každou tabulku.
        '''
        for tableDef in configRUIAN.tableDef.values():
            xmlSubPaths = []
            fieldDefs = tableDef[configRUIAN.FIELDS_KEY_NAME]
            for fieldName in fieldDefs:
                fieldDef = fieldDefs[fieldName]
                if not fieldDef.has_key(configRUIAN.XMLSUBPATH_KEYNAME):
                    fieldDef[configRUIAN.XMLSUBPATH_KEYNAME] = fieldName
                xmlSubPaths.append(fieldDef[configRUIAN.XMLSUBPATH_KEYNAME])
            tableDef[configRUIAN.XMLSUBPATH_KEYNAME] = xmlSubPaths
        pass

    def newRecord(self):
        self.recordValues = {}
        self.columnName = ""
        pass

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

        def start_element(name, attrs):
            """ Start element Handler. """
            self.elemCount = self.elemCount + 1
            self.elemLevel = self.elemLevel + 1
            name = name.replace("vf:", "")  # remove the namespace prefix

            # Jestliže jsme na úrovni datových tabulek, založíme ji
            if self.elemPathStr == "VymennyFormat\\Data":
                self.insideImportedTable = configRUIAN.tableDef.has_key(name)
                self.tableName = name
                self.insideTable = True
                if self.insideImportedTable:
                    dbHandler.createTable(self.tableName, removeTables)
                    config = configRUIAN.tableDef[name]
                    self.recordTagName = ""

                    # Najdeme sloupce k importu
                    if config.has_key(configRUIAN.FIELDS_KEY_NAME):
                         fieldDefs = config[configRUIAN.FIELDS_KEY_NAME]
                         self.allowedColumns = fieldDefs.keys()
                    else:
                        self.allowedColumns = None
                    print self.tableName, ":", self.allowedColumns
                else:
                    print name, "properties are not configured."

            elif self.insideImportedTable: # jsme uvnitř tabulky
                if self.recordTagName == "": # new table record
                    self.recordTagName = name
                    self.newRecord()
                elif (self.allowedColumns != None):
                    # Remove namespace prefix, if needed
                    if configRUIAN.SKIPNAMESPACEPREFIX:
                        doubleDotPos = name.find(":")
                        if doubleDotPos >= 0:
                            name = name[doubleDotPos + 1:]

                    if name in self.allowedColumns and self.elemLevel == 5: # start of allowed column
                        self.columnName = name
                    else:
                        self.columnName = ""
            else:
                # Skipped tags
                pass

            self.elemPath.append(name)
            self.elemPathStr = "\\".join(self.elemPath)

        def end_element(name):
            """ End element Handler """
            name = name.replace("vf:", "")          # remove namespace prefix

            # close table
            if self.insideImportedTable and self.tableName == name and self.elemLevel == 3:
                self.insideImportedTable = False
                self.tableName = None
                self.allowedColumns = None

            # close record
            elif self.recordTagName == name:
                self.recordTagName = ""
                if self.insideImportedTable:
                    if self.tableName == 'Parcely' and self.recordValues['Id'] == '141':
                        pass    # ********************* poriznuta, blbe parsovana hodnota  ***********************
                    dbHandler.writeRowToTable(self.tableName, self.recordValues)
                    self.recordValues = {}

            self.elemPath.remove(self.elemPath[len(self.elemPath) - 1])
            self.elemPathStr = "\\".join(self.elemPath)
            self.elemLevel = self.elemLevel - 1
            pass

        def char_data(data):
            if self.columnName <> "":
                if self.recordValues.has_key(self.columnName):
                    self.recordValues[self.columnName] = self.recordValues[self.columnName] + data
                else:
                    self.recordValues[self.columnName] = data

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
