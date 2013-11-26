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

def nearByAddresses(resultFormat, JTSKX, JTSKY, Distance):
    return ""

def nearByAddressesServiceHandler(queryParams, response):

    s = nearByAddresses(
        p(queryParams, "Format", "xml"),
        p(queryParams, "JTSKX", ""),
        p(queryParams, "JTSKY", ""),
        p(queryParams, "Distance", "")
    )
    response.htmlData = s
    response.mimeFormat = getMimeFormat(p("Format", "xml"))
    response.handled = True
    return response

def createServiceHandlers():
    services.append(
        WebService("/NearbyAddresses", u"Blízké adresy", u"Hledá adresu nejbližší daným souřadnicím",
                   u"""Umožňuje vyhledat adresní místa v okolí zadaných souřadnic do určité vzdálenosti.
                   Vrací záznamy databáze RÚIAN setříděné podle vzdálenosti od zadaných souřadnic.""",
            [
                getResultFormatParam(),
                RestParam("/JTSKX", u"JTSK X", u"Souřadnice X v systému S-JTSK"),
                RestParam("/JTSKY", u"JTSK Y", u"Souřadnice Y v systému S-JTSK"),
                RestParam("/Distance", u"Vzdálenost", u"Vzdálenost v metrech od vloženého bodu")
            ],
            [ ],
            nearByAddressesServiceHandler,
            sendButtonCaption = u"Hledej blízké adresy"
        )
    )
