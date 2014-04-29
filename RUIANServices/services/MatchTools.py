# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        MatchTools
# Purpose:
#
# Author:      Radek Augustýn
#
# Created:     13/11/2013
# Copyright:   (c) Radek Augustýn 2013
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import codecs

def saveNamesListToFile(namesList, fileName):
    print "Creating file", fileName
    file = codecs.open(fileName, "w", "utf-8")
    for name in namesList:
        file.write(name + "\n")
    file.close()

class SearchDatabase:
    TOWN_NAMES_FILENAME   = 'TownNames.txt'
    STREET_NAMES_FILENAME = 'StreetNames.txt'
    townNames = ['chodov', 'praha']
    streetNames = [u'budovatelů', u'mrkvičkova']
    ZIPCodes = ['35735', '16300']
    addressData = {
      'chodov': {
        'budovatelů' : ['676', '677', '678', '679', '680', '681']
      },
      'praha': {
        'mrkvičkova' : ['1370', '1371', '1372', '1373', '1374', '1375']
      },
    }


    def isTownName(self, value):
        return value.lower() in self.townNames

    def isStreetName(self, value):
        return value.lower() in self.streetNames

    def isZIPCode(self, value):
        return value.lower() in self.ZIPCodes

    def getTown(self, townName):
        return self.addressData[townName]

    def saveToFiles(self, path):
        saveNamesListToFile(self.townNames,   path + "\\" + self.TOWN_NAMES_FILENAME)
        saveNamesListToFile(self.streetNames, path + "\\" + self.STREET_NAMES_FILENAME)
        pass

searchDatabase = SearchDatabase()

ADDRESS_STRING_SEPARATOR = ","
CISLO_ORIENTACNI_SEPARATOR = "/"

def normalizeAddressString(addressString):
    """ Normalizuje adresní řetězec addressString """
    result = addressString
    result = result.replace("  ", " ")                         # Více mezer je chápáno jako jedna
    result = result.replace(";",  ADDRESS_STRING_SEPARATOR)    # Středník je chápán jako oddělovač čárka
    result = result.replace(":",  ADDRESS_STRING_SEPARATOR)    # Dvojtečka je chápána jako oddělovač čárka
    result = result.replace(",,", ADDRESS_STRING_SEPARATOR)    # Více čárek je chápáno jako prázdná informace
    return result

class Adresa:

    def __init__(self):
        ''' '''
        self.mesto = ""
        self.psc = ""
        self.ulice = ""
        self.cislo_domovni = ""
        self.cislo_orientacni = ""
        self.cislo_orientacni_pismeno = ""
        self.names = []
        pass

    def parseAddressString(self, addressString):
        addressString = normalizeAddressString(addressString)
        addressItems = addressString.split(ADDRESS_STRING_SEPARATOR)
        for item in addressItems:
            itemNoSpaces = item.replace(" ", "")
            if itemNoSpaces.isdigit() == True: # Číslo domovní nebo PSČ
                if len(item) == 5:
                    self.psc = item
                else:
                    self.cislo_domovni = itemNoSpaces
            else:
                separatorPos = itemNoSpaces.find(CISLO_ORIENTACNI_SEPARATOR)
                if separatorPos >= 0:
                    self.cislo_domovni = itemNoSpaces[0:separatorPos - 1]
                    self.cislo_orientacni = itemNoSpaces[separatorPos + 1:]
                else:
                    self.names.append(item)

        return True

    def matchDatabase(self):
        town = None
        for name in self.names:
            if town <> None:
                if town.has_key(name):
                    self.ulice = name
                else:
                    pass # error
            elif searchDatabase.isTownName(name):
                town = searchDatabase.getTown(name)
                self.mesto = name
            elif searchDatabase.isStreetName(name):
                self.ulice = name
            else:
                pass # error
        pass


class AdresniMisto(Adresa):

    def __init__(self):
        ''' '''
        Adresa.__init__(self)
        pass

if __name__ == '__main__':
    address = Adresa()
    address.parseAddressString("chodov, budovatelů, 677")
    address.matchDatabase()
    import MatchTools_UnitTests
    MatchTools_UnitTests.main()
    unittest.main()
