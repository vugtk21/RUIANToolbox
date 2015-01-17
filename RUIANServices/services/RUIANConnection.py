__author__ = 'Augustyn'

class Coordinates:
    def __init__(self, JTSKY, JTSKX):
        self.JTSKX = JTSKX
        self.JTSKY = JTSKY

class Address:
    def __init__(self,street, houseNumber, recordNumber, orientationNumber, orientationNumberCharacter, zipCode, locality, localityPart, districtNumber):
        self.street = street
        self.houseNumber = houseNumber
        self.recordNumber = recordNumber
        self.orientationNumber = orientationNumber
        self.orientationNumberCharacter = orientationNumberCharacter
        self.zipCode = zipCode
        self.locality = locality
        self.localityPart = localityPart
        self.districtNumber = districtNumber

class Locality:
    def __init__(self,address, coordinates):
        self.address=address
        self.coordinates=coordinates

if (False):
    from RUIANReferenceDB import _findAddress, _getNearbyLocalities, _validateAddress, _findCoordinates, \
         _findCoordinatesByAddress, _getRUIANVersionDate, _saveRUIANVersionDateToday, _getDBDetails, _getTableNames
else:
    from postgisdb import _findAddress, _getNearbyLocalities, _validateAddress, _findCoordinates, \
         _findCoordinatesByAddress, _getRUIANVersionDate, _saveRUIANVersionDateToday, _getDBDetails, _getTableNames, _getAddresses


findAddress = _findAddress
getNearbyLocalities = _getNearbyLocalities
validateAddress = _validateAddress
findCoordinates = _findCoordinates
findCoordinatesByAddress = _findCoordinatesByAddress
getRUIANVersionDate = _getRUIANVersionDate
saveRUIANVersionDateToday = _saveRUIANVersionDateToday
getDBDetails = _getDBDetails
getTableNames = _getTableNames
getAddresses = _getAddresses