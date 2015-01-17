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

def buildValidateDict(street, houseNumber, recordNumber, orientationNumber, orientationNumberCharacter, zipCode, locality, localityPart, districtNumber):
    return {
        "street": street,
        "houseNumber": houseNumber,
        "recordNumber": recordNumber,
        "orientationNumber": orientationNumber,
        "orientationNumberCharacter": orientationNumberCharacter,
        "zipCode": str(zipCode).replace(" ", ""),
        "locality": locality,
        "localityPart": localityPart,
        "districtNumber": districtNumber
    }

def validateAddress(builder, street, houseNumber, recordNumber, orientationNumber, orientationNumberCharacter, zipCode, locality, localityPart, districtNumber):

    if not rightAddress(street, houseNumber, recordNumber, orientationNumber, orientationNumberCharacter, zipCode, locality, localityPart, districtNumber):
        return "False"

    dict = buildValidateDict(street, houseNumber, recordNumber, orientationNumber, orientationNumberCharacter, zipCode, locality, localityPart, districtNumber)

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
                   prvků adresy.""",
            [
                getResultFormatParam()
            ],
            [
                URLParam("Locality",          u"Obec", u"Obec", htmlTags = ' class="RUIAN_TOWN_INPUT" '),
                URLParam("LocalityPart",      u"Část obce", u"Část obce, pokud je známa", htmlTags = ' class="RUIAN_TOWNPART_INPUT" '),
                getDistrictNumberURL(False),
                URLParam("Street",            u"Ulice", u"Název ulice", htmlTags = ' class="RUIAN_STREET_INPUT" '),
                getHouseNumberURL(False),
                getRecordNumberURL(False),
                getOrientationNumberURL(False),
                getOrientationNumberCharacterURL(False),
                #URLParam("OrientationNumberCharacter", u"Písmeno čísla<br>orientačního", ""),
                getZIPCodeURL(False),
                URLParam("FillAddressButton",  u"Doplň adresu", u"Najde v databázi adresu odpovídající vyplněným hodnotám", "", False)
            ],
            validateAddressServiceHandler,
            sendButtonCaption = u"Ověř adresu",
            htmlInputTemplate = ''
        )
    )
