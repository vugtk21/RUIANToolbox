# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        textFile_DBHandler
# Purpose:     Implementuje ovladač pro souborovou databázi.
#
# Author:      Radek Augustýn
#
# Created:     03.05.2013
# Copyright:   (c) Radek Augustýn 2013
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import os
import DBHandlers
import configRUIAN, configReader

DATAFILEEXTENSION = ".txt"

class Handler:
    """ Implementace souborové databáze. Databáze je celá uložena v jednom
    adresáři, definovaném při inicializaci parametrem databasePath. Každá tabulka
    je uložena v jednom souboru s příponou DATAFILEEXTENSION.
    """
    def __init__(self, databasePath):
        ''' Nastavuje proměnnou databasePath a inicializuje seznam otevřených
        souborů'''
        self.databasePath = databasePath
        self.openedFiles = {}
        pass

    def __del__(self):
        ''' Uzavírá všechny otevřené soubory. '''
        for key in self.openedFiles:
            f = self.openedFiles[key]
            if f != None:
                f.close()
        self.openedFiles = {}

    def closeTable(self, tableName):
        ''' Uzavírá tabulku tableName '''
        if self.openedFiles.has_key(tableName):
            self.openedFiles[tableName].close()
            self.openedFiles[tableName] = None

        return True

    def deleteTable(self, tableName):
        ''' Uvolňuje tabulku tableName, vrací True pokud se podařilo  '''
        fileName = self.tableNameToFileName(tableName)
        self.closeTable(tableName)
        if os.path.exists(fileName):
            os.remove(fileName)
            return not os.path.exists(fileName)
        else:
            return False

    def tableNameToFileName(self, tableName):
        ''' '''
        return self.databasePath + tableName + DATAFILEEXTENSION

    def tableExists(self, tableName):
        ''' Vrací True, jestliže tabulka tableName v databázi existuje. '''
        return os.path.exists(self.tableNameToFileName(tableName))

    def createTable(self, tableName, overwriteIfExists = False):
        ''' Vytvoří tabulku tableName, pokud ještě neexistuje, se sloupci podle definice v
        configRUIAN.tableDef.'''
        if not self.openedFiles.has_key(tableName):
            if not overwriteIfExists and self.tableExists(tableName):
                fileMode = "a"
            else:
                fileMode = "w"
            self.openedFiles[tableName] = open(self.tableNameToFileName(tableName), fileMode)
        fields = configReader.getTableFields(tableName)
        if fields != None:
            self.openedFiles[tableName].write(str(fields))

        return True

    def writeRowToTable(self, tableName, columnValues):
        ''' Zapíše nový řádek do databáze s hodnotami uloženými v dictionary columnValues '''
        self.createTable(tablename, false)
        f = self.openedFiles[tableName]
        f.write(str(columnValues) + "\n")

        return True

import unittest

class TestHandler(DBHandlers.TestHandler):
    def setUp(self):
        DBHandlers.TestHandler.setUp(self)
        self.h = Handler("")

if __name__ == '__main__':
    unittest.main()
