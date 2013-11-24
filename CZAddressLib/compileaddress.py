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

def errorMessage(msg):
    pass

class TextFormat:
    plainText = 0
    xml       = 1
    json      = 2
    html      = 3

def formatZIPCode(code):
    code = code.replace(" ", "")
    code = code[:3] + " " + code[3:]
    return code

def compileAddress(resultFormat, street, houseNumber, recordNumber, orientationNumber, zipCode, locality, localityPart, districtNumber):
    """
        @param street            string  Název ulice
        @param locality          string  Obec
        @param houseNumber       number  Číslo popisné
        @param zipCode           number  Poštovní směrovací číslo
        @param localityPart      string  Část obce, pokud je známa
        @param orientationNumber number  Číslo orientační
    """
    lines = []
    zipCode = formatZIPCode(zipCode)
    townInfo = zipCode + " " + locality + " " + districtNumber

    if houseNumber != "":
        houseNumberStr = " " + houseNumber
        if orientationNumber != "":
            houseNumberStr += u"/" + orientationNumber
    elif recordNumber != "":
        houseNumberStr = u" č. ev. " + recordNumber
    else:
        houseNumberStr = ""

    if locality.upper() == "PRAHA":
        if street != "":
            lines.append(street + houseNumberStr)
            lines.append(localityPart)
            lines.append(townInfo)
        else:
            lines.append(localityPart + houseNumberStr)
            lines.append(townInfo)
    else:
        if street != "":
            lines.append(street + houseNumberStr)
            if localityPart != locality:
                lines.append(localityPart)
            lines.append(townInfo)
        else:
            pass

        pass

    textDict = {
      "address" : "\n".join(lines)
    }
    builder = MimeBuilder(resultFormat)
    return builder.dictToResponseText(textDict)

def compileAddressServiceHandler(queryParams, response):

    def p(name, defValue = ""):
        if queryParams.has_key(name):
            return queryParams[name]
        else:
            return defValue

    s = compileAddress(
        p("Format", "xml"),
        p("Street"),
        p("HouseNumber"),
        p("RecordNumber"),
        p("OrientationNumber"),
        p("ZIPCode"),
        p("Locality"),
        p("LocalityPart"),
        p("DistrictNumber")
    )
    response.htmlData = s
    response.mimeFormat = getMimeFormat(p("Format", "xml"))
    response.handled = True
    return response

def createServiceHandlers():
    services.append(
        WebService("/CompileAddress", u"Sestavení adresy", u"Formátování adresy ve standardizovaném tvaru",
            u"""Tato webová služba sestavit zápis adresy ve standardizovaném tvaru podle § 6 vyhlášky č. 359/2011 Sb.,
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
                URLParam("RecordNumber",      u"Číslo evidenční", u"Číšlo evidenční, pokud je přiděleno"),
                URLParam("DistrictNumber",    u"Obvod", u"Číšlo městského obvodu, pokud exituje")
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