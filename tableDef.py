# -*- coding: cp1250 -*-
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
 "String"    : "text",
 "Integer"   : "integer",
 "DateTime"  : "date",
 "Long"      : "bigint",
 "MultiPointPropertyType"  : "string",
 "MultiSurfacePropertyType" : "string",
 "MultiCurvePropertyType" : "string"
}

tableDef = {
    "Obce":{
        "skipNamespacePrefix" : "true", # remove namespace prefix obi, oki etc
        "field":{
            "Kod":                   {"type":"Integer", "notNull" : "yes", "pkey" : "yes"},
            "Nazev":                 {"type":"String"},
            "StatusKod":             {"type":"Integer"},
            "PlatiOd":               {"type":"DateTime"},
            "PlatiDo":               {"type":"DateTime"},
            "IdTransakce":           {"type":"Long"},
            "GlobalniIdNavrhuZmeny": {"type":"Long"},
            "VlajkaText":            {"type":"String"},
            "ZnakText":              {"type":"String"},
            "DefinicniBod":          {"type":"MultiPointPropertyType",   "xmlSubPath" : "Geometrie/DefinicniBod"},
            "OriginalniHranice":     {"type":"MultiSurfacePropertyType", "xmlSubPath" : "Geometrie/OriginalniHranice"}
        },
        # indexy definuje ota
        "index":{"nazev":{"idxtype":"btree","cluster":"yes"}}
        },
    "CastiObci":{
        "skipNamespacePrefix" : "true", # remove namespace prefix coi, obi, oki etc
        "field":{
            "Kod":                   {"type":"Integer", "notNull" : "yes", "pkey" : "yes"},
            "Nazev":                 {"type":"String"},
            "Obec":                  {"type":"Integer", "xmlSubPath" : "Obec/Kod"}, # nadrazena obec
            "PlatiOd":               {"type":"DateTime"},
            "PlatiDo":               {"type":"DateTime"},
            "IdTransakce":           {"type":"Long"},
            "GlobalniIdNavrhuZmeny": {"type":"Long"},
            "DefinicniBod":          {"type":"MultiPointPropertyType",   "xmlSubPath" : "Geometrie/DefinicniBod"},
        },
        # indexy definuje ota
        "index":{"nazev":{"idxtype":"btree","cluster":"yes"}}
        },
    "Momc":{
        "skipNamespacePrefix" : "true", # remove namespace prefix mci, coi, obi, oki etc
        "field":{
            "Kod":                   {"type":"Integer", "notNull" : "yes", "pkey" : "yes"},
            "Nazev":                 {"type":"String"},
            "MOP":                   {"type":"Integer", "xmlSubPath" : "Mop/Kod"},
            "Obec":                  {"type":"Integer", "xmlSubPath" : "Obec/Kod"},  # nadrazena obec
            "PlatiOd":               {"type":"DateTime"},
            "PlatiDo":               {"type":"DateTime"},
            "IdTransakce":           {"type":"Long"},
            "GlobalniIdNavrhuZmeny": {"type":"Long"},
            "VlajkaText":            {"type":"String"},
            "ZnakText":              {"type":"String"},
            "DefinicniBod":          {"type":"MultiPointPropertyType",   "xmlSubPath" : "Geometrie/DefinicniBod"},
        },
        # indexy definuje ota
        "index":{"nazev":{"idxtype":"btree","cluster":"yes"}}
        },
    "Mop":{
        "skipNamespacePrefix" : "true", # remove namespace prefix mci, mpi, coi, obi, oki etc
        "field":{
            "Kod":                   {"type":"Integer", "notNull" : "yes", "pkey" : "yes"},
            "Nazev":                 {"type":"String"},
            "Obec":                  {"type":"Integer", "xmlSubPath" : "Obec/Kod"},  # nadrazena obec
            "PlatiOd":               {"type":"DateTime"},
            "PlatiDo":               {"type":"DateTime"},
            "IdTransakce":           {"type":"Long"},
            "GlobalniIdNavrhuZmeny": {"type":"Long"},
            "DefinicniBod":          {"type":"MultiPointPropertyType",   "xmlSubPath" : "Geometrie/DefinicniBod"},
        },
        # indexy definuje ota
        "index":{"nazev":{"idxtype":"btree","cluster":"yes"}}
        },
    "Ulice":{
        "skipNamespacePrefix" : "true", # remove namespace prefix uli, mci, mpi, coi, obi, oki etc
        "field":{
            "Kod":                   {"type":"Integer", "notNull" : "yes", "pkey" : "yes"},
            "Nazev":                 {"type":"String"},
            "Obec":                  {"type":"Integer", "xmlSubPath" : "Obec/Kod"},  # nadrazena obec
            "PlatiOd":               {"type":"DateTime"},
            "PlatiDo":               {"type":"DateTime"},
            "IdTransakce":           {"type":"Long"},
            "GlobalniIdNavrhuZmeny": {"type":"Long"},
            "DefinicniCara":         {"type":"MultiCurvePropertyType",   "xmlSubPath" : "Geometrie/DefinicniCara"},
        },
        # indexy definuje ota
        "index":{"nazev":{"idxtype":"btree","cluster":"yes"}}
        },
    "KatastralniUzemi":{
        "skipNamespacePrefix" : "true", # remove namespace prefix obi, oki etc
        "field":{
            "Kod":                   {"type":"Integer", "notNull" : "yes", "pkey" : "yes"},
            "Nazev":                 {"type":"String"},
            "ExistujeDigitalniMapa": {"type":"Boolean"},
            "Obec":                  {"type":"Integer", "xmlSubPath" : "Obec/Kod"},  # nadrazena obec
            "PlatiOd":               {"type":"DateTime"},
            "PlatiDo":               {"type":"DateTime"},
            "IdTransakce":           {"type":"Long"},
            "GlobalniIdNavrhuZmeny": {"type":"Long"},
            "RizeniId":              {"type":"Long"},
            "DefinicniBod":          {"type":"MultiPointPropertyType",   "xmlSubPath" : "Geometrie/DefinicniBod"},
            "OriginalniHranice":     {"type":"MultiSurfacePropertyType", "xmlSubPath" : "Geometrie/OriginalniHranice"}
        },
        # indexy definuje ota
        "index":{"nazev":{"idxtype":"btree","cluster":"yes"}}
        },
    "Parcely":{
        "skipNamespacePrefix" : "true", # remove namespace prefix obi, oki etc
        "field":{
            "Id":                    {"type":"Long", "notNull" : "yes", "pkey" : "yes"},
            "KmenoveCislo":          {"type":"Integer"},
            "PododdeleniCisla":      {"type":"Integer"},
            "VymeraParcely":         {"type":"Long"},
            "ZpusobyVyuzitiPozemku": {"type":"Integer"},
            "DruhCislovaniKod":      {"type":"Integer"},
            "DruhPozemkuKod":        {"type":"Integer"},
            "KatastralniUzemi":      {"type":"Integer", "xmlSubPath" : "KatastralniUzemi/Kod"},  # nadrazene katastralni uzemi
            "PlatiOd":               {"type":"DateTime"},
            "PlatiDo":               {"type":"DateTime"},
            "IdTransakce":           {"type":"Long"},
            "RizeniId":              {"type":"Long"},
            "DefinicniBod":          {"type":"MultiPointPropertyType",   "xmlSubPath" : "Geometrie/DefinicniBod"},
            "OriginalniHranice":     {"type":"MultiSurfacePropertyType", "xmlSubPath" : "Geometrie/OriginalniHranice"}
        },
        # indexy definuje ota
        "index":{"nazev":{"idxtype":"btree","cluster":"yes"}}
        },
    "StavebniObjekty":{
        "skipNamespacePrefix" : "true", # remove namespace prefix soi, com, mci, mpi, coi, obi, oki etc
        "field":{
            "Kod":                     {"type":"Integer", "notNull" : "yes", "pkey" : "yes"},
            "CislaDomovni":            {"type":"Integer", "xmlSubPath" : "CislaDomovni/CisloDomovni"},  # kolekce cisel domovnich
            "IdentifikacniParcela":    {"type":"Long", "xmlSubPath" : "IdentifikacniParcela/Id"},  # parcela nebo jedna z parcel, na nichž je stavebni objekt postaven, zvolena pro identifikaci objektu
            "TypStavebnihoObjektuKod": {"type":"Integer"},  # muze nabyvat hodnot: 1-budova s cislem popisnym, 2-budova s cislem evidencnim, 3-budova bez cisla popisneho ci evidencniho
            "ZpusobyVyuzitiKod":       {"type":"Integer"},
            "CastObce":                {"type":"Integer", "xmlSubPath" : "CastObce/Kod"} , # nadrazena cast obce
            "Momc":                    {"type":"Integer", "xmlSubPath" : "Momc/Kod"},  # nadrazeny MOMC
            "PlatiOd":                 {"type":"DateTime"},
            "PlatiDo":                 {"type":"DateTime"},
            "GlobalniIdNavrhuZmeny":   {"type":"Long"},
            "IdTransakce":             {"type":"Long"},
            "IsknBudovaId":            {"type":"Long"},
            "DefinicniBod":            {"type":"MultiPointPropertyType",   "xmlSubPath" : "Geometrie/DefinicniBod"},
            "OriginalniHranice":       {"type":"MultiSurfacePropertyType", "xmlSubPath" : "Geometrie/OriginalniHranice"}
        },
        # indexy definuje ota
        "index":{"nazev":{"idxtype":"btree","cluster":"yes"}}
        },
    "AdresniMista":{
        "skipNamespacePrefix" : "true", # remove namespace prefix obi, oki etc
        "field":{
            "Kod":                    {"type":"Integer", "notNull" : "yes", "pkey" : "yes"},
            "CisloDomovni":           {"type":"Integer"},
            "CisloOrientacni":        {"type":"Integer"},
            "CisloOrientacniPismeno": {"type":"String"},
            "Psc":                    {"type":"Integer"},
            "StavebniObjekt":         {"type":"Integer", "xmlSubPath" : "StavebniObjekt/Kod"},  # nadrazeny stavebni objekt
            "Ulice":                  {"type":"Long", "xmlSubPath" : "Ulice/Kod"},  # nadrazena ulice
            "PlatiOd":                {"type":"DateTime"},
            "PlatiDo":                {"type":"DateTime"},
            "IdTransakce":            {"type":"Long"},
            "GlobalniIdNavrhuZmeny":  {"type":"Long"},
            "AdresniBod":             {"type":"MultiPointPropertyType", "xmlSubPath" : "Geometrie/DefinicniBod/AdresniBod"}
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
