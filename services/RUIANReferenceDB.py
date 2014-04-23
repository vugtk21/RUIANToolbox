#!C:/Python27/python.exe
# -*- coding: utf-8 -*-

__author__ = 'Liska'

import RUIANInterface

class Address:
    def __init__(self,street, houseNumber, recordNumber, orientationNumber, zipCode, locality, localityPart, districtNumber):
        self.street = street
        self.houseNumber = houseNumber
        self.recordNumber = recordNumber
        self.orientationNumber = orientationNumber
        self.zipCode = zipCode
        self.locality = locality
        self.localityPart = localityPart
        self.districtNumber = districtNumber

database = {"12356": Address(u"Lhenická", u"1120", u"", u"1", u"37005", u"České Budějovice", u"České Budějovice 2", u"")}


def FindAddress(ID, builder):
    if ID in database.keys():
        address = database[ID]
        return address
    """    lines = [u"Lhenická 1120/1",u"České Budějovice 2",u"37005 České Budějovice"]
    else:
        lines = []
    return builder.listToResponseText(lines)
    """
RUIANInterface.FindAddress = FindAddress