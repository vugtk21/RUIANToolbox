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
import re

char_mapping = {'%E1':u'á','%E4':u'ä','%u010D':u'č','%u010F':u'ď','%E9':u'é','%u011B':u'ě','%ED':u'í','%u013A':u'ĺ',
'%u013E':u'ľ','%F3':u'ó','%F4':u'ô','%u0155':u'ŕ','%u0159':u'ř','%u0161':u'š','%u0165':u'ť','%FA':u'ú','%u016F':u'ů',
u'%u017E':u"\u017E",'%C1':u'Á','%E4':u'Ä','%u010C':u'Č','%u010E':u'Ď','%C9':u'É','%u011A':u'Ě','%u0139':u'Ĺ','%u013D':u'Ľ','%D3':u'Ó',
'%F4':u'Ô','%u0154':u'Ŕ','%u0158':u'Ř','%u0160':u'Š','%u0164':u'Ť','%DA':u'Ú','%u016E':u'Ů','%u017D':u'Ž'}

def mapping(str):
    """
    Returns mapping function for given mapping dict
    """
    for key in char_mapping.keys():
        if key in str:
            str.replace(key, char_mapping[key])
            print char_mapping[key]
            print str
    return str

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
    townInfo = zipCode + " " + locality#unicode(locality, "utf-8")
    if districtNumber != "":
        townInfo += " " + districtNumber

    if houseNumber != "":
        houseNumberStr = " " + houseNumber
        if orientationNumber != "":
            houseNumberStr += u"/" + orientationNumber
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
    builder = MimeBuilder(resultFormat)
    return builder.listToResponseText(lines)

def compileAddressServiceHandler(queryParams, response):

    def p(name, defValue = ""):
        if queryParams.has_key(name):
            a = urllib.unquote(queryParams[name])
            #a = a.replace("%u017E",u"ž")
            return mapping(a)
            #return (urllib.unquote(queryParams[name]).decode("utf-8"))
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