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
__author__ = 'Radek Augustýn'

import codecs
from HTTPShared import *
import urllib
import IDCheck
import fulltextsearch

def errorMessage(msg):
    pass

class TextFormat:
    plainText = 0
    xml       = 1
    json      = 2
    html      = 3

def compileAddress(builder, street, houseNumber, recordNumber, orientationNumber, orientationNumberCharacter, zipCode, locality, localityPart, districtNumber):
    """
        @param street            string  Název ulice
        @param locality          string  Obec
        @param houseNumber       number  Číslo popisné
        @param zipCode           number  Poštovní směrovací číslo
        @param localityPart      string  Část obce, pokud je známa
        @param orientationNumber number  Číslo orientační
        @param orientationNumberCharacter string  Písmeno čísla orientačního
    """

    if builder.formatText == "json":
        return compileAddressAsJSON(street, houseNumber, recordNumber, orientationNumber, orientationNumberCharacter, zipCode, locality, localityPart, districtNumber)

    elif builder.formatText == "xml":
        return compileAddressAsXML(street, houseNumber, recordNumber, orientationNumber, orientationNumberCharacter, zipCode, locality, localityPart, districtNumber)

    elif builder.formatText == "texttoonerow" or builder.formatText == "htmltoonerow":
        return compileAddressToOneRow(street, houseNumber, recordNumber, orientationNumber, orientationNumberCharacter, zipCode, locality, localityPart, districtNumber)

    else:
        return builder.listToResponseText(compileAddressAsText(street, houseNumber, recordNumber, orientationNumber, orientationNumberCharacter, zipCode, locality, localityPart, districtNumber))

def compileAddressServiceHandler(queryParams, response):

    def p(name, defValue = ""):
        if queryParams.has_key(name):
            a = urllib.unquote(queryParams[name])
            #a = a.replace("%u017E",u"ž")
            #return mapping(a)
            return urllib.unquote(queryParams[name]) #decode("utf-8"))
        else:
            return defValue

    resultFormat = p("Format", "text")
    builder = MimeBuilder(resultFormat)
    response.mimeFormat = builder.getMimeFormat()

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
        if queryParams.has_key("ExtraInformation"):
            withID = queryParams["ExtraInformation"].lower() == "id"
        else:
            withID = False
        s = fulltextsearch.searchAddress(builder, None, queryParams["SearchText"], withID)
        response.htmlData = s

    else:
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
            p("DistrictNumber")
        )
        response.htmlData = builder.listToResponseText([s])
    #response.mimeFormat = builder.getMimeFormat() #getMimeFormat(p("Format", "xml"))
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
                URLParam("Street",            u"Ulice", u"Název ulice", "", True),
                URLParam("HouseNumber",       u"Číslo popisné", "", "", True),
                URLParam("RecordNumber",      u"Číslo evidenční", u"Číslo evidenční, pokud je přiděleno", "", True),
                URLParam("OrientationNumber", u"Číslo orientační", "", "", True, htmlTags=' pattern="[0-9]"'),
                URLParam("OrientationNumberCharacter", u"Písmeno čísla<br>orientačního", "", "", True),
                URLParam("ZIPCode",           u"PSČ", u"Poštovní směrovací číslo", "", True),
                URLParam("Locality",          u"Obec",  u"Obec", "", True),
                URLParam("LocalityPart",      u"Část obce", u"Část obce, pokud je známa", "", True),
                URLParam("DistrictNumber",    u"Číslo městského<br>obvodu v Praze", u"Číslo městského obvodu, pokud existuje", "", True),
                URLParam("ExtraInformation", u"Další informace", u"Vypíše zvolený druh dodatečných informací", "", False)
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
    import compileaddress_UnitTests
    compileaddress_UnitTests.main()