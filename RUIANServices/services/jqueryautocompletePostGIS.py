# -*- coding: utf-8 -*-
__author__ = 'Augustyn'
#-------------------------------------------------------------------------------
# Name:        jqueryautocompletePostGIS
# Purpose:     Implementuje funkcionalitu pro autocomplete pomocí jQuery
#              napojením na databázi RÚIAN uloženou v PostGIS.
# Author:      raugustyn
#
# Created:     10/11/2013
# Copyright:   (c) raugustyn 2013
# Licence:
#-------------------------------------------------------------------------------

import psycopg2
import compileaddress
import HTTPShared
from config import config

AC_OBCE  = "ac_obce"
AC_PSC   = "ac_psc"
AC_ULICE = "ac_ulice"
AC_CASTI_OBCE = "ac_casti_obce"

class PostGISDatabase():

    def __init__(self):
        self.conection = psycopg2.connect(host = config.databaseHost, database = config.databaseName,
                                          port = config.databasePort, user = config.databaseUserName,
                                          password = config.databasePassword)

    def getQueryResult(self, query):
        cursor = self.conection.cursor()
        cursor.execute(query)

        rows = []
        row_count = 0
        for row in cursor:
            row_count += 1
            rows.append(row)
        return rows

    def getObecByName(self, name):
        cursor = self.conection.cursor()
        cursor.execute("SELECT obce FROM " + AC_OBCE + " WHERE nazev_obce like '%" + name + "%'")

        rows = []
        row_count = 0
        for row in cursor:
              row_count += 1
              data = row[0]
              data = data[1:len(data) - 1]
              rows.append(data)
        return rows

    def getZIPByStreetAndTown(self, streetName, townName):
        cursor = self.conection.cursor()
        cursor.execute("SELECT psc FROM addresspoints WHERE nazev_obce = '" + townName + "' and nazev_ulice = '" + streetName + "'")

        rows = []
        row_count = 0
        for row in cursor:
              row_count += 1
              data = row[0]
              data = data[1:len(data) - 1]
              rows.append(data)
        return rows

def numberToString(number):
    if number is None:
        return ""
    else:
        return str(number)

def extractDictrictNumber(nazev_mop):
    # Praha 10 -> 10
    if (nazev_mop != "") and (nazev_mop != None) and (nazev_mop.find(" ") >= 0):
        return nazev_mop.split(" ")[1]
    else:
        return ""

def analyseRow(typ_so, cislo_domovni):
    if typ_so[-3:] == ".p.":
        houseNumber = numberToString(cislo_domovni)
        recordNumber = ""
    elif typ_so[-3:] == "ev.":
        houseNumber = ""
        recordNumber = numberToString(cislo_domovni)
    else:
        pass

    return houseNumber, recordNumber

def itemToStr(item):
    if item == None:
        return ""
    else:
        return str(item)

builder = HTTPShared.MimeBuilder("texttoonerow")

ID_VALUE = 'id'

def getAutocompleteOneItemResults(ruianType, nameToken, maxCount = 10):
    if nameToken == "" or nameToken == None:
        return []

    if ruianType == "":
        ruianType == ID_VALUE

    nameToken = nameToken.lower()

    joinSeparator = ", "
    if ruianType == ID_VALUE:
        searchSQL = "select gid from gids where cast(gid as text) ilike '" + nameToken + "%'"

    searchSQL += " limit " + str(maxCount)

    try:
        db = PostGISDatabase()
        cursor = db.conection.cursor()
        cursor.execute(searchSQL)
    except:
        import sys
        return[sys.exc_info()[0]]

    rows = []
    rowCount = 0
    for row in cursor:
        rowCount += 1
        v = str(row[0])
        value = '{"id":"' + v + '","label":"' + v + '","value":"' + v + '"}'
        rows.append(value)
        if rowCount >= maxCount:  break

    return rows

def parseFullTextToken(nameToken):
    hasNumber = False

    if nameToken.isdigit():
        # jedná se o PSČ nebo číslo bez ulice
        if len(nameToken) < 2:
            return(False, "")
        else:
            name = ""
            cislo = nameToken
            hasNumber = True
    else:
        name = nameToken
        cislo = ""
        delPos = nameToken.rfind(" ")
        if delPos >= 0:
            # je druhá část cislo?
            name = nameToken[:delPos]
            cislo = nameToken[delPos + 1:]
            if cislo.isdigit():
                hasNumber = True
            else:
                cislo = ""
                name = nameToken

    if hasNumber:
        whereList = []
        if name != "":
            whereList.append("nazev_ulice ilike '%" + name + "%'")
        else:
            whereList.append("nazev_ulice is null")

        if cislo != "":
            whereList.append("(cast(cislo_domovni as text) ilike '" + cislo + "%'" + \
                        "or cast(cislo_orientacni as text) ilike '" + cislo + "%')")
        searchSQL = 'select nazev_ulice, cast(cislo_domovni as text), nazev_obce, cast(psc as text),' \
                    'cast(cislo_orientacni as text), znak_cisla_orientacniho, nazev_casti_obce, typ_so, nazev_mop from ' \
                    'address_points where ' + " and ".join(whereList)


    else:
        searchSQL = "select nazev_ulice, nazev_obce from " + AC_ULICE + " where nazev_ulice ilike '%" + nameToken + "%'"

    return (hasNumber, searchSQL)

