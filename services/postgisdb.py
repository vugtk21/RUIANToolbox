__author__ = 'Augustyn'

DATABASE_HOST = "192.168.1.93"
PORT = "5432"
DATABSE_NAME = "adresni_misto"
USER_NAME = "postgres"
PASSWORD = "postgres"

ITEM_TO_DBFIELDS = {
    "street": "nazev_ulice"


}

def _findAddress(ID, builder):
    return None

def _getNearbyLocalities(x,y,distance):
    return None

def _validateAddress(street, houseNumber, recordNumber, orientationNumber, zipCode, locality, localityPart, districtNumber):
    return None

def _findID():
    return None
