# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        validateaddressid
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

def validateAddressId(resultFormat, addressPlaceId):
    return ""

def validateAddressIdServiceHandler(queryParams, response):
    s = nearByAddresses(
        p(queryParams, "Format", "xml"),
        p(queryParams, "AddressPlaceId", "")
    )
    response.htmlData = s
    response.mimeFormat = getMimeFormat(p("Format", "xml"))
    response.handled = True
    return response

def createServiceHandlers():
    services.append(
        WebService("/ValidateAddressId", u"Ověření identifikátoru adresy", u"Ověřuje existenci daného identifikátoru adresy",
                   u"""Umožňuje ověřit existenci zadaného identifikátoru adresy RÚIAN v databázi.""",
            [
                getResultFormatParam(),
                getAddressPlaceIdParamRest()
            ],
            [ ],
            validateAddressIdServiceHandler,
            sendButtonCaption = u"Ověř identifikátor adresy"
        )
    )