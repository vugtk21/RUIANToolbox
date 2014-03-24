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

import urllib2

class TextFormater:
    def __init__(self, lineSeparator="<br>"):
        self.lineSeparator = lineSeparator
        self.text = u""
        pass

    def clear(self):
        self.text = u""
        pass

    def addLine(self, line):
        if self.text != "":
            self.text += self.lineSeparator
        self.text += line

def spaceToCamelCase(value ):
    output = u""
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

    def toAddressString(self, formater ):
        """ Naformátuje a vrátí standardizovaný adresní řetězec """
        formater.clear()

        # 1. Adresní místo v Praze s ulicí, číslem popisným a orientačním
        if self.town.lower() == self.PRAHA_NAME and self.descNumber != "" and self.orientationNumber != "":
            formater.addLine(u"%s %s/%s" % (self.street, self.descNumber, self.orientationNumber))
            formater.addLine(self.getNormalizedDistrictName())
            formater.addLine(u"%s %s %s" % (self.getNormalizedZIPCode(), self.getNormalizedTownName(), self.districtNumber))

        # 2. Adresní místo v Praze s ulicí a číslem popisným
        if self.town.lower() == self.PRAHA_NAME and self.descNumber != "" and self.orientationNumber == "":
            formater.addLine(u"%s %s" % (self.street, self.descNumber))
            formater.addLine(self.getNormalizedDistrictName())
            formater.addLine(u"%s %s %s" % (self.getNormalizedZIPCode(), self.getNormalizedTownName(), self.districtNumber))

        # 3. Adresní místo v Praze s ulicí a číslem evidenčním
        if self.town.lower() == self.PRAHA_NAME and self.street != "" and self.recordNumber != "":
            formater.addLine(u"%s č.ev. %s" % (self.street, self.recordNumber))
            formater.addLine(self.getNormalizedDistrictName())
            formater.addLine(u"%s %s %s" % (self.getNormalizedZIPCode(), self.getNormalizedTownName(), self.districtNumber))

        # 4. Adresní místo v Praze s číslem evidenčním
        if self.town.lower() == self.PRAHA_NAME and self.street == "" and self.recordNumber != "":
            formater.addLine(u"%s č.ev. %s" % (self.getNormalizedDistrictName(), self.recordNumber))
            formater.addLine(u"%s %s %s" % (self.getNormalizedZIPCode(), self.getNormalizedTownName(), self.districtNumber))

        # 5. Adresní místo mimo Prahu s ulicí, číslem popisným a orientačním, název obce a její části nejsou shodné
        if self.town.lower() != self.PRAHA_NAME and self.street != "" and self.descNumber != "" and self.orientationNumber != "" and self.town != self.district:
            formater.addLine(u"%s %s/%s" % (self.street, self.descNumber, self.orientationNumber))
            formater.addLine(self.getNormalizedDistrictName())
            formater.addLine(u"%s %s" % (self.getNormalizedZIPCode(), self.getNormalizedTownName()))

        # 6. Adresní místo mimo Prahu s ulicí, číslem popisným, název obce a její části nejsou shodné
        if self.town.lower() != self.PRAHA_NAME and self.street != "" and self.descNumber != "" and self.orientationNumber == "" and self.town != self.district:
            formater.addLine(u"%s %s" % (self.street, self.descNumber))
            formater.addLine(self.getNormalizedDistrictName())
            formater.addLine(u"%s %s" % (self.getNormalizedZIPCode(), self.getNormalizedTownName()))

        # 7. Adresní místo mimo Prahu s ulicí a číslem evidenčním, název obce a její části nejsou shodné
        if self.town.lower() != self.PRAHA_NAME and self.street != "" and self.descNumber == "" and self.recordNumber != "" and self.orientationNumber == "" and self.town != self.district:
            formater.addLine(u"%s č.ev. %s" % (self.street, self.recordNumber))
            formater.addLine(self.getNormalizedDistrictName())
            formater.addLine(u"%s %s" % (self.getNormalizedZIPCode(), self.getNormalizedTownName()))

        # 8. Adresní místo mimo Prahu s ulicí a číslem popisným, název obce a její části jsou shodné
        if self.town.lower() != self.PRAHA_NAME and self.street != "" and self.descNumber != "" and self.recordNumber == "" and self.orientationNumber == "" and self.town == self.district:
            formater.addLine(u"%s %s" % (self.street, self.descNumber))
            formater.addLine(u"%s %s" % (self.getNormalizedZIPCode(), self.getNormalizedTownName()))

        # 9. Adresní místo mimo Prahu s ulicí, číslem popisným a orientačním, název obce a její části jsou shodné
        if self.town.lower() != self.PRAHA_NAME and self.street != "" and self.descNumber != "" and self.recordNumber == "" and self.orientationNumber != "" and self.town == self.district:
            formater.addLine(u"%s %s/%s" % (self.street, self.descNumber, self.orientationNumber))
            formater.addLine(u"%s %s" % (self.getNormalizedZIPCode(), self.getNormalizedTownName()))

        # 10. Adresní místo mimo Prahu s ulicí a číslem evidenčním, název obce a její části jsou shodné
        if self.town.lower() != self.PRAHA_NAME and self.street != "" and self.descNumber == "" and self.recordNumber != "" and self.orientationNumber == "" and self.town == self.district:
            formater.addLine(u"%s č.ev. %s" % (self.street, self.recordNumber))
            formater.addLine(u"%s %s" % (self.getNormalizedZIPCode(), self.getNormalizedTownName()))

        # 11. Adresní místo mimo Prahu s číslem popisným, název obce a její části nejsou shodné
        if self.town.lower() != self.PRAHA_NAME and self.street == "" and self.descNumber != "" and self.recordNumber == "" and self.orientationNumber == "" and self.town != self.district:
            formater.addLine(u"%s %s" % (self.getNormalizedDistrictName(), self.descNumber))
            formater.addLine(u"%s %s" % (self.getNormalizedZIPCode(), self.getNormalizedTownName()))

        # 12. Adresní místo mimo Prahu s číslem popisným a orientačním, název obce a její části nejsou shodné
        if self.town.lower() != self.PRAHA_NAME and self.street == "" and self.descNumber != "" and self.recordNumber == "" and self.orientationNumber != "" and self.town != self.district:
            formater.addLine(u"%s %s/%s" % (self.getNormalizedDistrictName(), self.descNumber, self.orientationNumber))
            formater.addLine(u"%s %s" % (self.getNormalizedZIPCode(), self.getNormalizedTownName()))

        # 13. Adresní místo mimo Prahu s číslem evidenčním, název obce a její části nejsou shodné
        if self.town.lower() != self.PRAHA_NAME and self.street == "" and self.descNumber == "" and self.recordNumber != "" and self.orientationNumber == "" and self.town != self.district:
            formater.addLine(u"%s č.ev. %s" % (self.getNormalizedDistrictName(), self.recordNumber))
            formater.addLine(u"%s %s" % (self.getNormalizedZIPCode(), self.getNormalizedTownName()))

        # 14. Adresní místo mimo Prahu s číslem popisným, název obce a její části jsou shodné
        if self.town.lower() != self.PRAHA_NAME and self.street == "" and self.descNumber != "" and self.recordNumber == "" and self.orientationNumber == "" and self.town == self.district:
            formater.addLine(u"č.p. %s" % (self.descNumber))
            formater.addLine(u"%s %s" % (self.getNormalizedZIPCode(), self.getNormalizedTownName()))

        # 15. Adresní místo mimo Prahu s číslem popisným a orientačním, název obce a její části jsou shodné
        if self.town.lower() != self.PRAHA_NAME and self.street == "" and self.descNumber != "" and self.recordNumber == "" and self.orientationNumber != "" and self.town == self.district:
            formater.addLine(u"č.p. %s/%s" % (self.descNumber, self.orientationNumber))
            formater.addLine(u"%s %s" % (self.getNormalizedZIPCode(), self.getNormalizedTownName()))

        # 16. Adresní místo mimo Prahu s číslem evidenčním, název obce a její části jsou shodné
        if self.town.lower() != self.PRAHA_NAME and self.street == "" and self.descNumber == "" and self.recordNumber != "" and self.orientationNumber == "" and self.town == self.district:
            formater.addLine(u"č.ev. %s" % (self.recordNumber))
            formater.addLine(u"%s %s" % (self.getNormalizedZIPCode(), self.getNormalizedTownName()))

        return formater.text

    def toRestString(self):
        # 1. Adresní místo v Praze s ulicí, číslem popisným a orientačním
        if self.town.lower() == self.PRAHA_NAME and self.descNumber != "" and self.orientationNumber != "":
            url = u"http://192.168.1.130:8080/CompileAddress/HTML?AddressPlaceId=&SearchText=&Street=%s&Locality=%s&HouseNumber=%s&ZIPCode=%s&LocalityPart=%s&OrientationNumber=%s&RecordNumber=%s&DistrictNumber=%s" % (self.street, self.getNormalizedTownName(),self.descNumber,self.getNormalizedZIPCode(),self.getNormalizedDistrictName(), self.orientationNumber, self.recordNumber, self.districtNumber)
            #url = u"http://www.vugtk.cz/euradin/services/rest.py/CompileAddress/HTML?AddressPlaceId=&SearchText=&Street=%s&Locality=%s&HouseNumber=%s&ZIPCode=%s&LocalityPart=%s&OrientationNumber=%s&RecordNumber=%s&DistrictNumber=%s" % (self.street, self.getNormalizedTownName(),self.descNumber,self.getNormalizedZIPCode(),self.getNormalizedDistrictName(), self.orientationNumber, self.recordNumber, self.districtNumber)
            url = url.replace(" ", "%20")
            html = urllib2.urlopen(url.encode('utf-8')).read()
            return html

        # 2. Adresní místo v Praze s ulicí a číslem popisným
        if self.town.lower() == self.PRAHA_NAME and self.descNumber != "" and self.orientationNumber == "":
            url = u"http://192.168.1.130:8080/CompileAddress/HTML?AddressPlaceId=&SearchText=&Street=%s&Locality=%s&HouseNumber=%s&ZIPCode=%s&LocalityPart=%s&OrientationNumber=%s&RecordNumber=%s&DistrictNumber=%s" % (self.street, self.getNormalizedTownName(),self.descNumber,self.getNormalizedZIPCode(),self.getNormalizedDistrictName(), self.orientationNumber, self.recordNumber, self.districtNumber)
            #url = u"http://www.vugtk.cz/euradin/services/rest.py/CompileAddress/HTML?AddressPlaceId=&SearchText=&Street=%s&Locality=%s&HouseNumber=%s&ZIPCode=%s&LocalityPart=%s&OrientationNumber=%s&RecordNumber=%s&DistrictNumber=%s" % (self.street, self.getNormalizedTownName(),self.descNumber,self.getNormalizedZIPCode(),self.getNormalizedDistrictName(), self.orientationNumber, self.recordNumber, self.districtNumber)
            url = url.replace(" ", "%20")
            html = urllib2.urlopen(url.encode('utf-8')).read()
            return html

        # 3. Adresní místo v Praze s ulicí a číslem evidenčním
        if self.town.lower() == self.PRAHA_NAME and self.street != "" and self.recordNumber != "":
            url = u"http://192.168.1.130:8080/CompileAddress/HTML?AddressPlaceId=&SearchText=&Street=%s&Locality=%s&HouseNumber=%s&ZIPCode=%s&LocalityPart=%s&OrientationNumber=%s&RecordNumber=%s&DistrictNumber=%s" % (self.street, self.getNormalizedTownName(),self.descNumber,self.getNormalizedZIPCode(),self.getNormalizedDistrictName(), self.orientationNumber, self.recordNumber, self.districtNumber)
            #url = u"http://www.vugtk.cz/euradin/services/rest.py/CompileAddress/HTML?AddressPlaceId=&SearchText=&Street=%s&Locality=%s&HouseNumber=%s&ZIPCode=%s&LocalityPart=%s&OrientationNumber=%s&RecordNumber=%s&DistrictNumber=%s" % (self.street, self.getNormalizedTownName(),self.descNumber,self.getNormalizedZIPCode(),self.getNormalizedDistrictName(), self.orientationNumber, self.recordNumber, self.districtNumber)
            url = url.replace(" ", "%20")
            html = urllib2.urlopen(url.encode('utf-8')).read()
            return html

        # 4. Adresní místo v Praze s číslem evidenčním
        if self.town.lower() == self.PRAHA_NAME and self.street == "" and self.recordNumber != "":
            url = u"http://192.168.1.130:8080/CompileAddress/HTML?AddressPlaceId=&SearchText=&Street=%s&Locality=%s&HouseNumber=%s&ZIPCode=%s&LocalityPart=%s&OrientationNumber=%s&RecordNumber=%s&DistrictNumber=%s" % (self.street, self.getNormalizedTownName(),self.descNumber,self.getNormalizedZIPCode(),self.getNormalizedDistrictName(), self.orientationNumber, self.recordNumber, self.districtNumber)
            #url = u"http://www.vugtk.cz/euradin/services/rest.py/CompileAddress/HTML?AddressPlaceId=&SearchText=&Street=%s&Locality=%s&HouseNumber=%s&ZIPCode=%s&LocalityPart=%s&OrientationNumber=%s&RecordNumber=%s&DistrictNumber=%s" % (self.street, self.getNormalizedTownName(),self.descNumber,self.getNormalizedZIPCode(),self.getNormalizedDistrictName(), self.orientationNumber, self.recordNumber, self.districtNumber)
            url = url.replace(" ", "%20")
            #try:
            html = urllib2.urlopen(url.encode('utf-8')).read()
            #except urllib2.HTTPError, error:
            #    html = error.read()
            return html

        # 5. Adresní místo mimo Prahu s ulicí, číslem popisným a orientačním, název obce a její části nejsou shodné
        if self.town.lower() != self.PRAHA_NAME and self.street != "" and self.descNumber != "" and self.orientationNumber != "" and self.town != self.district:
            url = u"http://192.168.1.130:8080/CompileAddress/HTML?AddressPlaceId=&SearchText=&Street=%s&Locality=%s&HouseNumber=%s&ZIPCode=%s&LocalityPart=%s&OrientationNumber=%s&RecordNumber=%s&DistrictNumber=%s" % (self.street, self.getNormalizedTownName(),self.descNumber,self.getNormalizedZIPCode(),self.getNormalizedDistrictName(), self.orientationNumber, self.recordNumber, self.districtNumber)
            #url = u"http://www.vugtk.cz/euradin/services/rest.py/CompileAddress/HTML?AddressPlaceId=&SearchText=&Street=%s&Locality=%s&HouseNumber=%s&ZIPCode=%s&LocalityPart=%s&OrientationNumber=%s&RecordNumber=%s&DistrictNumber=%s" % (self.street, self.getNormalizedTownName(),self.descNumber,self.getNormalizedZIPCode(),self.getNormalizedDistrictName(), self.orientationNumber, self.recordNumber, self.districtNumber)
            url = url.replace(" ", "%20")
            html = urllib2.urlopen(url.encode('utf-8')).read()
            return html

        # 6. Adresní místo mimo Prahu s ulicí, číslem popisným, název obce a její části nejsou shodné
        if self.town.lower() != self.PRAHA_NAME and self.street != "" and self.descNumber != "" and self.orientationNumber == "" and self.town != self.district:
            url = u"http://192.168.1.130:8080/CompileAddress/HTML?AddressPlaceId=&SearchText=&Street=%s&Locality=%s&HouseNumber=%s&ZIPCode=%s&LocalityPart=%s&OrientationNumber=%s&RecordNumber=%s&DistrictNumber=%s" % (self.street, self.getNormalizedTownName(),self.descNumber,self.getNormalizedZIPCode(),self.getNormalizedDistrictName(), self.orientationNumber, self.recordNumber, self.districtNumber)
            #url = u"http://www.vugtk.cz/euradin/services/rest.py/CompileAddress/HTML?AddressPlaceId=&SearchText=&Street=%s&Locality=%s&HouseNumber=%s&ZIPCode=%s&LocalityPart=%s&OrientationNumber=%s&RecordNumber=%s&DistrictNumber=%s" % (self.street, self.getNormalizedTownName(),self.descNumber,self.getNormalizedZIPCode(),self.getNormalizedDistrictName(), self.orientationNumber, self.recordNumber, self.districtNumber)
            url = url.replace(" ", "%20")
            html = urllib2.urlopen(url.encode('utf-8')).read()
            return html

        # 7. Adresní místo mimo Prahu s ulicí a číslem evidenčním, název obce a její části nejsou shodné
        if self.town.lower() != self.PRAHA_NAME and self.street != "" and self.descNumber == "" and self.recordNumber != "" and self.orientationNumber == "" and self.town != self.district:
            url = u"http://192.168.1.130:8080/CompileAddress/HTML?AddressPlaceId=&SearchText=&Street=%s&Locality=%s&HouseNumber=%s&ZIPCode=%s&LocalityPart=%s&OrientationNumber=%s&RecordNumber=%s&DistrictNumber=%s" % (self.street, self.getNormalizedTownName(),self.descNumber,self.getNormalizedZIPCode(),self.getNormalizedDistrictName(), self.orientationNumber, self.recordNumber, self.districtNumber)
            #url = u"http://www.vugtk.cz/euradin/services/rest.py/CompileAddress/HTML?AddressPlaceId=&SearchText=&Street=%s&Locality=%s&HouseNumber=%s&ZIPCode=%s&LocalityPart=%s&OrientationNumber=%s&RecordNumber=%s&DistrictNumber=%s" % (self.street, self.getNormalizedTownName(),self.descNumber,self.getNormalizedZIPCode(),self.getNormalizedDistrictName(), self.orientationNumber, self.recordNumber, self.districtNumber)
            url = url.replace(" ", "%20")
            html = urllib2.urlopen(url.encode('utf-8')).read()
            return html

        # 8. Adresní místo mimo Prahu s ulicí a číslem popisným, název obce a její části jsou shodné
        if self.town.lower() != self.PRAHA_NAME and self.street != "" and self.descNumber != "" and self.recordNumber == "" and self.orientationNumber == "" and self.town == self.district:
            url = u"http://192.168.1.130:8080/CompileAddress/HTML?AddressPlaceId=&SearchText=&Street=%s&Locality=%s&HouseNumber=%s&ZIPCode=%s&LocalityPart=%s&OrientationNumber=%s&RecordNumber=%s&DistrictNumber=%s" % (self.street, self.getNormalizedTownName(),self.descNumber,self.getNormalizedZIPCode(),self.getNormalizedDistrictName(), self.orientationNumber, self.recordNumber, self.districtNumber)
            #url = u"http://www.vugtk.cz/euradin/services/rest.py/CompileAddress/HTML?AddressPlaceId=&SearchText=&Street=%s&Locality=%s&HouseNumber=%s&ZIPCode=%s&LocalityPart=%s&OrientationNumber=%s&RecordNumber=%s&DistrictNumber=%s" % (self.street, self.getNormalizedTownName(),self.descNumber,self.getNormalizedZIPCode(),self.getNormalizedDistrictName(), self.orientationNumber, self.recordNumber, self.districtNumber)
            url = url.replace(" ", "%20")
            html = urllib2.urlopen(url.encode('utf-8')).read()
            return html

        # 9. Adresní místo mimo Prahu s ulicí, číslem popisným a orientačním, název obce a její části jsou shodné
        if self.town.lower() != self.PRAHA_NAME and self.street != "" and self.descNumber != "" and self.recordNumber == "" and self.orientationNumber != "" and self.town == self.district:
            url = u"http://192.168.1.130:8080/CompileAddress/HTML?AddressPlaceId=&SearchText=&Street=%s&Locality=%s&HouseNumber=%s&ZIPCode=%s&LocalityPart=%s&OrientationNumber=%s&RecordNumber=%s&DistrictNumber=%s" % (self.street, self.getNormalizedTownName(),self.descNumber,self.getNormalizedZIPCode(),self.getNormalizedDistrictName(), self.orientationNumber, self.recordNumber, self.districtNumber)
            #url = u"http://www.vugtk.cz/euradin/services/rest.py/CompileAddress/HTML?AddressPlaceId=&SearchText=&Street=%s&Locality=%s&HouseNumber=%s&ZIPCode=%s&LocalityPart=%s&OrientationNumber=%s&RecordNumber=%s&DistrictNumber=%s" % (self.street, self.getNormalizedTownName(),self.descNumber,self.getNormalizedZIPCode(),self.getNormalizedDistrictName(), self.orientationNumber, self.recordNumber, self.districtNumber)
            url = url.replace(" ", "%20")
            html = urllib2.urlopen(url.encode('utf-8')).read()
            return html

        # 10. Adresní místo mimo Prahu s ulicí a číslem evidenčním, název obce a její části jsou shodné
        if self.town.lower() != self.PRAHA_NAME and self.street != "" and self.descNumber == "" and self.recordNumber != "" and self.orientationNumber == "" and self.town == self.district:
            url = u"http://192.168.1.130:8080/CompileAddress/HTML?AddressPlaceId=&SearchText=&Street=%s&Locality=%s&HouseNumber=%s&ZIPCode=%s&LocalityPart=%s&OrientationNumber=%s&RecordNumber=%s&DistrictNumber=%s" % (self.street, self.getNormalizedTownName(),self.descNumber,self.getNormalizedZIPCode(),self.getNormalizedDistrictName(), self.orientationNumber, self.recordNumber, self.districtNumber)
            #url = u"http://www.vugtk.cz/euradin/services/rest.py/CompileAddress/HTML?AddressPlaceId=&SearchText=&Street=%s&Locality=%s&HouseNumber=%s&ZIPCode=%s&LocalityPart=%s&OrientationNumber=%s&RecordNumber=%s&DistrictNumber=%s" % (self.street, self.getNormalizedTownName(),self.descNumber,self.getNormalizedZIPCode(),self.getNormalizedDistrictName(), self.orientationNumber, self.recordNumber, self.districtNumber)
            url = url.replace(" ", "%20")
            html = urllib2.urlopen(url.encode('utf-8')).read()
            return html

        # 11. Adresní místo mimo Prahu s číslem popisným, název obce a její části nejsou shodné
        if self.town.lower() != self.PRAHA_NAME and self.street == "" and self.descNumber != "" and self.recordNumber == "" and self.orientationNumber == "" and self.town != self.district:
            url = u"http://192.168.1.130:8080/CompileAddress/HTML?AddressPlaceId=&SearchText=&Street=%s&Locality=%s&HouseNumber=%s&ZIPCode=%s&LocalityPart=%s&OrientationNumber=%s&RecordNumber=%s&DistrictNumber=%s" % (self.street, self.getNormalizedTownName(),self.descNumber,self.getNormalizedZIPCode(),self.getNormalizedDistrictName(), self.orientationNumber, self.recordNumber, self.districtNumber)
            #url = u"http://www.vugtk.cz/euradin/services/rest.py/CompileAddress/HTML?AddressPlaceId=&SearchText=&Street=%s&Locality=%s&HouseNumber=%s&ZIPCode=%s&LocalityPart=%s&OrientationNumber=%s&RecordNumber=%s&DistrictNumber=%s" % (self.street, self.getNormalizedTownName(),self.descNumber,self.getNormalizedZIPCode(),self.getNormalizedDistrictName(), self.orientationNumber, self.recordNumber, self.districtNumber)
            url = url.replace(" ", "%20")
            html = urllib2.urlopen(url.encode('utf-8')).read()
            return html

        # 12. Adresní místo mimo Prahu s číslem popisným a orientačním, název obce a její části nejsou shodné
        if self.town.lower() != self.PRAHA_NAME and self.street == "" and self.descNumber != "" and self.recordNumber == "" and self.orientationNumber != "" and self.town != self.district:
            url = u"http://192.168.1.130:8080/CompileAddress/HTML?AddressPlaceId=&SearchText=&Street=%s&Locality=%s&HouseNumber=%s&ZIPCode=%s&LocalityPart=%s&OrientationNumber=%s&RecordNumber=%s&DistrictNumber=%s" % (self.street, self.getNormalizedTownName(),self.descNumber,self.getNormalizedZIPCode(),self.getNormalizedDistrictName(), self.orientationNumber, self.recordNumber, self.districtNumber)
            #url = u"http://www.vugtk.cz/euradin/services/rest.py/CompileAddress/HTML?AddressPlaceId=&SearchText=&Street=%s&Locality=%s&HouseNumber=%s&ZIPCode=%s&LocalityPart=%s&OrientationNumber=%s&RecordNumber=%s&DistrictNumber=%s" % (self.street, self.getNormalizedTownName(),self.descNumber,self.getNormalizedZIPCode(),self.getNormalizedDistrictName(), self.orientationNumber, self.recordNumber, self.districtNumber)
            url = url.replace(" ", "%20")
            html = urllib2.urlopen(url.encode('utf-8')).read()
            return html

        # 13. Adresní místo mimo Prahu s číslem evidenčním, název obce a její části nejsou shodné
        if self.town.lower() != self.PRAHA_NAME and self.street == "" and self.descNumber == "" and self.recordNumber != "" and self.orientationNumber == "" and self.town != self.district:
            url = u"http://192.168.1.130:8080/CompileAddress/HTML?AddressPlaceId=&SearchText=&Street=%s&Locality=%s&HouseNumber=%s&ZIPCode=%s&LocalityPart=%s&OrientationNumber=%s&RecordNumber=%s&DistrictNumber=%s" % (self.street, self.getNormalizedTownName(),self.descNumber,self.getNormalizedZIPCode(),self.getNormalizedDistrictName(), self.orientationNumber, self.recordNumber, self.districtNumber)
            #url = u"http://www.vugtk.cz/euradin/services/rest.py/CompileAddress/HTML?AddressPlaceId=&SearchText=&Street=%s&Locality=%s&HouseNumber=%s&ZIPCode=%s&LocalityPart=%s&OrientationNumber=%s&RecordNumber=%s&DistrictNumber=%s" % (self.street, self.getNormalizedTownName(),self.descNumber,self.getNormalizedZIPCode(),self.getNormalizedDistrictName(), self.orientationNumber, self.recordNumber, self.districtNumber)
            url = url.replace(" ", "%20")
            html = urllib2.urlopen(url.encode('utf-8')).read()
            return html

        # 14. Adresní místo mimo Prahu s číslem popisným, název obce a její části jsou shodné
        if self.town.lower() != self.PRAHA_NAME and self.street == "" and self.descNumber != "" and self.recordNumber == "" and self.orientationNumber == "" and self.town == self.district:
            url = u"http://192.168.1.130:8080/CompileAddress/HTML?AddressPlaceId=&SearchText=&Street=%s&Locality=%s&HouseNumber=%s&ZIPCode=%s&LocalityPart=%s&OrientationNumber=%s&RecordNumber=%s&DistrictNumber=%s" % (self.street, self.getNormalizedTownName(),self.descNumber,self.getNormalizedZIPCode(),self.getNormalizedDistrictName(), self.orientationNumber, self.recordNumber, self.districtNumber)
            #url = u"http://www.vugtk.cz/euradin/services/rest.py/CompileAddress/HTML?AddressPlaceId=&SearchText=&Street=%s&Locality=%s&HouseNumber=%s&ZIPCode=%s&LocalityPart=%s&OrientationNumber=%s&RecordNumber=%s&DistrictNumber=%s" % (self.street, self.getNormalizedTownName(),self.descNumber,self.getNormalizedZIPCode(),self.getNormalizedDistrictName(), self.orientationNumber, self.recordNumber, self.districtNumber)
            url = url.replace(" ", "%20")
            html = urllib2.urlopen(url.encode('utf-8')).read()
            return html

        # 15. Adresní místo mimo Prahu s číslem popisným a orientačním, název obce a její části jsou shodné
        if self.town.lower() != self.PRAHA_NAME and self.street == "" and self.descNumber != "" and self.recordNumber == "" and self.orientationNumber != "" and self.town == self.district:
            url = u"http://192.168.1.130:8080/CompileAddress/HTML?AddressPlaceId=&SearchText=&Street=%s&Locality=%s&HouseNumber=%s&ZIPCode=%s&LocalityPart=%s&OrientationNumber=%s&RecordNumber=%s&DistrictNumber=%s" % (self.street, self.getNormalizedTownName(),self.descNumber,self.getNormalizedZIPCode(),self.getNormalizedDistrictName(), self.orientationNumber, self.recordNumber, self.districtNumber)
            #url = u"http://www.vugtk.cz/euradin/services/rest.py/CompileAddress/HTML?AddressPlaceId=&SearchText=&Street=%s&Locality=%s&HouseNumber=%s&ZIPCode=%s&LocalityPart=%s&OrientationNumber=%s&RecordNumber=%s&DistrictNumber=%s" % (self.street, self.getNormalizedTownName(),self.descNumber,self.getNormalizedZIPCode(),self.getNormalizedDistrictName(), self.orientationNumber, self.recordNumber, self.districtNumber)
            url = url.replace(" ", "%20")
            html = urllib2.urlopen(url.encode('utf-8')).read()
            return html

        # 16. Adresní místo mimo Prahu s číslem evidenčním, název obce a její části jsou shodné
        if self.town.lower() != self.PRAHA_NAME and self.street == "" and self.descNumber == "" and self.recordNumber != "" and self.orientationNumber == "" and self.town == self.district:
            url = u"http://192.168.1.130:8080/CompileAddress/HTML?AddressPlaceId=&SearchText=&Street=%s&Locality=%s&HouseNumber=%s&ZIPCode=%s&LocalityPart=%s&OrientationNumber=%s&RecordNumber=%s&DistrictNumber=%s" % (self.street, self.getNormalizedTownName(),self.descNumber,self.getNormalizedZIPCode(),self.getNormalizedDistrictName(), self.orientationNumber, self.recordNumber, self.districtNumber)
            #url = u"http://www.vugtk.cz/euradin/services/rest.py/CompileAddress/HTML?AddressPlaceId=&SearchText=&Street=%s&Locality=%s&HouseNumber=%s&ZIPCode=%s&LocalityPart=%s&OrientationNumber=%s&RecordNumber=%s&DistrictNumber=%s" % (self.street, self.getNormalizedTownName(),self.descNumber,self.getNormalizedZIPCode(),self.getNormalizedDistrictName(), self.orientationNumber, self.recordNumber, self.districtNumber)
            url = url.replace(" ", "%20")
            html = urllib2.urlopen(url.encode('utf-8')).read()
            return html
