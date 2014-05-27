# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        geocode
# Purpose:
#
# Author:      Radek Augustýn
#
# Created:     13/11/2013
# Copyright:   (c) Radek Augustýn 2013
# Licence:     <your licence>
#-------------------------------------------------------------------------------
__author__ = 'Radek Augustýn'

from HTTPShared import *

def geocodeAddress(resultFormat, addressPlaceId):
    return ""

def geocodeAddressServiceHandler(queryParams, response):

    s = geocodeAddress(
        p(queryParams, "Format", "xml"),
        p(queryParams, "AddressPlaceId")
    )
    response.htmlData = s
    response.mimeFormat = getMimeFormat(p("Format", "xml"))
    response.handled = True
    return response

def createServiceHandlers():
    services.append(
        WebService("/Geocode", u"Geokódování", u"Vyhledávání adresního bodu adresního místa",
            u"""<p>Umožňuje klientům jednotným způsobem získat souřadnice zadaného adresního místa.
            Adresní místo zadáme buď pomocí jeho identifikátoru RÚIAN nebo pomocí textového řetězce adresy.<br>""",
            [
                getResultFormatParam()
            ],
            [
                getAddressPlaceIdParamURL(),
                getSearchTextParam(),
                URLParam("Street",            u"Ulice", u"Název ulice"),
                URLParam("Locality",          u"Obec",  u"Obec"),
                URLParam("HouseNumber",       u"Číslo popisné", ""),
                URLParam("ZIPCode",           u"PSČ", u"Poštovní směrovací číslo"),
                URLParam("LocalityPart",      u"Část obce", u"Část obce, pokud je známa"),
                URLParam("OrientationNumber", u"Číslo orientační", ""),
                URLParam("RecordNumber",      u"Číslo evidenční", u"Číslo evidenční, pokud je přiděleno"),
                URLParam("DistrictNumber",    u"Obvod", u"Číslo městského obvodu, pokud existuje")
            ],
            geocodeAddressServiceHandler,
            sendButtonCaption = u"Najdi polohu",
            htmlInputTemplate=""
        )

    )