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

# RUIAN to PostGIS SQL conversion table
ruianToPostGISDBTypes = {
 "string"    : "text",
 "integer"   : "integer",
 "datetime"  : "date",
 "long"      : "bigint",
 "MultiPointPropertyType"  : "string",
 "MultiSurfacePropertyType" : "string"
}

tableDef = {
    "obec":{
        "skipNamespacePrefix" : "true", # remove namespace prefix obi, oki etc
        "field":{
            "Kod":                   {"type":"integer", "notNull" : "yes", "pkey" : "yes"},
            "Nazev":                 {"type":"string"},
            "StatusKod":             {"type":"integer"},
            "PlatiOd":               {"type":"datetime"},
            "PlatiDo":               {"type":"datetime"},
            "IdTransakce":           {"type :long"},
            "GlobalniIdNavrhuZmeny": {"type":"long"},
            "VlajkaText":            {"type":"string"},
            "ZnakText":              {"type":"string"},
            "DefinicniBod":          {"type":"MultiPointPropertyType" },
            "OriginalniHranice":     {"type":"MultiSurfacePropertyType"}
        },
        # indexy definuje ota
        "index":{"nazev":{"idxtype":"btree","cluster":"yes"}}
        }
    }


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
