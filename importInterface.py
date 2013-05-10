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
import configRUIAN, configReader

def dummyMessageProc(message, tabLevel = 0):
    tabStr = ""
    for i in range(0, tabLevel):
        tabStr = tabStr + "    "
    print tabStr + message
    pass

def dummyCreateDatabaseProc():
    displayMessage("Creating database")
    for tableName in configRUIAN.tableDef:
        displayMessage("Creating table " + tableName, 1)
        fields = configReader.getTableFields(tableName)
        displayMessage("fields:" + str(fields), 2)
    displayMessage("Done")
    pass

def onImportDatabaseProc():
    displayMessage("Importing database")
    displayMessage("Importing file file1.xml", 1)
    displayMessage("Importing file file2.xml", 1)
    displayMessage("Done")
    pass

def onDatabaseExistsProc():
    return False

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
createDatabase = dummyCreateDatabaseProc

"""
Tuto proceduru spustíme, když pøejdeme na stránku import
"""
importDatabase = onImportDatabaseProc

def main():
    createDatabase()
    importDatabase()
    pass

if __name__ == '__main__':
    main()
