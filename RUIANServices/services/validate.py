# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        validate
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

def validateAddress(resultFormat, street, houseNumber, recordNumber, orientationNumber, zipCode, locality, localityPart, districtNumber):
    return ""

def validateAddressServiceHandler(queryParams, response):

    s = validateAddress(
        p(queryParams, "Format", "xml"),
        p(queryParams, "Street"),
        p(queryParams, "HouseNumber"),
        p(queryParams, "RecordNumber"),
        p(queryParams, "OrientationNumber"),
        p(queryParams, "ZIPCode"),
        p(queryParams, "Locality"),
        p(queryParams, "LocalityPart"),
        p(queryParams, "DistrictNumber")
    )
    response.htmlData = s
    response.mimeFormat = getMimeFormat(p("Format", "xml"))
    response.handled = True
    return response

def createServiceHandlers():
    services.append(
        WebService("/Validate", u"Ověření adresy", u"Ověřuje existenci dané adresy",
                   u"""Umožňuje ověřit zadanou adresu. Adresa je zadána pomocí jednotlivých
                   prvků adresního místa.""",
            [
                getResultFormatParam(),
                RestParam("/Street",      u"Ulice", u"Název ulice"),
                RestParam("/Locality",    u"Obec", u"Obec"),
                RestParam("/HouseNumber", u"Číslo popisné", ""),
            ],
            [
                URLParam("ZIPCode",           u"PSČ", u"Poštovní směrovací číslo"),
                URLParam("LocalityPart",      u"Část obce", u"Část obce, pokud je známa"),
                URLParam("OrientationNumber", u"Číslo orientační", "")
            ],
            validateAddressServiceHandler,
            sendButtonCaption = u"Ověř adresu"
        )
    )