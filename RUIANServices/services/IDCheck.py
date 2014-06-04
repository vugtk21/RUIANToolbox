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
    if address:
        response.handled = True
    else:
        response.handled = False
        return response
    response.htmlData = compileaddress.compileAddress(builder, address.street, address.houseNumber, address.recordNumber, address.orientationNumber, address.zipCode, address.locality, address.localityPart, address.districtNumber)
    return response