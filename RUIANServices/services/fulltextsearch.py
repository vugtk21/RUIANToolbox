# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
# Name:        compileaddress
# Purpose:
#
# Author:      Radek Augustýn
#
# Created:     13/11/2013
# Copyright:   (c) Radek Augustýn 2013
# Licence:     <your licence>
# -------------------------------------------------------------------------------

from HTTPShared import *
import parseaddress

def searchAddress(builder, searchFlag, searchText, withID=True):
    parser = parseaddress.AddressParser()
    candidates = parser.fullTextSearchAddress(searchText)
    items = parser.buildAddress(builder, candidates, withID)
    s = builder.listToResponseText(items, recordSeparator=builder.recordSeparator)
    return s


def searchAddressServiceHandler(queryParams, response):
    builder = MimeBuilder(queryParams["Format"])
    response.mimeFormat = builder.getMimeFormat()
    if queryParams.has_key("ExtraInformation"):
        withID=queryParams["ExtraInformation"] == "id"
    else:
        withID=False

    #searchText = p(queryParams, "SearchText")
    #searchText = queryParams[name]
    s = searchAddress(
        builder,
        p(queryParams, "SearchFlag"),
        p(queryParams, "SearchText"),
        withID
    )
    response.htmlData = s
    response.handled = True
    return response

def createServiceHandlers():
    services.append(
        WebService("/FullTextSearch", u"Fulltextové vyhledávání", u"Vyhledávání adresního místa podle řetězce",
            u"""Umožňuje nalézt a zobrazit seznam pravděpodobných adres na základě textového řetězce adresy.
            Textový řetězec adresy může být nestandardně formátován nebo může být i neúplný.""",
            [getResultFormatParam()],
            [
                getSearchTextParam(),
                URLParam("ExtraInformation", u"Další informace", u"Vypíše zvolený druh dodatečných informací", "", False)
            ],
            searchAddressServiceHandler,
            sendButtonCaption=u"Vyhledej adresu",
            htmlInputTemplate=''
        )
    )