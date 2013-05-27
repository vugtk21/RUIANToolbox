# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        importInterface
# Purpose:
#
# Author:      Radecek
#
# Created:     06/05/2013
# Copyright:   (c) Radecek 2013
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import os
import sharedTools, configRUIAN, configReader, configGUI

# import business logic
import parseRUIANFile, textFile_DBHandler

databaseHandler = None

def createDatabaseHandler():
        global databaseHandler

        dbType = configGUI.configData['selectedDatabaseType']
        if dbType == 'textFile_DBHandler':
            databaseHandler = textFile_DBHandler.Handler(configGUI.configData['textFile_DBHandler']['dataDirectory'], ",")
        elif dbType == 'postGIS_DBHandler':
            import postGIS_DBHandler

            databaseHandler = postGIS_DBHandler.Handler(postGIS_DBHandler.params.connectionParams, postGIS_DBHandler.params.schemaName)
        else:
            databaseHandler = None

def dummyMessageProc(message, tabLevel = 0):
    tabStr = ""
    for i in range(0, tabLevel):
        tabStr = tabStr + "    "
    print tabStr + message
    pass

def closeAllKnownTables():
    if databaseHandler:
        displayMessage("Zavírám tabulky databáze...")
        for tableName in configRUIAN.tableDef:
            displayMessage(tableName, 1)
            databaseHandler.closeTable(tableName)
        displayMessage("Hotovo")
    pass

def createDatabaseProc(overwriteIfExists = False):
    createDatabaseHandler()
    displayMessage("Vytvářím tabulky databáze...")
    for tableName in configRUIAN.tableDef:
        if sharedTools.isImportedTable(tableName):
            fields = configReader.getTableFields(tableName)
            displayMessage(tableName + "\t:" + str(fields), 1)
            if databaseHandler:
                databaseHandler.createTable(tableName, overwriteIfExists)
                databaseHandler.closeTable(tableName)
        else:
            if databaseHandler:
                databaseHandler.deleteTable(tableName)

    displayMessage("Hotovo")
    pass

def importDatabaseProc():
    dataPath = sharedTools.pathWithLastSlash(configGUI.configData['importParameters']['dataRUIANDir'])

    displayMessage("Importuji databázi z adresáře " + dataPath)

    parseRUIANFile.removeTables = True
    parser = parseRUIANFile.RUIANParser()

    dirItems = os.listdir(dataPath)
    extMask = sharedTools.getFileExtension(configGUI.configData['importParameters']['suffix'])
    for dirItem in dirItems:
        itemExtension = sharedTools.getFileExtension(dirItem)
        if itemExtension == extMask:
            displayMessage("Importuji soubor " + dirItem, 1)
            if databaseHandler:
                parser.importData(dataPath + dirItem, databaseHandler)
                parseRUIANFile.removeTables = False

    displayMessage("Done")
    closeAllKnownTables()

    pass

def onDatabaseExistsProc():
    if databaseHandler == None:
        return False
    else:
        #databaseHandler.c
        # @TODO
        pass

"""
Tato procedura by mìla vypisovat do konzole obsah parametru message. Vzhledem k
tomu, že jste přesmìroval standardní výstup do textového pole, teda aspoò myslím,
tak by nemìlo být potřeba na to sahat.

        # create connections
        XStream.stdout().messageWritten.connect( self._console.insertPlainText )
        XStream.stderr().messageWritten.connect( self._console.insertPlainText )

"""
displayMessage = dummyMessageProc

""" Procedura, kterou využijeme pro testování, jestli ze stránky vyplnìní
parametrù databáze přejít na vytváření databáze nebo přímo na import.
"""
databaseExists = onDatabaseExistsProc

"""
Tuto proceduru spustíme, když přejdeme na stránku vytváření databáze (databaseExists = false)
"""
createDatabase = createDatabaseProc

"""
Tuto proceduru spustíme, když přejdeme na stránku import
"""
importDatabase = importDatabaseProc

import unittest

class TestGlobalFunctions(unittest.TestCase):

    def setUp(self):
        createDatabaseHandler()
        pass

    def tearDown(self):
        pass

    def testcreateDatabaseProc(self):
        createDatabase(True)
        pass


    def testimportDatabaseProc(self):
        importDatabaseProc()
        pass

if __name__ == '__main__':
    unittest.main()