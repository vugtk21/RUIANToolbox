#!C:/Python27/python.exe
# -*- coding: utf-8 -*-

__author__ = 'Liska'
from HTTPShared import *

import RUIANConnection

import compileaddress
import sharetools

def IDCheckServiceHandler(queryParams, response, builder):
    response.mimeFormat = builder.getMimeFormat()
    address = RUIANConnection.findAddress(sharetools.getKeyValue(queryParams, "AddressPlaceId"))
    response.handled = True
    if not address:
        return response

    #if address.districtNumber != "":
    #    district = address.districtNumber.split(" ")
    #    districtNumber = district[1]
    #else:
    #    districtNumber = ""
    html = compileaddress.compileAddress(builder, address.street, address.houseNumber, address.recordNumber, address.orientationNumber, address.orientationNumberCharacter, address.zipCode, address.locality, address.localityPart, address.districtNumber)
    response.htmlData = builder.listToResponseText([html])
    return response