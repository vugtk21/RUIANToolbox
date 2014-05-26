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
import os, codecs, string
import sharedTools, DBHandlers, configRUIAN, configReader, importRUIAN

DATAFILEEXTENSION = ".csv"

class Handler(DBHandlers.DatabaseHandler):
    """ Implementace souborové databáze. Databáze je celá uložena v jednom
    adresáři, definovaném při inicializaci parametrem databasePath. Každá tabulka
    je uložena v jednom souboru s příponou DATAFILEEXTENSION.
    """
    def __init__(self, databasePath, fieldSeparator = ","):
        ''' Nastavuje proměnnou databasePath a inicializuje seznam otevřených
        souborů'''
        self.databasePath = sharedTools.pathWithLastSlash(databasePath)
        self.openedFiles = {}
        self.fieldSeparator = fieldSeparator
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
            del self.openedFiles[tableName]

        return True

    def databaseExists(self):
        return self.tableExists(configRUIAN.CONTROLDB_TABLENAME)

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
        if isinstance(tableName, unicode):
            tableName = tableName.encode('ascii','ignore')
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
            self.openedFiles[tableName] = codecs.open(self.tableNameToFileName(tableName), fileMode, "utf-8")
            fields = configReader.getTableFields(tableName)
            if fields != None:
                f = self.openedFiles[tableName]
                f.write(self.fieldSeparator.join(fields) + "\n")
                f.flush()

        return True

    def writeRowToTable(self, tableName, columnValues):
        ''' Zapíše nový řádek do databáze s hodnotami uloženými v dictionary columnValues '''
        self.createTable(tableName, False)
        f = self.openedFiles[tableName]

        if tableName == 'Parcely':
            if columnValues['Id'] == '141':
                pass    # ********************* oriznuta, blbe parsovana hodnota  ***********************

            if len(string.split(columnValues['PlatiOd'],'T')[0]) < 10:
                pass    # ********************* oriznuta, blbe parsovana hodnota  ***********************
            pass

        fields = configReader.getTableFields(tableName)
        if fields != None:
            values = []
            for key in fields:
                if columnValues.has_key(key):
                    value = columnValues[key]
                else:
                    value = ""

                #if isinstance(value, unicode):
                #    value = value.encode('ascii','ignore')

                values.append(value)

            f.write(self.fieldSeparator.join(values) + "\n")
        #f.write(",".join(columnValues.values()) + "\n")
        #f.write(str(columnValues) + "\n")

        return True

    def closeDatabase(self):
        """
        Tato metoda zavírá databázi, pokud je to potřeba.

        @return: True jestliže se tabulky podařilo zavřít.
        """
        importRUIAN.displayMessage("Zavírám tabulky databáze...")
        for tableName in configRUIAN.tableDef:
            importRUIAN.displayMessage(tableName, 1)
            self.closeTable(tableName)
        importRUIAN.displayMessage("Hotovo")
        return True

import unittest

class TestHandler(DBHandlers.TestHandler):
    def setUp(self):
        DBHandlers.TestHandler.setUp(self)
        self.h = Handler("")

if __name__ == '__main__':
    unittest.main()