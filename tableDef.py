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

def main():
    pass

if __name__ == '__main__':
    main()

# if removeNamespace is set to true, than removes namespace prefix from XMLTagName
# additionally, it converts CamelCase RUIAN name to underscore notation
# obi:Kod -> Kod -> kod
# obi:GlobalniIdNavrhuZmeny -> GlobalniIdNavrhuZmeny -> globalni_id_navrhuZmeny
def ruianToPostGISColumnName(XMLTagName, removeNamespace):
    return XMLTagName

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
print (tabledef)