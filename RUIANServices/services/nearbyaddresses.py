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


import RUIANConnection
from HTTPShared import *
import parseaddress

def FormatAddress(address):
    FormatedAddress = u""
    houseNumberStr = u""

    if address.houseNumber != "":
        houseNumberStr += address.houseNumber
        if address.orientationNumber != "":
            houseNumberStr += "/"+address.orientationNumber+address.orientationNumberCharacter
    elif address.recordNumber != "":
        houseNumberStr = u"č. ev. " + address.recordNumber

    if address.street != "":
        FormatedAddress += address.street + " " + houseNumberStr + ", "
        if address.locality == "Praha":
            FormatedAddress += address.localityPart + ", " + address.zipCode + ", " + address.locality + " " + address.districtNumber
        elif address.locality == address.localityPart:
            FormatedAddress += address.zipCode + " " + address.locality
        else:
            FormatedAddress += address.localityPart + ", " + address.zipCode + " " + address.locality
    else:
        if address.locality == address.localityPart:
            if address.recordNumber != "":
                FormatedAddress += houseNumberStr + ", "
            else:
                FormatedAddress += u"č.p. " + address.houseNumber + ", "
            FormatedAddress += address.zipCode + " " + address.locality
        else:
            FormatedAddress += address.localityPart + " " + houseNumberStr + ", " + address.zipCode + " " + address.locality
            if address.locality == "Praha":
                FormatedAddress += ", " + address.districtNumber

    return FormatedAddress

def nearByAddresses(builder, JTSKY, JTSKX, Distance, withID):
    if JTSKX.isdigit() and JTSKY.isdigit() and Distance.isdigit():
        addresses = RUIANConnection.getNearbyLocalities(JTSKX, JTSKY, Distance)
        parser = parseaddress.AddressParser()
        FormattedAddress = parser.buildAddress(builder,addresses,withID)
        s = builder.listToResponseText(FormattedAddress, True)
        return s
    else:
        return ""

def nearByAddressesServiceHandler(queryParams, response):
    builder = MimeBuilder(queryParams["Format"])
    response.mimeFormat = builder.getMimeFormat()
    if queryParams.has_key("ExtraInformation"):
        withID = queryParams["ExtraInformation"].lower() == "id"
    else:
        withID = False

    s = nearByAddresses(
        builder,
        p(queryParams, "JTSKY", ""),
        p(queryParams, "JTSKX", ""),
        p(queryParams, "Distance", ""),
        withID
    )
    response.htmlData = s
    #response.mimeFormat = getMimeFormat(p("Format", "xml"))
    response.handled = True
    return response

def createServiceHandlers():
    services.append(
        WebService("/NearbyAddresses", u"Blízké adresy", u"Hledá adresu nejbližší daným souřadnicím",
                   u"""Umožňuje vyhledat adresní místa v okolí zadaných souřadnic do určité vzdálenosti.
                   Vrací záznamy databáze RÚIAN setříděné podle vzdálenosti od zadaných souřadnic.""",
            [
                getResultFormatParam(),
                RestParam("/JTSKY", u"JTSK Y", u"Souřadnice Y v systému S-JTSK"),
                RestParam("/JTSKX", u"JTSK X", u"Souřadnice X v systému S-JTSK"),
                RestParam("/Distance", u"Vzdálenost [m]", u"Vzdálenost v metrech od vloženého bodu")
            ],
            [
                URLParam("ExtraInformation", u"Další informace", u"Vypíše zvolený druh dodatečných informací", "", False)
            ],
            nearByAddressesServiceHandler,
            sendButtonCaption = u"Hledej blízké adresy",
            htmlInputTemplate = '''<select>
                                        <option value="text">text</option>
                                        <option value="xml">xml</option>
                                        <option value="html">html</option>
                                        <option value="json">json</option>
                                    </select>'''
        )
    )
