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
import os, string
import DBHandlers, configRUIAN, configReader

fieldPostGISGeom = {
 "MultiPointPropertyType"  : "point",
 "MultiCurvePropertyType"  : "line",
 "MultiSurfacePropertyType" : "poly"
}

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

def ruianToPostGISMultipoint(elementXML):
    if string.find(elementXML,'pointMembers'):
        result = string.replace(elementXML,'pointMembers','pointMember')

    return result
    pass


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

def ruianPostGISTablesStructure(schemaName, tableName):
    tableCreateSQL = "CREATE TABLE " + schemaName + '.' + ruianToPostGISColumnName(tableName, configRUIAN.SKIPNAMESPACEPREFIX) + "("
    for item in configRUIAN.tableDef[tableName]:
            if item == 'fields':
                numFields = 1
                pKey = ''
                for fieldName in configRUIAN.tableDef[tableName][item]:
                    if numFields < len(configRUIAN.tableDef[tableName][item]):
                        separator = ','
                    else:
                        separator = ''
                    numFields = numFields + 1
                    fieldDef = ruianToPostGISColumnName(
                       fieldName, configRUIAN.SKIPNAMESPACEPREFIX) + ' ' + \
                       ruianToPostGISDBTypes[configRUIAN.tableDef[tableName][item][fieldName]['type']]
                    if fieldPostGISGeom.has_key(configRUIAN.tableDef[tableName][item][fieldName]['type']):
                        fieldDef = fieldDef + ', ' + ruianToPostGISColumnName(fieldName, configRUIAN.SKIPNAMESPACEPREFIX) + '_' + fieldPostGISGeom[configRUIAN.tableDef[tableName][item][fieldName]['type']] + ' geometry'

                    if configRUIAN.tableDef[tableName][item][fieldName].has_key('notNull'):
                        if configRUIAN.tableDef[tableName][item][fieldName]['notNull'] == 'yes':
                            fieldDef = fieldDef + ' NOT NULL'
                        if configRUIAN.tableDef[tableName][item][fieldName]['pkey'] == 'yes':
                            pKey = ',CONSTRAINT ' + \
                                   ruianToPostGISColumnName(
                                     (tableName + '_' +   fieldName),
                                     configRUIAN.SKIPNAMESPACEPREFIX) + \
                                     '_pk PRIMARY KEY (' + \
                                     ruianToPostGISColumnName(fieldName,configRUIAN.SKIPNAMESPACEPREFIX) + ')'
                    fieldDef = fieldDef + separator
                    tableCreateSQL = tableCreateSQL + fieldDef
                tableCreateSQL = tableCreateSQL + pKey + ") WITH (OIDS=FALSE);"
    return tableCreateSQL

