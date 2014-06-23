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

def formatZIPCode(code):
    code = code.replace(" ", "")
    if code.isdigit():
        return code
    else:
        return ""

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
        if houseNumber != "":
            sign = u"č.p."
            addressNumber = houseNumber
        else:
            sign = u"č.ev."
            addressNumber = recordNumber

        if orientationNumber != "":
            houseNumberStr = '\t"' + sign +'": ' + addressNumber + ',\n\t"orientační_číslo": ' + orientationNumber + orientationNumberCharacter + ','
        else:
            houseNumberStr ='\t"' + sign +'": ' + addressNumber + ','

        if street != "":
            street = '\t"ulice": ' + street + ",\n"

        if districtNumber != "":
            districtNumberStr = ',\n\t"číslo_městského_obvodu": ' + districtNumber
        else:
            districtNumberStr = ""

        if locality == localityPart or localityPart == "":
            townDistrict = '\t"obec": ' + locality + districtNumberStr
        else:
            townDistrict = '\t"obec": ' + locality + districtNumberStr + ',\n\t"část_obce": ' + localityPart


        result = street + houseNumberStr + '\n\t"PSČ" :' + zipCode + ",\n" + townDistrict + "\n"
        return result

    elif builder.formatText == "xml":
        if houseNumber != "":
            sign = "c.p."
            addressNumber = houseNumber
        else:
            sign = "c.ev."
            addressNumber = recordNumber

        if orientationNumber != "":
            houseNumberStr = '\t<' + sign +'>' + addressNumber + '</' + sign +'>\n\t<orientacni_cislo>' + orientationNumber + orientationNumberCharacter + '</orientacni_cislo>'
        else:
            houseNumberStr ='\t<' + sign +'>' + addressNumber + '</' + sign +'>'

        if street != "":
            street = '\t<ulice>' + street + "</ulice>\n"

        if districtNumber != "":
            districtNumberStr = '\n\t<cislo_mestskeho_obvodu>' + districtNumber + '</cislo_mestskeho_obvodu>'
        else:
            districtNumberStr = ""

        if locality == localityPart or localityPart == "":
            townDistrict = '\t<obec>' + locality + "</obec>" + districtNumberStr
        else:
            townDistrict = '\t<obec>' + locality + '</obec>' + districtNumberStr + '\n\t<cast_obce>' + localityPart + '</cast_obce>'

        result = street + houseNumberStr + '\n\t<PSC>' + zipCode + "</PSC>\n" + townDistrict + "\n"
        return result

    lines = []
    zipCode = formatZIPCode(zipCode)
    houseNumber = numberCheck(houseNumber)
    orientationNumber = numberCheck(orientationNumber)
    districtNumber = numberCheck(districtNumber)
    orientationNumberCharacter = alphaCheck(orientationNumberCharacter)

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
        queryParams["AddressPlaceId"] = numberCheck(queryParams["AddressPlaceId"])
        if queryParams["AddressPlaceId"] != "":
            response = IDCheck.IDCheckServiceHandler(queryParams, response, builder)
        else:
            response.html = ""
            response.handled = True
            response.mimeFormat = builder.getMimeFormat()
        return response

    elif queryParams.has_key("SearchText"):
        withID = queryParams["SuppressID"].lower() == "id"
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
                URLParam("OrientationNumber", u"Číslo orientační", "", "", True),
                URLParam("OrientationNumberCharacter", u"Písmeno čísla<br>orientačního", "", "", True),
                URLParam("ZIPCode",           u"PSČ", u"Poštovní směrovací číslo", "", True),
                URLParam("Locality",          u"Obec",  u"Obec", "", True),
                URLParam("LocalityPart",      u"Část obce", u"Část obce, pokud je známa", "", True),
                URLParam("DistrictNumber",    u"Číslo městského<br>obvodu v Praze", u"Číslo městského obvodu, pokud existuje", "", True),
                URLParam("SuppressID",        u"Potlač identifikátor", u"Nevypíše identifikátor RÚIAN při více než jednom nalezeném záznamu", "", False)
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