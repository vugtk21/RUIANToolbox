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
import psycopg2
import os
import DBHandlers, configRUIAN, configReader

# RUIAN to PostGIS SQL conversion table
ruianToPostGISDBTypes = {
 "String"    : "text",
 "Integer"   : "integer",
 "DateTime"  : "date",
 "Long"      : "bigint",
 "Boolean"      : "boolean",
 "MultiPointPropertyType"  : "text",
 "MultiCurvePropertyType"  : "text",
 "MultiSurfacePropertyType" : "text"
}

def ruianToPostGISColumnName(XMLTagName, removeNamespace):
    """ if removeNamespace is set to true, than removes namespace prefix from XMLTagName
    additionally, it converts CamelCase RUIAN name to underscore notation
    obi:Kod -> Kod -> kod
    obi:GlobalniIdNavrhuZmeny -> GlobalniIdNavrhuZmeny -> globalni_id_navrhu_zmeny
    """
    # if no modifications, return XML tag name
    result = XMLTagName

    # if remove namespaces, than do it
    if removeNamespace:
        doubleDotPos = result.find(":")
        if doubleDotPos >= 0:
            result = result[doubleDotPos + 1:]

    # switch CamelCase to underscore notation
    if result != "":
        stack = ""
        firstAfterNameSpace = False
        for i in range(0, len(result)):
            ch = result[i:i + 1]
            if ch != ch.lower():
                ch = ch.lower()
                if i != 0 and not firstAfterNameSpace:
                    ch = "_" + ch.lower()
            firstAfterNameSpace = ch == ":"
            stack = stack + ch
        result = stack

    return result

def getRuianPostGISTableStructure():
    """ """
    result = {}
    for tableName in configRUIAN.tableDef:
        tableCreateSQL = "CREATE TABLE " + ruianToPostGISColumnName(tableName, configRUIAN.SKIPNAMESPACEPREFIX) + "("
        for item in tableDef[tableName]:
            if item == 'fields':
                numFields = 1
                pKey = ''
                for fieldName in tableDef[tableName][item]:
                    if numFields < len(tableDef[tableName][item]):
                        separator = ','
                    else:
                        separator = ''
                    numFields = numFields + 1
                    fieldDef = ruianToPostGISColumnName(
                       fieldName, configRUIAN.SKIPNAMESPACEPREFIX) + ' ' + \
                       ruianToPostGISDBTypes[tableDef[tableName][item][fieldName]['type']]
                    if tableDef[tableName][item][fieldName].has_key('notNull'):
                        if tableDef[tableName][item][fieldName]['notNull'] == 'yes':
                            fieldDef = fieldDef + ' NOT NULL'
                        if tableDef[tableName][item][fieldName]['pkey'] == 'yes':
                            pKey = ',CONSTRAINT ' + \
                                   ruianToPostGISColumnName(
                                     (tableName + '_' +   fieldName),
                                     configRUIAN.SKIPNAMESPACEPREFIX) + \
                                     '_pk PRIMARY KEY (' + \
                                     ruianToPostGISColumnName(fieldName,configRUIAN.SKIPNAMESPACEPREFIX) + ')'
                    fieldDef = fieldDef + separator
                    tableCreateSQL = tableCreateSQL + fieldDef
                tableCreateSQL = tableCreateSQL + pKey + ") WITH (OIDS=FALSE);"
                result[tableName] = tableCreateSQL
    return result

class Handler:
    """ Implementace souborové databáze. Databáze je celá uložena v jednom
    adresáři, definovaném při inicializaci parametrem databasePath. Každá tabulka
    je uložena v jednom souboru s příponou DATAFILEEXTENSION.
    """
    def __init__(self, connectionParams, schemaName):
        ''' Nastavuje proměnnou databasePath a inicializuje seznam otevřených
        souborů'''
        self.connection = psycopg2.connect(connectionParams)
        self.cursor = connection.cursor()
        self.cursor = cursor
        self.schemaName = schemaName

        pass

    def _disconnect():
        ''' Odpojí se od databáze. '''
        if self.cursor != None:
            self.cursor.close()
            self.cursor = None

        if self.connection != None:
            self.connection.close()
            self.connection = None

        pass

    def __del__(self):
        ''' Destruktor, volá odpojení od databáze. '''
        _disconnect()

    def closeTable(self, tableName):
        ''' Uzavírá tabulku tableName '''

        return True

    def deleteTable(self, tableName):
        ''' Uvolňuje tabulku tableName, vrací True pokud se podařilo  '''
        if self.tableExists(tableName):
            SQL = ("DROP TABLE %s;") %(tableName)
            cursor.execute(SQL)
            return True # ??? Nevraci nahodou cursor.execute chybu???
        else:
            return False

    def tableExists(self, tableName):
        ''' Vrací True, jestliže tabulka tableName v databázi existuje. '''
        SQL= ("select * from pg_tables where (schemaname = '%s' and tablename = '%s');") % (self.schemaName,tableName)
        self.cursor.execute(SQL)
        return self.cursor.rowcount > 0

    def createTable(self, tableName, overwriteIfExists = False):
        ''' Vytvoří tabulku tableName, pokud ještě neexistuje, se sloupci podle definice v
        configRUIAN.tableDef.'''
        if overwriteIfExists and self.tableExists(tableName):
            deleteTable(tableName)

        if not self.tableExists(tableName):
            cursor.execute(getTablesSQDef(self.schemaName, tableName, ruianPostGISTablesStructure[tableName]))

        return True

    def writeRowToTable(self, tableName, columnValues):
        ''' Zapíše nový řádek do databáze s hodnotami uloženými v dictionary columnValues '''

        return False

import unittest

class TestHandler(DBHandlers.TestHandler):
    def setUp(self):
        DBHandlers.TestHandler.setUp(self)
        self.h = Handler("", "")

class TestGlobalFunctions(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testruianToPostGISColumnName(self):
        self.assertEqual(ruianToPostGISColumnName("obi:Kod", True), "kod", "Error removing namespace")
        self.assertEqual(ruianToPostGISColumnName("obi:Kod", False), "obi:kod", "Error removing namespace")
        self.assertEqual(ruianToPostGISColumnName("obi:GlobalniIdNavrhuZmeny", True), "globalni_id_navrhu_zmeny", "Error replacing CamelCase by underscores")
        pass

if __name__ == '__main__':
    unittest.main()