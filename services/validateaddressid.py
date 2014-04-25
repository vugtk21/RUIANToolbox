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
import RUIANInterface, RUIANReferenceDB

def validateAddressId(resultFormat, addressPlaceId):
    return ""

def validateAddressIdServiceHandler(queryParams, response):
    builder = MimeBuilder(queryParams["Format"])
    response.mimeFormat = builder.getMimeFormat()
    address = RUIANInterface.FindAddress(queryParams["AddressPlaceId"], builder)  ### předělat !!!
    if address:
        response.htmlData = builder.listToResponseText(["True"])
    else:
        response.htmlData = builder.listToResponseText(["False"])
    response.handled = True
    return response

def createServiceHandlers():
    services.append(
        WebService("/ValidateAddressId", u"Ověření identifikátoru adresy", u"Ověřuje existenci daného identifikátoru adresy",
                   u"""Umožňuje ověřit existenci zadaného identifikátoru adresy RÚIAN v databázi.""",
            [
                getResultFormatParam()
            ],
            [
                getAddressPlaceIdParamURL()
            ],
            validateAddressIdServiceHandler,
            sendButtonCaption = u"Ověř identifikátor adresy"
        )
    )