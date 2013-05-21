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
import configRUIAN, configReader, configGUI

# import business logic
import parseRUIANFile, textFile_DBHandler

databaseHandler = None

##def postGISParams():
##    result = ""
##    for key in configGUI.configData['postGIS_DBHandler']:
##        if key <> 'schemaName':
##            if result <> "":
##                result = result + ' '
##            result = result + key + "=" + configGUI.configData['postGIS_DBHandler'][key]
##    return result
##
##def databaseTypeChanged():
##    global databaseExists
##    databaseType = configGUI.configData['selectedDatabaseType']
##    if databaseType == "postGIS_DBHandler":
##        databaseHandler = textFile_DBHandler.Handler(configGUI.configData['textFile_DBHandler']['dataDirectory'])
##    elif databaseType == "postGIS_DBHandler":
##        databaseHandler = postGIS_DBHandler.Handler(postGISParams(), configGUI.configData['postGIS_DBHandler']['schemaName'])
##    else:
##        databaseHandler = None
##    pass

def createDatabaseHandler():
        global databaseHandler

        dbType = configGUI.configData['selectedDatabaseType']
        if dbType == 'textFile_DBHandler':
            databaseHandler = textFile_DBHandler.Handler(configGUI.configData['textFile_DBHandler']['dataDirectory'], ",")
        elif dbType == 'postGIS_DBHandler':
            databaseHandler = None
        else:
            databaseHandler = None

def dummyMessageProc(message, tabLevel = 0):
    tabStr = ""
    for i in range(0, tabLevel):
        tabStr = tabStr + "    "
    print tabStr + message
    pass

def createDatabaseProc(overwriteIfExists = False):
    createDatabaseHandler()
    displayMessage("Vytvářím tabulky databáze...")
    for tableName in configRUIAN.tableDef:
        fields = configReader.getTableFields(tableName)
        displayMessage(tableName + "\t:" + str(fields), 1)
        if databaseHandler:
            databaseHandler.createTable(tableName, overwriteIfExists)
            databaseHandler.closeTable(tableName)
    displayMessage("Hotovo")
    pass

def pathWithLastSlash(path):
    sepIdx = path.rfind(os.sep)
    if sepIdx == len(path) - 1:
        return path
    else:
        return path + os.sep

def importDatabaseProc():
    dataPath = pathWithLastSlash(configGUI.configData['importParameters']['dataRUIANDir'])

    displayMessage("Importuji databázi z adresáře " + dataPath)

    parser = parseRUIANFile.RUIANParser()

    dirItems = os.listdir(dataPath)
    extMask = configGUI.configData['importParameters']['suffix'].split(os.extsep)[1]
    for dirItem in dirItems:
        itemExtension = dirItem.split(os.extsep)[1]
        if itemExtension == extMask:
            displayMessage("Importuji soubor " + dirItem, 1)
            if databaseHandler:
                parser.importData(dataPath + dirItem, databaseHandler)

    displayMessage("Done")

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
tomu, že jste pøesmìroval standardní výstup do textového pole, teda aspoò myslím,
tak by nemìlo být potøeba na to sahat.

        # create connections
        XStream.stdout().messageWritten.connect( self._console.insertPlainText )
        XStream.stderr().messageWritten.connect( self._console.insertPlainText )

"""
displayMessage = dummyMessageProc

""" Procedura, kterou využijeme pro testování, jestli ze stránky vyplnìní
parametrù databáze pøejít na vytváøení databáze nebo pøímo na import.
"""
databaseExists = onDatabaseExistsProc

"""
Tuto proceduru spustíme, když pøejdeme na stránku vytváøení databáze (databaseExists = false)
"""
createDatabase = createDatabaseProc

"""
Tuto proceduru spustíme, když pøejdeme na stránku import
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
        createDatabase()
        pass


    def testimportDatabaseProc(self):
        importDatabaseProc()
        pass

if __name__ == '__main__':
    unittest.main()