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

def errorMessage(msg):
    pass

class TextFormat:
    plainText = 0
    xml       = 1
    json      = 2
    html      = 3

def formatZIPCode(code):
    code = code.replace(" ", "")
    #code = code[:3] + " " + code[3:]
    return code

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
    lines = []
    zipCode = formatZIPCode(zipCode)
    townInfo = zipCode + " " + locality#unicode(locality, "utf-8")
    if districtNumber != "":
        townInfo += " " + districtNumber

    if houseNumber != "":
        houseNumberStr = " " + houseNumber
        if orientationNumber != "":
            houseNumberStr += u"/" + orientationNumber + orientationNumberCharacter
    elif recordNumber != "":
        houseNumberStr = u" č.ev. " + recordNumber
    else:
        houseNumberStr = ""

    if locality.upper() == "PRAHA":
        if street != "":
            lines.append(street + houseNumberStr)#(unicode(street, "utf-8") + houseNumberStr)
            lines.append(localityPart)#(unicode(localityPart, "utf-8"))
            lines.append(townInfo)
        else:
            lines.append(localityPart + houseNumberStr)#(unicode(localityPart, "utf-8") + houseNumberStr)
            lines.append(townInfo)
    else:
        if street != "":
            lines.append(street + houseNumberStr)#(unicode(street, "utf-8") + houseNumberStr)
            if localityPart != locality:
                lines.append(localityPart)#(unicode(localityPart, "utf-8"))
            lines.append(townInfo)
        else:
            if localityPart != locality:
                lines.append(localityPart + houseNumberStr)#(unicode(localityPart, "utf-8") + houseNumberStr)
            else:
                if houseNumber != "":
                    lines.append(u"č.p."+houseNumberStr)
                else:
                    lines.append(houseNumberStr[1:])
            lines.append(townInfo)
        pass

    #textDict = {
    #  "address" : "\n".join(lines)
    #}
    return builder.listToResponseText(lines)

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
        response = IDCheck.IDCheckServiceHandler(queryParams, response, builder)
        return response

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
    response.htmlData = s
    response.mimeFormat = builder.getMimeFormat() #getMimeFormat(p("Format", "xml"))
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