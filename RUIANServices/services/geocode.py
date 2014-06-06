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
import RUIANConnection

def geocodeID(builder, AddressID):
    coordinates = RUIANConnection.findCoordinates(AddressID)
    return builder.coordintesToResponseText(coordinates)

def geocodeAddress(builder, street, houseNumber, recordNumber, orientationNumber, orientationNumberCharacter, zipCode, locality, localityPart, districtNumber):
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
    coordinates = RUIANConnection.findCoordinatesByAddress(dict)
    return builder.coordintesToResponseText(coordinates)

def geocodeAddressServiceHandler(queryParams, response):

    def p(name, defValue = ""):
        if queryParams.has_key(name):
            return urllib.unquote(queryParams[name])
        else:
            return defValue

    resultFormat = p("Format", "text")
    builder = MimeBuilder(resultFormat)
    response.mimeFormat = builder.getMimeFormat()

    if queryParams.has_key("AddressPlaceId"):
        #response = IDCheck.IDCheckServiceHandler(queryParams, response, builder)
        s = geocodeID(builder, queryParams.AddressPlaceId)
        response.htmlData = s
    elif queryParams.has_key("SearchText"):
        response.handled = True
        response.htmlData = builder.listToResponseText([u"neimplementováno"])
        return response
    else:
        s = geocodeAddress(
            builder,
            p("Street"),
            p("HouseNumber"),
            p("RecordNumber"),
            p("OrientationNumber"),
            p("OrientationNumberCharacter"),
            p("ZIPCode"),
            p("Locality"),
            p("LocalityPart"),
            p("DistrictNumber")
        )
        response.htmlData = s
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
                URLParam("OrientationNumberCharacter", u"Písmeno čísla orientačního", ""),
                URLParam("RecordNumber",      u"Číslo evidenční", u"Číslo evidenční, pokud je přiděleno"),
                URLParam("DistrictNumber",    u"Obvod", u"Číslo městského obvodu, pokud existuje")
            ],
            geocodeAddressServiceHandler,
            sendButtonCaption = u"Najdi polohu",
            htmlInputTemplate=""
        )

    )