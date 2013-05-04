# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        tableDef
# Purpose:
#
# Author:      ruzickao
#
# Created:     30.04.2013
# Copyright:   (c) ruzickao 2013
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import unittest
import configRUIAN, DBHandlers

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

# if removeNamespace is set to true, than removes namespace prefix from XMLTagName
# additionally, it converts CamelCase RUIAN name to underscore notation
# obi:Kod -> Kod -> kod
# obi:GlobalniIdNavrhuZmeny -> GlobalniIdNavrhuZmeny -> globalni_id_navrhu_zmeny
def ruianToPostGISColumnName(XMLTagName, removeNamespace):
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
    result = {}
    for tableName in tableDef:
        tableCreateSQL = "CREATE TABLE " + ruianToPostGISColumnName(tableName,tableDef[tableName]['skipNamespacePrefix']) + "("
        for item in tableDef[tableName]:
            if item == 'field':
                numFields = 1
                pKey = ''
                for fieldName in tableDef[tableName][item]:
                    if numFields < len(tableDef[tableName][item]):
                        separator = ','
                    else:
                        separator = ''
                    numFields = numFields + 1
                    fieldDef = ruianToPostGISColumnName(fieldName,tableDef[tableName]['skipNamespacePrefix']) + ' ' + ruianToPostGISDBTypes[tableDef[tableName][item][fieldName]['type']]
                    if tableDef[tableName][item][fieldName].has_key('notNull'):
                        if tableDef[tableName][item][fieldName]['notNull'] == 'yes':
                            fieldDef = fieldDef + ' NOT NULL'
                        if tableDef[tableName][item][fieldName]['pkey'] == 'yes':
                            pKey = ',CONSTRAINT ' + ruianToPostGISColumnName((tableName + '_' +   fieldName),tableDef[tableName]['skipNamespacePrefix']) + '_pk PRIMARY KEY (' + ruianToPostGISColumnName(fieldName,tableDef[tableName]['skipNamespacePrefix']) + ')'
                    fieldDef = fieldDef + separator
                    tableCreateSQL = tableCreateSQL + fieldDef
                tableCreateSQL = tableCreateSQL + pKey + ") WITH (OIDS=FALSE);"
                result[tableName]=tableCreateSQL
    return result

# ##############################################################################
#
# PostGIS_TableExists
#
# Vrací True, jestliže tabulka tableName v databázi existuje.
#
# ##############################################################################
def PostGIS_TableExists(tableName):
    print "Table exists(", tableName, ")"
    return False

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