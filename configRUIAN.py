# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        configRUIAN
# Purpose:     Definuje hodnoty načítané z exportního souboru RÚIAN
#
# Author:      Radek Augustýn, Tomáš Vacek, Otakar Růžička
#
# Created:     03.05.2013
# Copyright:   (c) VÚGTK 2013
# Licence:     <your licence>
#-------------------------------------------------------------------------------

SKIPNAMESPACEPREFIX = True
FIELDS_KEY_NAME     = "fields"

""" Slovník definující jednotlivé načítané tabulky. Pro každou tabulku je jeden
záznam, jehož název (klíč) je shodný s názvem XML tagu. Např. <vf:Obce> budou uloženy
v tabulce Obce.

Tento záznam je opět dictionary, obsahující:
"fields" ... definice jednotlivých sloupců v tabulce
"index"  ... definice indexů

Obec -> Obce
Field -> Fields
"skipNamespacePrefix" -> SKIPNAMESPACEPREFIX
"""
tableDef = {
    "Obce":{
        "fields":{
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
        # indexy se nadefinuji podle toho, jak se bude vyhledavat
        "indexes":{
             "Nazev":{"fields":"Nazev","idxtype":"btree","cluster":"yes"}
        }
        },
    "CastiObci": {
        "fields":{
            "Kod":                   {"type":"Integer", "notNull" : "yes", "pkey" : "yes"},
            "Nazev":                 {"type":"String"},
            "Obec":                  {"type":"Integer", "xmlSubPath" : "Obec/Kod"}, # nadrazena obec
            "PlatiOd":               {"type":"DateTime"},
            "PlatiDo":               {"type":"DateTime"},
            "IdTransakce":           {"type":"Long"},
            "GlobalniIdNavrhuZmeny": {"type":"Long"},
            "DefinicniBod":          {"type":"MultiPointPropertyType",   "xmlSubPath" : "Geometrie/DefinicniBod"},
        },

        "index":{"nazev":{"idxtype":"btree","cluster":"yes"}}
        },
	"Momc":{
        "fields":{
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

        "index":{"nazev":{"idxtype":"btree","cluster":"yes"}}
        },
	"Mop":{
        "fields":{
            "Kod":                   {"type":"Integer", "notNull" : "yes", "pkey" : "yes"},
            "Nazev":                 {"type":"String"},
			"Obec":                  {"type":"Integer", "xmlSubPath" : "Obec/Kod"},  # nadrazena obec
            "PlatiOd":               {"type":"DateTime"},
            "PlatiDo":               {"type":"DateTime"},
            "IdTransakce":           {"type":"Long"},
            "GlobalniIdNavrhuZmeny": {"type":"Long"},
            "DefinicniBod":          {"type":"MultiPointPropertyType",   "xmlSubPath" : "Geometrie/DefinicniBod"},
        },

        "index":{"nazev":{"idxtype":"btree","cluster":"yes"}}
        },
	"Ulice":{
        "fields":{
            "Kod":                   {"type":"Integer", "notNull" : "yes", "pkey" : "yes"},
            "Nazev":                 {"type":"String"},
			"Obec":                  {"type":"Integer", "xmlSubPath" : "Obec/Kod"},  # nadrazena obec
            "PlatiOd":               {"type":"DateTime"},
            "PlatiDo":               {"type":"DateTime"},
            "IdTransakce":           {"type":"Long"},
            "GlobalniIdNavrhuZmeny": {"type":"Long"},
            "DefinicniCara":         {"type":"MultiCurvePropertyType",   "xmlSubPath" : "Geometrie/DefinicniCara"},
        },

        "index":{"nazev":{"idxtype":"btree","cluster":"yes"}}
        },
	"KatastralniUzemi":{
        "fields":{
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

        "index":{"nazev":{"idxtype":"btree","cluster":"yes"}}
        },
	"Parcely":{
        "fields":{
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

        "index":{"nazev":{"idxtype":"btree","cluster":"yes"}}
        },
	"StavebniObjekty":{
        "fields":{
            "Kod":                     {"type":"Integer", "notNull" : "yes", "pkey" : "yes"},
            "CislaDomovni":            {"type":"Integer", "xmlSubPath" : "CislaDomovni/CisloDomovni"},  # kolekce cisel domovnich
            "IdentifikacniParcela":    {"type":"Long", "xmlSubPath" : "IdentifikacniParcela/Id"},       # parcela nebo jedna z parcel, na nich ...  je stavebni objekt postaven, zvolena pro identifikaci objektu
			"TypStavebnihoObjektuKod": {"type":"Integer"},                                              # muze nabyvat hodnot: 1-budova s cislem popisnym, 2-budova s cislem evidencnim, 3-budova bez cisla popisneho ci evidencniho
            "ZpusobyVyuzitiKod":       {"type":"Integer"},
			"CastObce":                {"type":"Integer", "xmlSubPath" : "CastObce/Kod"},               # nadrazena cast obce
			"Momc":                    {"type":"Integer", "xmlSubPath" : "Momc/Kod"},                   # nadrazeny MOMC
			"PlatiOd":                 {"type":"DateTime"},
            "PlatiDo":                 {"type":"DateTime"},
            "GlobalniIdNavrhuZmeny":   {"type":"Long"},
			"IdTransakce":             {"type":"Long"},
            "IsknBudovaId":            {"type":"Long"},
            "DefinicniBod":            {"type":"MultiPointPropertyType",   "xmlSubPath" : "Geometrie/DefinicniBod"},
			"OriginalniHranice":       {"type":"MultiSurfacePropertyType", "xmlSubPath" : "Geometrie/OriginalniHranice"}
        },

        "index":{"nazev":{"idxtype":"btree","cluster":"yes"}}
        },
	"AdresniMista":{
        "fields":{
            "Kod":                    {"type":"Integer", "notNull" : "yes", "pkey" : "yes"},
            "CisloDomovni":           {"type":"Integer"},
            "CisloOrientacni":        {"type":"Integer"},
			"CisloOrientacniPismeno": {"type":"String"},
			"Psc":                    {"type":"Integer"},
			"StavebniObjekt":         {"type":"Integer", "xmlSubPath" : "StavebniObjekt/Kod"},  # nadrazeny stavebni objekt
			"Ulice":                  {"type":"Long", "xmlSubPath" : "Ulice/Kod"},              # nadrazena ulice
            "PlatiOd":                {"type":"DateTime"},
            "PlatiDo":                {"type":"DateTime"},
            "IdTransakce":            {"type":"Long"},
            "GlobalniIdNavrhuZmeny":  {"type":"Long"},
            "AdresniBod":             {"type":"MultiPointPropertyType", "xmlSubPath" : "Geometrie/DefinicniBod/AdresniBod"}
        },
        "index":{"nazev":{"idxtype":"btree","cluster":"yes"}}
        }
	}