#!C:/Python27/python.exe
# -*- coding: utf-8 -*-

__author__ = 'Liska'

import RUIANInterface

class Coordinates:
    def __init__(self, JTSKY, JTSKX):
        self.JTSKX = JTSKX
        self.JTSKY = JTSKY

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

class Locality:
    def __init__(self,address, coordinates):
        self.address=address
        self.coordinates=coordinates

database = {
            "12351": Locality(Address(u"Arnošta Valenty", u"670", u"", u"31", u"19800", u"Praha", u"Černý Most", u"9"), Coordinates(0,0)),
            "12353": Locality(Address(u"Medová", u"", u"30", u"", u"10400", u"Praha", u"Křeslice", u"10"), Coordinates(100,100)),
            "12355": Locality(Address(u"Lhenická", u"1120", u"", u"1", u"37005", u"České Budějovice", u"České Budějovice 2", u""), Coordinates(80,70)),
            "12356": Locality(Address(u"Lhenická", u"1120", u"", u"", u"37005", u"České Budějovice", u"České Budějovice 2", u""), Coordinates(0,100)),
            "12358": Locality(Address(u"Žamberecká", u"339", u"", u"", u"51601", u"Vamberk", u"Vamberk", u""), Coordinates(200,100)),
            "12361": Locality(Address(u"", u"106", u"", u"", u"53333", u"Pardubice", u"Dražkovice", u""), Coordinates(120,180)),
            "12364": Locality(Address(u"", u"111", u"", u"", u"50333", u"Praskačka", u"Praskačka", u""), Coordinates(130,120)),
            }


def FindAddress(ID, builder):
    if ID in database.keys():
        location = database[ID]
        return location.address
    """    lines = [u"Lhenická 1120/1",u"České Budějovice 2",u"37005 České Budějovice"]
    else:
        lines = []
    return builder.listToResponseText(lines)
    """

def GetNearbyLocalities(x,y,MaxDistance):
    localities = []
    for id, location in database.iteritems():
        RealDistance = ((float(x)-float(location.coordinates.JTSKX)) ** 2 +(float(y)-float(location.coordinates.JTSKY)) ** 2) ** 0.5
        if RealDistance < float(MaxDistance):
            localities.append(location)
    return localities

def ValidateAddress(street, houseNumber, recordNumber, orientationNumber, zipCode, locality, localityPart, districtNumber):
    for id, location in database.iteritems():
        if (street.lower() == location.address.street.lower()) and (houseNumber == location.address.houseNumber) \
                and (recordNumber == location.address.recordNumber) and (orientationNumber == location.address.orientationNumber) \
                and (zipCode == location.address.zipCode) and (locality.lower() == location.address.locality.lower()) \
                and (localityPart == location.address.localityPart) and (districtNumber == location.address.districtNumber):
            return True
    return False

RUIANInterface.FindAddress = FindAddress
RUIANInterface.GetNearbyLocalities = GetNearbyLocalities
RUIANInterface.ValidateAddress = ValidateAddress
