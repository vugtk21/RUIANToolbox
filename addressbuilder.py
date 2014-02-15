# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        addressbuilder
# Purpose:     Formátuje adresu ve standardizovaném tvaru
#
# Author:      Radek Augustýn
#
# Created:     14/02/2014
# Copyright:   (c) Radek Augustýn 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------
__author__ = 'raugustyn'

class TextFormater:
    def __init__(self, lineSeparator="<br>"):
        self.lineSeparator = lineSeparator
        self.text = u""
        pass

    def clear(self):
        self.text = u""
        pass

    def addLine(self, line: str):
        if self.text != "":
            self.text += self.lineSeparator
        self.text += line

def spaceToCamelCase(value : str):
    output = ""
    for word in value.split(" "):
        if output != "":
            output += " "
        output += word[0:1].upper() + word[1:].lower()
    return output


class Address:
    PRAHA_NAME = 'praha'

    def __init__(self, **kwargs):
        self.street = kwargs.get("street", "")
        self.descNumber = kwargs.get("descNumber", "")
        self.recordNumber = kwargs.get("recordNumber", "")
        self.orientationNumber = kwargs.get("orientationNumber", "")
        self.ZIPCode = kwargs.get("ZIPCode", "")
        self.town = kwargs.get("town", "") # @TODO Velka pismena ve viceslovnem nazvu mesta
        self.districtNumber = kwargs.get("districtNumber", "")
        self.district = kwargs.get("district", "")
        pass

    def getNormalizedZIPCode(self):
        """ Odstraní mezery ze zápisu PSČ """
        return self.ZIPCode.replace(" ", "")

    def getNormalizedTownName(self):
        """ První písmena ve slovech velká """
        return spaceToCamelCase(self.town)

    def getNormalizedDistrictName(self):
        """ První písmena ve slovech velká """
        return spaceToCamelCase(self.district)

    def toAddressString(self, formater : TextFormater):
        """ Naformátuje a vrátí standardizovaný adresní řetězec """
        formater.clear()

        # 1. Adresní místo v Praze s ulicí, číslem popisným a orientačním
        if self.town.lower() == self.PRAHA_NAME and self.descNumber != "" and self.orientationNumber != "":
            formater.addLine("%s %s/%s" % (self.street, self.descNumber, self.orientationNumber))
            formater.addLine(self.getNormalizedDistrictName())
            formater.addLine("%s %s %s" % (self.getNormalizedZIPCode(), self.getNormalizedTownName(), self.districtNumber))

        # 2. Adresní místo v Praze s ulicí a číslem popisným
        if self.town.lower() == self.PRAHA_NAME and self.descNumber != "" and self.orientationNumber == "":
            formater.addLine("%s %s" % (self.street, self.descNumber))
            formater.addLine(self.getNormalizedDistrictName())
            formater.addLine("%s %s %s" % (self.getNormalizedZIPCode(), self.getNormalizedTownName(), self.districtNumber))

        # 3. Adresní místo v Praze s ulicí a číslem evidenčním
        if self.town.lower() == self.PRAHA_NAME and self.street != "" and self.recordNumber != "":
            formater.addLine("%s č. ev. %s" % (self.street, self.recordNumber))
            formater.addLine(self.getNormalizedDistrictName())
            formater.addLine("%s %s %s" % (self.getNormalizedZIPCode(), self.getNormalizedTownName(), self.districtNumber))

        # 4. Adresní místo v Praze s číslem evidenčním
        if self.town.lower() == self.PRAHA_NAME and self.street == "" and self.recordNumber != "":
            formater.addLine("%s č. ev. %s" % (self.getNormalizedDistrictName(), self.recordNumber))
            formater.addLine("%s %s %s" % (self.getNormalizedZIPCode(), self.getNormalizedTownName(), self.districtNumber))

        return formater.text

def getAddressFromStr(s : str):

    pass

def main():
    s = Address(street = "ulice")
    pass

if __name__ == '__main__':
    main()