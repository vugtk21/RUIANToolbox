#!C:/Python27/python.exe
# -*- coding: utf-8 -*-

__author__ = 'Liska'

from HTTPShared import *
import RUIANInterface

def IDCheckServiceHandler(queryParams, response):
    builder = MimeBuilder(queryParams["Format"])
    response.htmlData = RUIANInterface.FindAddress(queryParams["AddressPlaceId"], builder)
    response.mimeFormat = builder.getMimeFormat()
    response.handled = True
    return response

def createServiceHandlers():
    services.append(
        WebService("/IDCheck", u"Vyhledání adresy", u"Vyhledání adresy podle ID",
            u"""Umožňuje sestavit zápis adresy ve standardizovaném tvaru podle § 6 vyhlášky č. 359/2011 Sb.,
            kterou se provádí zákon č. 111/2009 Sb., o základních registrech, ve znění zákona č. 100/2010 Sb.
            Adresní místo lze zadat buď pomocí jeho identifikátoru RÚIAN, textového řetězce adresy nebo jednotlivých prvků adresy.""",
            [
                getResultFormatParam()
            ],
            [
                getAddressPlaceIdParamURL()
            ],
            IDCheckServiceHandler,
            sendButtonCaption = u"Najdi adresu",
            htmlInputTemplate = '''<select>
                                        <option value="text">text</option>
                                        <option value="xml">xml</option>
                                        <option value="html">html</option>
                                        <option value="json">json</option>
                                    </select>'''
        )
    )