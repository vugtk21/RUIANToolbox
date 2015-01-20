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

def geocodeAddress(builder, street, houseNumber, recordNumber, orientationNumber, orientationNumberCharacter, zipCode, locality, localityPart, districtNumber, withID, withAddress):
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
        lines = []
        for item in coordinates:
            dictionary = {"JTSKY": item[0], "JTSKX": item[1],"id": str(item[2]), "locality": item[3], "localityPart": item[4], "street": item[5], "houseNumber": item[6], "recordNumber": item[7], "orientationNumber": item[8], "orientationNumberCharacter": item[9], "zipCode": item[10], "districtNumber": item[11]}
            lines.append(dictionary)
        s = builder.listOfDictionariesToResponseText(lines, withID, withAddress)
        return s
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
    withID = p("ExtraInformation") == "id"
    withAddress = p("ExtraInformation") == "address"

    if queryParams.has_key("AddressPlaceId"):
        #response = IDCheck.IDCheckServiceHandler(queryParams, response, builder)
        queryParams["AddressPlaceId"] = numberCheck(queryParams["AddressPlaceId"])
        if queryParams["AddressPlaceId"] != "":
            coordinates = geocodeID(queryParams["AddressPlaceId"])
            if coordinates != []:
                temp = coordinates[0]
                dictionary = {"JTSKX": temp[0], "JTSKY": temp[1],"id": str(temp[2]), "locality": temp[3], "localityPart": temp[4], "street": temp[5], "houseNumber": temp[6], "recordNumber": temp[7], "orientationNumber": temp[8], "orientationNumberCharacter": temp[9], "zipCode": temp[10], "districtNumber": temp[11]}
                s = builder.listOfDictionariesToResponseText([dictionary], withID, withAddress)
            else:
                s = ""
        else:
            s = ""

    elif queryParams.has_key("SearchText"):
        parser = parseaddress.AddressParser()
        candidates = parser.fullTextSearchAddress(queryParams["SearchText"])
        lines = []
        for candidate in candidates:
            coordinates = geocodeID(candidate[0])
            if coordinates == []:
                continue
            else:
                temp = coordinates[0]
            #if candidate[4] == "č.p.":
            #    houseNumber = candidate[5]
            #    recordNumber = ""
            #else:
            #    houseNumber = ""
            #    recordNumber = candidate[5]
            dictionary = {"JTSKX": temp[0], "JTSKY": temp[1],"id": str(temp[2]), "locality": temp[3], "localityPart": temp[4], "street": temp[5], "houseNumber": temp[6], "recordNumber": temp[7], "orientationNumber": temp[8], "orientationNumberCharacter": temp[9], "zipCode": temp[10], "districtNumber": temp[11]}
            lines.append(dictionary)
        s = builder.listOfDictionariesToResponseText(lines, withID, withAddress)
        #s = builder.coordintesToResponseText(temp)

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
            p("DistrictNumber"),
            withID,
            withAddress
        )
    response.htmlData = s
    response.handled = True
    return response

def createServiceHandlers():
    services.append(
        WebService("/Geocode", u"Geokódování", u"Vyhledávání definičního bodu adresního místa",
            u"""<p>Umožňuje klientům jednotným způsobem získat souřadnice zadaného adresního místa.
            Adresní místo zadáme buď pomocí jeho identifikátoru RÚIAN nebo pomocí textového řetězce adresy.<br>""",
            [
                getResultFormatParam()
            ],
            [
                getAddressPlaceIdParamURL(),
                getSearchTextParam(),
                URLParam("Locality",          u"Obec",  u"Obec", "", True, htmlTags = ' class="RUIAN_TOWN_INPUT" '),
                URLParam("LocalityPart",      u"Část obce", u"Část obce, pokud je známa", "", True, htmlTags = ' class="RUIAN_TOWNPART_INPUT" '),
                getDistrictNumberURL(),
                URLParam("Street",            u"Ulice", u"Název ulice", "", True, htmlTags = ' class="RUIAN_STREET_INPUT" '),
                getHouseNumberURL(),
                getRecordNumberURL(),
                getOrientationNumberURL(),
                getOrientationNumberCharacterURL(),
                getZIPCodeURL(),
                URLParam("ExtraInformation",  u"Další informace", u"Vypíše zvolený druh dodatečných informací", "", False),
                URLParam("FillAddressButton",  u"Doplň adresu", u"Najde v databázi adresu odpovídající vyplněným hodnotám", "", True)
            ],
            geocodeAddressServiceHandler,
            sendButtonCaption = u"Najdi polohu",
            htmlInputTemplate=""
        )

    )