class Handler:
    """ Implementace souborové databáze. Databáze je celá uložena v jednom
    adresáři, definovaném při inicializaci parametrem databasePath. Každá tabulka
    je uložena v jednom souboru s příponou DATAFILEEXTENSION.
    """
    def __init__(self, connectionParams, schemaName):
        ''' Nastavuje proměnnou databasePath a inicializuje seznam otevřených
        souborů'''
        self.schemaName = schemaName
        self.connection = psycopg2.connect(connectionParams)
        self.cursor = self.connection.cursor()

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
        self._disconnect

    def closeTable(self, tableName):
        ''' Uzavírá tabulku tableName '''

        return True

    def deleteTable(self, tableName):
        ''' Uvolňuje tabulku tableName, vrací True pokud se podařilo  '''
        if self.tableExists(tableName):
            SQL = ("DROP TABLE %s CASCADE;") %(ruianToPostGISColumnName(tableName, configRUIAN.SKIPNAMESPACEPREFIX))
            self.cursor.execute(SQL)
            self.connection.commit()
            return True
        else:
            return False

    def tableExists(self, tableName):
        ''' Vrací True, jestliže tabulka tableName v databázi existuje. '''
        SQL= ("select * from pg_tables where (schemaname = '%s' and tablename = '%s');") % (self.schemaName,ruianToPostGISColumnName(tableName, configRUIAN.SKIPNAMESPACEPREFIX))
        self.cursor.execute(SQL)
        return self.cursor.rowcount > 0

    def createIndexes(self, tableName):
        ''' Vytvori index'''
        SQL = '''
            SELECT
            a.attname::text AS f_geometry_column
            FROM pg_class c, pg_attribute a, pg_type t, pg_namespace n
            WHERE
            t.typname = 'geometry'::name AND a.attisdropped = false AND a.atttypid = t.oid
            AND a.attrelid = c.oid AND c.relnamespace = n.oid
            AND (c.relkind = 'r'::"char" OR c.relkind = 'v'::"char")
            AND NOT pg_is_other_temp_schema(c.relnamespace)
            AND NOT (n.nspname = 'public'::name AND c.relname = 'raster_columns'::name)
            AND has_table_privilege(c.oid, 'SELECT'::text)
            '''
        SQL = SQL + "AND n.nspname = '%s' AND c.relname = '%s';" % (self.schemaName,ruianToPostGISColumnName(tableName, configRUIAN.SKIPNAMESPACEPREFIX))

        self.cursor.execute(SQL)
        geomFields = self.cursor.fetchall()
        for geomField in geomFields:
            SQL = 'CREATE INDEX %s_%s_gidx ON %s USING gist(%s)'%(ruianToPostGISColumnName(tableName, configRUIAN.SKIPNAMESPACEPREFIX),geomField[0],ruianToPostGISColumnName(tableName, configRUIAN.SKIPNAMESPACEPREFIX),geomField[0])
            self.cursor.execute(SQL)
            self.connection.commit()

        return True

    def createTable(self, tableName, overwriteIfExists = False):
        ''' Vytvoří tabulku tableName, pokud ještě neexistuje, se sloupci podle definice v
        configRUIAN.tableDef.'''
        if overwriteIfExists and self.tableExists(tableName):
            self.deleteTable(ruianToPostGISColumnName(tableName, configRUIAN.SKIPNAMESPACEPREFIX))

        if not self.tableExists(tableName):
            SQL = ruianPostGISTablesStructure(self.schemaName, tableName)
            self.cursor.execute(SQL)
            self.connection.commit()

        return True

    def writeRowToTable(self, tableName, columnValues):
        ''' Zapíše nový řádek do databáze s hodnotami uloženými v dictionary columnValues '''
        self.createTable(tableName,False)
        comma = ''
        fieldsList = ''
        valuesList = ''
        for field in columnValues:
            # sestaveni seznamu atr. poli
            fieldsList = fieldsList + comma + ruianToPostGISColumnName(field,configRUIAN.SKIPNAMESPACEPREFIX)

            # sestaveni seznamu HODNOT atr. poli
            valuesList = valuesList + comma + "'" + columnValues[field] + "'"

            # uprava GML tak aby fungovaly funkce PGIS
            if field == 'DefinicniBod':
                columnValues[field] = ruianToPostGISMultipoint(columnValues[field])

            comma = ','

            # doplneni PostGIS geometrie
            if fieldPostGISGeom.has_key(configRUIAN.tableDef[tableName]['fields'][field]['type']):
                fieldsList = fieldsList + comma + ruianToPostGISColumnName(field, configRUIAN.SKIPNAMESPACEPREFIX) + '_' + fieldPostGISGeom[configRUIAN.tableDef[tableName]['fields'][field]['type']]
                valuesList = valuesList + comma + "st_geomfromgml('" + columnValues[field] + "')"

        SQL = "INSERT INTO " + ruianToPostGISColumnName(tableName,True) + "(" + fieldsList + ") VALUES (" + valuesList +  ");"
        self.cursor.execute(SQL)
        self.connection.commit()

        return True

import unittest

class TestHandler(DBHandlers.TestHandler):
    def setUp(self):
        DBHandlers.TestHandler.setUp(self)
        self.h = Handler("dbname=euradin host=localhost port=5432 user=postgres password=postgres","public")

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