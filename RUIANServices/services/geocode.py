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
import parseaddress

def geocodeID(AddressID):
    coordinates = RUIANConnection.findCoordinates(AddressID)
    return coordinates

def geocodeAddress(builder, street, houseNumber, recordNumber, orientationNumber, orientationNumberCharacter, zipCode, locality, localityPart, districtNumber):
    if rightAddress(street, houseNumber, recordNumber, orientationNumber, orientationNumberCharacter, zipCode, locality, localityPart, districtNumber):
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
    else:
        return ""


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
        queryParams["AddressPlaceId"] = numberCheck(queryParams["AddressPlaceId"])
        if queryParams["AddressPlaceId"] != "":
            s = builder.coordintesToResponseText(geocodeID(queryParams["AddressPlaceId"]))
        else:
            response.htmlData = ""
            response.mimeFormat = builder.getMimeFormat()
            response.handled = True
            return response

    elif queryParams.has_key("SearchText"):
        parser = parseaddress.AddressParser()
        candidates = parser.fullTextSearchAddress(queryParams["SearchText"])
        temp = []
        for candidate in candidates:
            temp = geocodeID(candidate[0]) + temp
        s = builder.coordintesToResponseText(temp)

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
                URLParam("Street",            u"Ulice", u"Název ulice", "", True),
                URLParam("HouseNumber",       u"Číslo popisné", "", "", True),
                URLParam("RecordNumber",      u"Číslo evidenční", u"Číslo evidenční, pokud je přiděleno", "", True),
                URLParam("OrientationNumber", u"Číslo orientační", "", "", True),
                URLParam("OrientationNumberCharacter", u"Písmeno čísla<br>orientačního", "", "", True),
                URLParam("ZIPCode",           u"PSČ", u"Poštovní směrovací číslo", "", True),
                URLParam("Locality",          u"Obec",  u"Obec", "", True),
                URLParam("LocalityPart",      u"Část obce", u"Část obce, pokud je známa", "", True),
                URLParam("DistrictNumber",    u"Číslo městského<br>obvodu v Praze", u"Číslo městského obvodu, pokud existuje", "", True)

            ],
            geocodeAddressServiceHandler,
            sendButtonCaption = u"Najdi polohu",
            htmlInputTemplate=""
        )

    )