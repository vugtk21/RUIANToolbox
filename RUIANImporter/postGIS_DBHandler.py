# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        postGIS_DBHandler
# Purpose:     Implementuje ovladač pro souborovou databázi.
#
# Author:      Radek Augustýn
#
# Created:     03.05.2013
# Copyright:   (c) Radek Augustýn 2013
# Licence:     <your licence>
#-------------------------------------------------------------------------------
"""
@DONE 26.05.2013    Normalizace názvů tabulek na lowercase (tableName = _normalizeTableName(tableName))
"""
import psycopg2
import os, string
import DBHandlers, configRUIAN, configReader, configGUI

fieldPostGISGeom = {
 "MultiPointPropertyType"  : "point",
 "MultiCurvePropertyType"  : "line",
 "MultiSurfacePropertyType" : "poly"
}

constrainPostGISGeom = {
 "MultiPointPropertyType"  : ["POINT","MULTIPOINT"],
 "MultiCurvePropertyType"  : ["LINESTRING","MULTILINESTRING"],
 "MultiSurfacePropertyType" : ["POLYGON","MULTIPOLYGON"]
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

POSTGIS_DBHANDLER_CONFIGKEY = 'postGIS_DBHandler'
DATABASENAME_KEY = 'dbname'
HOST_KEY         = 'host'
PORT_KEY         = 'port'
USER_KEY         = 'user'
PASWORD_KEY      = 'password'
SCHEMANAME_KEY      = 'schemaName'

class storedParams:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(storedParams, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    # Getters and setters
    def getDatabaseName(self):
        return configGUI.configData[POSTGIS_DBHANDLER_CONFIGKEY][DATABASENAME_KEY]

    def setDatabaseName(self, value):
        configGUI.configData[POSTGIS_DBHANDLER_CONFIGKEY][DATABASENAME_KEY] = value

    def getHost(self):
        return configGUI.configData[POSTGIS_DBHANDLER_CONFIGKEY][HOST_KEY]

    def setHost(self, value):
        configGUI.configData[POSTGIS_DBHANDLER_CONFIGKEY][HOST_KEY] = value

    def getPort(self):
        return configGUI.configData[POSTGIS_DBHANDLER_CONFIGKEY][PORT_KEY]

    def setPort(self, value):
        configGUI.configData[POSTGIS_DBHANDLER_CONFIGKEY][PORT_KEY] = value

    def getUser(self):
        return configGUI.configData[POSTGIS_DBHANDLER_CONFIGKEY][USER_KEY]

    def setUser(self, value):
        configGUI.configData[POSTGIS_DBHANDLER_CONFIGKEY][USER_KEY] = value

    def getPassword(self):
        return configGUI.configData[POSTGIS_DBHANDLER_CONFIGKEY][PASWORD_KEY]

    def setPassword(self, value):
        configGUI.configData[POSTGIS_DBHANDLER_CONFIGKEY][PASWORD_KEY] = value

    def getSchemaName(self):
        return configGUI.configData[POSTGIS_DBHANDLER_CONFIGKEY][SCHEMANAME_KEY]

    def setSchemaName(self, value):
        configGUI.configData[POSTGIS_DBHANDLER_CONFIGKEY][SCHEMANAME_KEY] = value

    def getConnectionParams(self):
        return 'dbname=' + self.databaseName + \
                 ' host=' + self.host + \
                 ' port=' + self.port + \
                 ' user=' + self.user + \
                 ' password=' + self.password

    # property definitions
    databaseName = property(getDatabaseName, setDatabaseName)
    host = property(getHost, setHost)
    port = property(getPort, setPort)
    user = property(getUser, setUser)
    password = property(getPassword, setPassword)
    schemaName = property(getSchemaName, setSchemaName)
    connectionParams = property(getConnectionParams)

params = storedParams()

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

def _normalizeTableName(tableName):
    return tableName.lower()

def ruianPostGISTablesStructure(schemaName, tableName):
    tableCreateSQL = "CREATE TABLE " + schemaName + '.' + ruianToPostGISColumnName(tableName, configRUIAN.SKIPNAMESPACEPREFIX) + "("
    for item in configRUIAN.tableDef[tableName]:
            if item == 'fields':
                numFields = 1
                pKey = ''
                fieldConstrainDef = ''
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
                        fieldConstrainDef = fieldConstrainDef + ",CONSTRAINT enforce_" + ruianToPostGISColumnName(tableName, configRUIAN.SKIPNAMESPACEPREFIX) + '_' + ruianToPostGISColumnName(fieldName, configRUIAN.SKIPNAMESPACEPREFIX) + '_' + fieldPostGISGeom[configRUIAN.tableDef[tableName][item][fieldName]['type']] + " CHECK (geometrytype(" +  ruianToPostGISColumnName(fieldName, configRUIAN.SKIPNAMESPACEPREFIX) + '_' + fieldPostGISGeom[configRUIAN.tableDef[tableName][item][fieldName]['type']] +  ") = '" + constrainPostGISGeom[configRUIAN.tableDef[tableName][item][fieldName]['type']][0] + "'::text OR geometrytype(" +  ruianToPostGISColumnName(fieldName, configRUIAN.SKIPNAMESPACEPREFIX) + '_' + fieldPostGISGeom[configRUIAN.tableDef[tableName][item][fieldName]['type']] +  ") = '" + constrainPostGISGeom[configRUIAN.tableDef[tableName][item][fieldName]['type']][1] + "'::text OR " + ruianToPostGISColumnName(fieldName, configRUIAN.SKIPNAMESPACEPREFIX) + '_' + fieldPostGISGeom[configRUIAN.tableDef[tableName][item][fieldName]['type']] + " IS NULL)"
                        pass

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
                tableCreateSQL = tableCreateSQL + pKey +  fieldConstrainDef + ") WITH (OIDS=FALSE);"
    return tableCreateSQL

class Handler(DBHandlers.DatabaseHandler):
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
        self.tableList = {}

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
        # Pro PostGIS není potřeba, pracuje na principu cursoru
        return True

    def deleteTable(self, tableName):
        ''' Uvolňuje tabulku tableName, vrací True pokud se podařilo  '''
        if self.tableExists(tableName):
            SQL = ("DROP TABLE %s CASCADE;") %(ruianToPostGISColumnName(tableName, configRUIAN.SKIPNAMESPACEPREFIX))
            del self.tableList[tableName]
            self.cursor.execute(SQL)
            self.connection.commit()
            return True
        else:
            return False

    def tableExists(self, tableName):
        ''' Vrací True, jestliže tabulka tableName v databázi existuje. '''
        if not tableName in self.tableList:
            SQL= ("select * from pg_tables where (schemaname = '%s' and tablename = '%s');") % (self.schemaName,ruianToPostGISColumnName(tableName, configRUIAN.SKIPNAMESPACEPREFIX))
            self.cursor.execute(SQL)
            self.tableList[tableName] = self.cursor.rowcount > 0

        return self.tableList[tableName]

    def createGeomIndexes(self, tableName):
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
            self.deleteTable(tableName)

        if not self.tableExists(tableName):
            SQL = ruianPostGISTablesStructure(self.schemaName, tableName)
            self.cursor.execute(SQL)
            self.connection.commit()
            self.createGeomIndexes(tableName)
            self.tableList[tableName] = True

        return True

    def writeRowToTable(self, tableName, columnValues):
        self.createTable(tableName)
        ''' Zapíše nový řádek do databáze s hodnotami uloženými v dictionary columnValues '''
        if tableName == 'Parcely' and columnValues['Id'] == '141':
            pass    # ********************* poriznuta, blbe parsovana hodnota  ***********************

        comma = ''
        fieldsList = ''
        valuesList = ''
        for field in columnValues:
            # sestaveni seznamu atributů poli
            fieldsList = fieldsList + comma + ruianToPostGISColumnName(field, configRUIAN.SKIPNAMESPACEPREFIX)

            # sestaveni seznamu HODNOT atr. poli
##            if configRUIAN.tableDef[tableName]['fields'][field]['type'] == 'DateTime':   #ponecha pouze datum, vypusti cas
##                columnValues[field] = string.split(columnValues[field],'T')[0]
##                if len(columnValues[field]) < 10:
##                    columnValues[field] = '0001-01-01'                           #nahradi nesmyslnou hodnotou

            valuesList = valuesList + comma + "'" + columnValues[field].replace("'", "") + "'" # @TODO Zabezpečit, aby v řetězci mohly být apostrofy

            # uprava GML tak aby fungovaly funkce PostGIS
            if field == 'DefinicniBod':
                columnValues[field] = ruianToPostGISMultipoint(columnValues[field])
                pass

            comma = ','

            # doplneni PostGIS geometrie
            if fieldPostGISGeom.has_key(configRUIAN.tableDef[tableName]['fields'][field]['type']) and columnValues[field] <> '':
                fieldsList = fieldsList + comma + ruianToPostGISColumnName(field, configRUIAN.SKIPNAMESPACEPREFIX) + '_' + fieldPostGISGeom[configRUIAN.tableDef[tableName]['fields'][field]['type']]
                valuesList = valuesList + comma + "st_geomfromgml('" + columnValues[field] + "')"

        SQL = "INSERT INTO " + ruianToPostGISColumnName(tableName,True) + "(" + fieldsList + ") VALUES (" + valuesList +  ");"
        try:
            self.cursor.execute(SQL)
            self.connection.commit()
            return True
        except:
            self.connection.rollback()  # todo - v pripade vadne geometrie dojde k preskoceni zaznamu
            pass
            return False


import unittest

class TestHandler(DBHandlers.TestHandler):
    def setUp(self):
        DBHandlers.TestHandler.setUp(self)
        self.h = Handler("dbname=euradin host=localhost port=5432 user=postgres password=ahoj","public")

class TestGlobalFunctions(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testcreateIndexes(self):
        self.assertEqual(self.h.createIndexes(TestHandler.testTableName), True, "Vytvoření indexů")
        pass

    def testruianToPostGISColumnName(self):
        self.assertEqual(ruianToPostGISColumnName("obi:Kod", True), "kod", "Error removing namespace")
        self.assertEqual(ruianToPostGISColumnName("obi:Kod", False), "obi:kod", "Error removing namespace")
        self.assertEqual(ruianToPostGISColumnName("obi:GlobalniIdNavrhuZmeny", True), "globalni_id_navrhu_zmeny", "Error replacing CamelCase by underscores")
        pass

if __name__ == '__main__':
    unittest.main()