def getRows(searchSQL, maxCount = 10):
    rows = []
    if searchSQL != "":
        searchSQL += " limit " + str(maxCount)

        try:
            db = PostGISDatabase()
            cursor = db.conection.cursor()
            cursor.execute(searchSQL)
        except:
            import sys
            return[sys.exc_info()[0]]

        rowCount = 0
        for row in cursor:
            rowCount += 1

            htmlItems = []
            for i in range(len(row)):
                if True:
                    htmlItems.insert(0, row[i])
                else:
                    item = row[i]
                    htmlItems.insert(0, item)

                rowLabel = None

            if len(row) == 1:
                idValue = ""#row[0]
                rowValue = row[0]
            else:
                rowValue = row[1]
                idValue = row[0]

            if rowLabel == None:
                rowLabel = ", ".join(htmlItems)


            value = '{"id":"' + idValue + '","label":"' + rowLabel + '","value":"' + rowValue + '"}'

            rows.append(value)

            if rowCount >= maxCount:
                break

    return rows

def getTownAutocompleteResults(nameToken, resultFormat, maxCount = 10):
    if nameToken == "" or nameToken == None:
        return []

    nameToken = nameToken.lower()

    searchSQL = "select nazev_obce from " + AC_OBCE + " where nazev_obce ilike '%" + nameToken + "%'"
    rows = getRows(searchSQL)

    searchSQL = "select nazev_casti_obce, nazev_obce from " + AC_CASTI_OBCE + " where nazev_casti_obce ilike '%" + nameToken + "%'" + \
                " and nazev_casti_obce <> nazev_obce"
    rows.extend(getRows(searchSQL))

    return rows

def getAutocompleteResults(ruianType, nameToken, resultFormat, maxCount = 10):
    if nameToken == "" or nameToken == None:
        return []

    if ruianType == "":
        ruianType == "town"

    nameToken = nameToken.lower()

    rows = []

    joinSeparator = ", "
    hasNumber = False
    isStreet = False
    if ruianType == "townpart":
        searchSQL = "select nazev_casti_obce, nazev_obce from " + AC_CASTI_OBCE + " where nazev_casti_obce ilike '%" + nameToken + "%'"
    elif ruianType == "town":
        return getTownAutocompleteResults(nameToken, resultFormat, maxCount)
    elif ruianType == ID_VALUE:
        searchSQL = "select cast(gid as text), address from ac_gids where cast(gid as text) like '" + nameToken + "%'"
    elif ruianType == "zip":
        searchSQL = "select psc, nazev_obce from " + AC_PSC + " where psc like '" + nameToken + "%'"
        joinSeparator = " "
    else:
        # street or textsearch
        hasNumber, searchSQL = parseFullTextToken(nameToken)

    if searchSQL != "":
        searchSQL += " limit " + str(maxCount)

        try:
            db = PostGISDatabase()
            cursor = db.conection.cursor()
            cursor.execute(searchSQL)
        except:
            import sys
            return[sys.exc_info()[0]]

        rowCount = 0
        for row in cursor:
            rowCount += 1

            htmlItems = []
            for i in range(len(row)):
                if True:
                    htmlItems.append(row[i])
                else:
                    item = row[i]
                    htmlItems.append(item)

                rowLabel = None

            if ruianType == "street" or ruianType == "textsearch":
                if hasNumber:
                    street, houseNumber, locality, zipCode, orientationNumber, orientationNumberCharacter, localityPart, typ_so, nazev_mop = row

                    houseNumber, recordNumber = analyseRow(typ_so, houseNumber)
                    districtNumber = extractDictrictNumber(nazev_mop)

                    rowLabel = compileaddress.compileAddress(builder, street, houseNumber, recordNumber, orientationNumber, orientationNumberCharacter, zipCode, locality, localityPart, districtNumber)
                    if resultFormat.lower() == "addressparts":
                        idValue =  itemToStr(street) + "," + itemToStr(houseNumber) + "," + itemToStr(recordNumber) + "," + itemToStr(orientationNumber) + "," + \
                               itemToStr(orientationNumberCharacter) + "," + itemToStr(zipCode) + "," + \
                               itemToStr(locality) + "," + itemToStr(localityPart) + "," + itemToStr(districtNumber)
                    else:
                        idValue = rowLabel[rowLabel.find(", ") + 2:]
                else:
                    idValue = row[1] # + ", " + row[2]
            else:
                idValue = row[1]

            if rowLabel == None:
                rowLabel = joinSeparator.join(htmlItems)

            if ruianType == "textsearch":
                rowValue = rowLabel
            else:
                if hasNumber:
                    rowValue = rowLabel[:rowLabel.find(",")]
                else:
                    rowValue = row[0]

            value = '{"id":"' + idValue + '","label":"' + rowLabel + '","value":"' + rowValue + '"}'

            rows.append(value)

            if rowCount >= maxCount:
                break

    return rows

def main():
    #print getAutocompleteResults("zip", "16")
    #print getAutocompleteResults("street", "Mrkvičkova 13")
    print getAutocompleteResults("street", "Budovatelů 6")

if __name__ == '__main__':
    import sys
    reload(sys)
    sys.setdefaultencoding('utf-8')
    main()

