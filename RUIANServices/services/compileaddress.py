#!C:/Python27/python.exe
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        compileaddress
# Purpose:
#
# Author:      Radek Augustýn
#
# Created:     13/11/2013
# Copyright:   (c) Radek Augustýn 2013
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import codecs
from HTTPShared import *
import urllib
import IDCheck
import fulltextsearch
import RUIANConnection
import validate
import HTTPShared

def errorMessage(msg):
    pass

class TextFormat:
    plainText = 0
    xml       = 1
    json      = 2
    html      = 3

def compileAddress(builder, street, houseNumber, recordNumber, orientationNumber, orientationNumberCharacter, zipCode, locality, localityPart, districtNumber, doValidate = False, withRUIANId = False):
    """
        @param street            string  Název ulice
        @param locality          string  Obec
        @param houseNumber       number  Číslo popisné
        @param zipCode           number  Poštovní směrovací číslo
        @param localityPart      string  Část obce, pokud je známa
        @param orientationNumber number  Číslo orientační
        @param orientationNumberCharacter string  Písmeno čísla orientačního
    """
    dict = validate.buildValidateDict(street, houseNumber, recordNumber, orientationNumber, orientationNumberCharacter, zipCode, locality, localityPart, districtNumber)

    if doValidate or withRUIANId:
        rows = RUIANConnection.getAddresses(dict)

        if len(rows) == 1:
            (houseNumber, orientationNumber, orientationNumberCharacter, zipCode, locality, localityPart, nazevMOP, street, typSO, ruianId) = rows[0]
            if typSO != "č.p.":
                recordNumber = houseNumber
                houseNumber = ""
            if nazevMOP != None and nazevMOP != "":
                districtNumber = nazevMOP[nazevMOP.find(" ") + 1:]
            if not withRUIANId: ruianId = ""
        else:
            return ""
    else:
        ruianId = ""


    if builder == None:
        return str((street, houseNumber, recordNumber, orientationNumber, orientationNumberCharacter, zipCode, locality, localityPart, districtNumber, ruianId))
    elif builder.formatText == "json":
        return compileAddressAsJSON(street, houseNumber, recordNumber, orientationNumber, orientationNumberCharacter, zipCode, locality, localityPart, districtNumber, ruianId)
    elif builder.formatText == "xml":
        return compileAddressAsXML(street, houseNumber, recordNumber, orientationNumber, orientationNumberCharacter, zipCode, locality, localityPart, districtNumber, ruianId)
    elif builder.formatText == "texttoonerow" or builder.formatText == "htmltoonerow":
        return compileAddressToOneRow(street, houseNumber, recordNumber, orientationNumber, orientationNumberCharacter, zipCode, locality, localityPart, districtNumber, ruianId)
    else:
        return builder.listToResponseText(compileAddressAsText(street, houseNumber, recordNumber, orientationNumber, orientationNumberCharacter, zipCode, locality, localityPart, districtNumber, ruianId))

def compileAddressServiceHandler(queryParams, response):

    def addId(self, id, str, builder):
        if builder.formatText == "json":
            return '\t"id": ' + id + ",\n" + str
        elif builder.formatText == "xml":
            return "\t<id>" + id + "</id>\n" + str
        else:
            return id + builder.lineSeparator + str

    def p(name, defValue = ""):
        return HTTPShared.getQueryParam(queryParams, name, defValue)

    resultFormat = p("Format", "text")
    builder = MimeBuilder(resultFormat)
    response.mimeFormat = builder.getMimeFormat()

    if queryParams.has_key("ExtraInformation"):
        withID = queryParams["ExtraInformation"].lower() == "id"
    else:
        withID = False

    if queryParams.has_key("AddressPlaceId"):
        queryParams["AddressPlaceId"] = numberCheck(queryParams["AddressPlaceId"])
        if queryParams["AddressPlaceId"] != "":
            response = IDCheck.IDCheckServiceHandler(queryParams, response, builder)
        else:
            response.html = ""
            response.handled = True
            response.mimeFormat = builder.getMimeFormat()
        return response

    elif queryParams.has_key("SearchText"):
        s = fulltextsearch.searchAddress(builder, None, queryParams["SearchText"], withID)
        response.htmlData = s

    else:
        doValidate = p("Validate", "true").lower() == "true"
        s = compileAddress(
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
            doValidate,
            withID
        )
        response.htmlData = builder.listToResponseText([s])
    response.handled = True
    return response

def createServiceHandlers():
    services.append(
        WebService("/CompileAddress", u"Sestavení adresy", u"Formátování adresy ve standardizovaném tvaru",
            u"""Umožňuje sestavit zápis adresy ve standardizovaném tvaru podle § 6 vyhlášky č. 359/2011 Sb.,
            kterou se provádí zákon č. 111/2009 Sb., o základních registrech, ve znění zákona č. 100/2010 Sb.
            Adresní místo lze zadat buď pomocí jeho identifikátoru RÚIAN, textového řetězce adresy nebo jednotlivých prvků adresy.""",
            [
                getResultFormatParam()
            ],
            [
                getAddressPlaceIdParamURL(),
                getSearchTextParam(),
                URLParam("Locality",          u"Obec",  u"Obec", "", True, htmlTags = ' class="RUIAN_TOWN_INPUT" '),
                URLParam("LocalityPart",      u"Část obce", u"Část obce, pokud je známa", "", True, htmlTags = ' class="RUIAN_TOWNPART_INPUT" '),
                getDistrictNumberURL(False),
                URLParam("Street",            u"Ulice", u"Název ulice", "", True, htmlTags = ' class="RUIAN_STREET_INPUT" '),
                getHouseNumberURL(),
                getRecordNumberURL(),
                getOrientationNumberURL(),
                getOrientationNumberCharacterURL(),
                getZIPCodeURL(),
                URLParam("ExtraInformation",  u"Další informace", u"Vypíše zvolený druh dodatečných informací", "", False),
                URLParam("FillAddressButton",  u"Doplň adresu", u"Najde v databázi adresu odpovídající vyplněným hodnotám", "", True)
            ],
            compileAddressServiceHandler,
            sendButtonCaption = u"Sestav adresu",
            htmlInputTemplate = '''<select>
                                        <option value="text">text</option>
                                        <option value="xml">xml</option>
                                        <option value="html">html</option>
                                        <option value="json">json</option>
                                    </select>'''
        )
    )

if __name__ == '__main__':
    import sharedtools.base
    sharedtools.base.setupUTF()
    #print compileAddress(None, u"Mrkvičkova", u"1370", "", "", "", "", "", "", "")
    print compileAddress(MimeBuilder("texttoonerow"), u"", u"14", "", "", "", "", "", "Stará Chodovská", "")

