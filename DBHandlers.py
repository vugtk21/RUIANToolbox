# -*- coding: cp1250 -*-
#-------------------------------------------------------------------------------
# Name:        DBTools
# Purpose:     Definuje abstraktní třídu pro ovládání databáze
#              a testovací balíček k ní
#
# Author:      Augustyn
#
# Created:     03.05.2013
# Copyright:   (c) Augustyn 2013
# Licence:     <your licence>
#-------------------------------------------------------------------------------
class DatabaseHandler:
    """ Abstraktní definice databáze.
    """

    def deleteTable(self, tableName):
        ''' Uvolňuje tabulku tableName, vrací True pokud se podařilo  '''
        return False

    def tableExists(self, tableName):
        ''' Vrací True, jestliže tabulka tableName v databázi existuje. '''
        return False

    def createTable(self, tableName, overwriteIfExists = False):
        ''' Vytvoří tabulku tableName, pokud ještě neexistuje, se sloupci podle definice v
        configRUIAN.tableDef.'''
        return False

    def writeRowToTable(self, tableName, columnValues):
        ''' Zapíše nový řádek do databáze s hodnotami uloženými v dictionary columnValues '''
        return False

    def closeTable(self, tableName):
        ''' Uzavírá tabulku tableName '''
        return False


import unittest
import configRUIAN

class TestHandler(unittest.TestCase):
    """ Abstraktní definice testování databáze.
    """
    testTableName = "testTable"

    def setUp(self):
        self.h = None
        configRUIAN.tableDef[TestHandler.testTableName] = {
            "skipNamespacePrefix" : "true", # remove namespace prefix obi, oki etc
            "field":{
                "Kod":                   {"type":"Integer", "notNull" : "yes", "pkey" : "yes"},
                "Nazev":                 {"type":"String"},
                "StatusKod":             {"type":"Integer"},
                "PlatiOd":               {"type":"DateTime"},
                "PlatiDo":               {"type":"DateTime"},
                "IdTransakce":           {"type":"Long"},
                "GlobalniIdNavrhuZmeny": {"type":"Long"},
                "VlajkaText":            {"type":"String"},
                "ZnakText":              {"type":"String"},
                "DefinicniBod":          {"type":"MultiPointPropertyType",   "xmlSubPath" : "Geometrie/DefinicniBod"},
                "OriginalniHranice":     {"type":"MultiSurfacePropertyType", "xmlSubPath" : "Geometrie/OriginalniHranice"}
            }
        }

        pass

    def tearDown(self):
        self.h = None
        pass

    def testHandlerAssigned(self):
        self.assertIsNotNone(self.h, "Database handler not assigned")

    def testcreateTable(self):
        self.assertEqual(self.h.createTable(TestHandler.testTableName, True), True, "Vytvoření testovací tabulky")
        self.assertEqual(self.h.tableExists(TestHandler.testTableName), True, "Ověření jestli vytvořená tabulka existuje")
        pass

    def testdeleteTable(self):
        self.h.createTable(TestHandler.testTableName)
        self.assertEqual(self.h.deleteTable(TestHandler.testTableName), True, "Vytvoříme tabulku a následně ji smažeme")

        self.assertEqual(self.h.deleteTable("NonExistingTable"), False, "Snaha o smazání neexistující tabulky -> vrací False")
        pass

    def testtableNameToFileName(self):
        pass

    def testtableExists(self):
        if self.h.createTable(TestHandler.testTableName, True):
            self.assertEqual(self.h.tableExists(TestHandler.testTableName), True, "Ověření jestli vytvořená tabulka existuje")
            self.h.deleteTable(TestHandler.testTableName)
            self.assertEqual(self.h.tableExists(TestHandler.testTableName), False, "Tabulku jsme právě vymazali, takže neexistuje")
        pass

    def testwriteRowToTable(self):
        pass