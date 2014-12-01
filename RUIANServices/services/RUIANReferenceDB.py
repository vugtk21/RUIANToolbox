#!C:/Python27/python.exe
# -*- coding: utf-8 -*-

__author__ = 'Liska'

from RUIANConnection import *

database = {
            "12351": Locality(Address(u"Arnošta Valenty", u"670", u"", u"31", u"19800", u"Praha", u"Černý Most", u"9"), Coordinates(0,0)),
            "12353": Locality(Address(u"Medová", u"", u"30", u"", u"10400", u"Praha", u"Křeslice", u"10"), Coordinates(100,100)),
            "12355": Locality(Address(u"Lhenická", u"1120", u"", u"1", u"37005", u"České Budějovice", u"České Budějovice 2", u""), Coordinates(80,70)),
            "12356": Locality(Address(u"Lhenická", u"1120", u"", u"", u"37005", u"České Budějovice", u"České Budějovice 2", u""), Coordinates(0,100)),
            "12358": Locality(Address(u"Žamberecká", u"339", u"", u"", u"51601", u"Vamberk", u"Vamberk", u""), Coordinates(200,100)),
            "12361": Locality(Address(u"", u"106", u"", u"", u"53333", u"Pardubice", u"Dražkovice", u""), Coordinates(120,180)),
            "12364": Locality(Address(u"", u"111", u"", u"", u"50333", u"Praskačka", u"Praskačka", u""), Coordinates(130,120)),
            }

def _findCoordinates(AddressID):
    for id, location in database.iteritems():
        if id == AddressID:
            return Coordinates(str(location.coordinates.JTSKY), str(location.coordinates.JTSKX))


def _findAddress(ID):
    if ID in database.keys():
        location = database[ID]
        return location.address

def _findCoordinatesByAddress(dict):
    coordinates = []
    for id, location in database.iteritems():
        if (dict["street"].lower() == location.address.street.lower() or dict["street"] == "") and (dict["houseNumber"] == location.address.houseNumber or dict["houseNumber"] == "") \
                and (dict["recordNumber"] == location.address.recordNumber or dict["recordNumber"] == "") and (dict["orientationNumber"] == location.address.orientationNumber or dict["orientationNumber"] == "") \
                and (dict["zipCode"] == location.address.zipCode or dict["zipCode"] == "") and (dict["locality"].lower() == location.address.locality.lower() or dict["locality"] == "") \
                and (dict["localityPart"] == location.address.localityPart or dict["localityPart"] == "") and (dict["districtNumber"] == location.address.districtNumber or dict["districtNumber"] == ""):
            coordinates.append(Coordinates(str(location.coordinates.JTSKY), str(location.coordinates.JTSKX)))
    return coordinates

def _getNearbyLocalities(x,y,MaxDistance):
    addresses = []
    for id, location in database.iteritems():
        RealDistance = ((float(x)-float(location.coordinates.JTSKX)) ** 2 +(float(y)-float(location.coordinates.JTSKY)) ** 2) ** 0.5
        if RealDistance < float(MaxDistance):
            addresses.append(location.address)
    return addresses

def _validateAddress(dict):
    for id, location in database.iteritems():
        if (dict["street"].lower() == location.address.street.lower()) and (dict["houseNumber"] == location.address.houseNumber) \
                and (dict["recordNumber"] == location.address.recordNumber) and (dict["orientationNumber"] == location.address.orientationNumber) \
                and (dict["zipCode"] == location.address.zipCode) and (dict["locality"].lower() == location.address.locality.lower()) \
                and (dict["localityPart"] == location.address.localityPart) and (dict["districtNumber"] == location.address.districtNumber):
            return True
    return False

def _getRUIANVersionDate():
    return "unassigned RUIAN Version"

def _saveRUIANVersionDateToday():
    pass

def _getDBDetails():
    return "getDBDetails() not implemented."

def _getTableNames():
    return ""
