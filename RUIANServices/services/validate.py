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
import RUIANConnection

def validateAddress(builder, street, houseNumber, recordNumber, orientationNumber, orientationNumberCharacter, zipCode, locality, localityPart, districtNumber):
    dict = {
    "street": street,
    "houseNumber": houseNumber,
    "recordNumber": recordNumber,
    "orientationNumber": orientationNumber,
    "orientationNumberCharacter": orientationNumberCharacter,
    "zipCode": zipCode,
    "locality": locality,
    "localityPart": localityPart,
    "districtNumber": districtNumber
}
    result = RUIANConnection.validateAddress(dict)
    return builder.listToResponseText(result)

def validateAddressServiceHandler(queryParams, response):
    builder = MimeBuilder(queryParams["Format"])
    response.mimeFormat = builder.getMimeFormat()

    s = validateAddress(
        builder,
        p(queryParams, "Street"),
        p(queryParams, "HouseNumber"),
        p(queryParams, "RecordNumber"),
        p(queryParams, "OrientationNumber"),
        p(queryParams, "OrientationNumberCharacter"),
        p(queryParams, "ZIPCode"),
        p(queryParams, "Locality"),
        p(queryParams, "LocalityPart"),
        p(queryParams, "DistrictNumber")
    )
    response.htmlData = s
    response.handled = True
    return response

def createServiceHandlers():
    services.append(
        WebService("/Validate", u"Ověření adresy", u"Ověřuje existenci dané adresy",
                   u"""Umožňuje ověřit zadanou adresu. Adresa je zadána pomocí jednotlivých
                   prvků adresního místa.""",
            [
                getResultFormatParam()
            ],
            [
                URLParam("Street",      u"Ulice", u"Název ulice"),
                URLParam("HouseNumber", u"Číslo popisné", ""),
                URLParam("RecordNumber", u"Číslo evidenční", u"Číslo evidenční, pokud je přiděleno"),
                URLParam("OrientationNumber", u"Číslo orientační", ""),
                URLParam("OrientationNumberCharacter", u"Písmeno čísla orientačního", ""),
                URLParam("ZIPCode",           u"PSČ", u"Poštovní směrovací číslo"),
                URLParam("Locality",    u"Obec", u"Obec"),
                URLParam("LocalityPart",      u"Část obce", u"Část obce, pokud je známa"),
                URLParam("DistrictNumber", u"Číslo městského obvodu", u"Číslo městského obvodu, pokud existuje")
            ],
            validateAddressServiceHandler,
            sendButtonCaption = u"Ověř adresu",
            htmlInputTemplate = ''
        )
    )