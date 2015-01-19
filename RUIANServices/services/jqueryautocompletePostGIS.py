# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        jqueryautocompletePostGIS
# Purpose:     Implementuje funkcionalitu pro autocomplete pomocí jQuery
#              napojením na databázi RÚIAN uloženou v PostGIS.
#
# Author:      Radek Augustýn
# Copyright:   (c) VUGTK, v.v.i. 2014
# License:     CC BY-SA 4.0
#-------------------------------------------------------------------------------

import psycopg2
import compileaddress
import HTTPShared
from config import config

AC_OBCE  = "ac_obce"
AC_PSC   = "ac_psc"
AC_ULICE = "ac_ulice"
AC_CASTI_OBCE = "ac_casti_obce"
ADDRESSPOINTS_TABLENAME = "address_points"
LOCALITY_QUERY_ID = "Locality"
LOCALITY_PART_QUERY_ID = "LocalityPart"
PAGESIZE_QUERYPARAM = "PageSize"
FIRSTROW_QUERYPARAM = "FirstRow"

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

def valueToStr(value):
    if value is None:
        return ""
    else:
        return str(value)

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

def parseFullTextToken(queryParams, nameToken):
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
        searchSQL = "select nazev_ulice, nazev_obce from " + AC_ULICE + " where nazev_ulice ilike '%" + nameToken + "%' group by nazev_ulice, nazev_obce order by nazev_ulice, nazev_obce"

    localityName = getQueryValue(queryParams, "localityName", "")
    if localityName != "":
        searchSQL += " and nazev_obce ilike '%" + localityName + "%'"

    localityPart = getQueryValue(queryParams, "localityPart", "")
    if localityPart != "":
        searchSQL += " and nazev_casti_obce ilike '%" + localityPart + "%'"

    return (hasNumber, searchSQL)

def getRows(searchSQL, maxCount = 15):
    rows = []
    if searchSQL != "" and maxCount != 0:
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
                idValue = ""
                rowValue = row[0]
            else:
                rowValue = row[1]
                idValue = row[0]

            if rowLabel == None:
                rowLabel = ", ".join(htmlItems)


            value = '{ "id" : "%s", "label" : "%s", "value" : "%s" }' % (idValue, rowLabel, rowValue)

            rows.append(value)

            if rowCount >= maxCount:
                break

    return rows

def getAutocompleteRows(searchSQL, fieldCount = 0, maxCount = 15):
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
            # TODO ošetřit výjimku

        rowCount = 0
        for row in cursor:
            rowCount += 1

            labelItems = []
            idItems = []
            for field in row:
                labelItems.append(str(field))
                idItems.append(str(field))

            while len(idItems) < fieldCount:
                idItems.append("")

            rowLabel = ", ".join(labelItems)
            idValue = ", ".join(idItems[1:])

            value = '{ "id" : "%s", "label" : "%s", "value" : "%s" }' % (idValue, rowLabel, row[0])

            rows.append(value)

            if rowCount >= maxCount:
                break

    return rows

def getQueryValue(queryParams, id, defValue):
    # Vrací hodnotu URL Query parametruy id, pokud neexistuje, vrací hodnotu defValue
    if queryParams.has_key(id):
        return queryParams[id]
    else:
        return defValue

def getSQLWhereClause(queryParams, paramList, andIsBeroreClause = True):
    result = u""
    for key in paramList:
        value =  getQueryValue(queryParams, key, "")
        if value != "":
            if andIsBeroreClause:
                result += " and "
            result += paramList[key] + " ilike '%" + value + "%'"
            if not andIsBeroreClause:
                result += " and "



    return result

def selectSQL(searchSQL):
    if searchSQL == None or searchSQL == "": return None

    try:
        db = PostGISDatabase()
        cursor = db.conection.cursor()
        cursor.execute(searchSQL)
        return cursor
    except:
        import sys
        return[sys.exc_info()[0]]

def getFillResults(queryParams):
    sqlItems = {
        "HouseNumber"  : "cast(cislo_domovni as text) like '%s%%' and typ_so='č.p.'",
        "RecordNumber" : "cast(cislo_domovni as text) ilike '%s%%' and typ_so<>'č.p.'",
        "OrientationNumber" : "cast(cislo_orientacni as text) like '%s%%'",
        "OrientationNumberCharacter" : "znak_cisla_orientacniho = '%s'",
        "ZIPCode" : "cast(psc as text) like '%s%%'",
        "Locality" : "nazev_obce ilike '%%%s%%'",
        "Street" : "nazev_ulice ilike '%%%s%%'",
        "LocalityPart" : "nazev_casti_obce ilike '%%%s%%'",
        "DistrictNumber" : "nazev_mop = 'Praha %s'"
    }

    firstRow = int(getQueryValue(queryParams, FIRSTROW_QUERYPARAM, "0"))
    if firstRow < 0: firstRow = 0
    pageSize = int(getQueryValue(queryParams, PAGESIZE_QUERYPARAM, "15"))

    limitValue = 100
    if limitValue < firstRow + pageSize:
        limitValue = firstRow + pageSize


    fields = " cislo_domovni, cislo_orientacni, znak_cisla_orientacniho, psc, nazev_obce, nazev_casti_obce, nazev_mop, nazev_ulice, typ_so "
    result = ""

    sqlParts = []
    for key in sqlItems:
        value = getQueryValue(queryParams, key, "")
        if value != "":
            sqlParts.append(sqlItems[key] % (value))

    if len(sqlParts) == 0: return ""

    sqlBase = u" from %s where " % (ADDRESSPOINTS_TABLENAME) + " and ".join(sqlParts)

    searchSQL = u"select %s %s order by  nazev_obce, nazev_casti_obce, psc, nazev_ulice, nazev_mop, typ_so, cislo_domovni, cislo_orientacni, znak_cisla_orientacniho limit %d" % (fields, sqlBase, limitValue)
    rows = selectSQL(searchSQL)

    resultArray = []
    rowNumber = 0
    for row in rows:
        if rowNumber >= firstRow:
            htmlItems = []
            for i in range(len(row)):
                htmlItems.append(numberToString(row[i]))

            houseNumber, orientationNumber, orientationNumberCharacter, zipCode, locality,   localityPart, nazev_mop, street,  typ_so = row
            houseNumber, recordNumber = analyseRow(typ_so, houseNumber)
            districtNumber = extractDictrictNumber(nazev_mop)

            rowLabel = compileaddress.compileAddress(builder, street, houseNumber, recordNumber, orientationNumber, orientationNumberCharacter, zipCode, locality, localityPart, districtNumber)

            resultArray.append(":".join(htmlItems) + ":" + rowLabel)
            if len(resultArray) >= pageSize: break
        rowNumber = rowNumber + 1

    rowCount = rows.rowcount
    if rowCount == limitValue:
        countSQL = u"select count(*) " + sqlBase
        countRows = selectSQL(countSQL)
        countRow = countRows.fetchone()
        rowCount = countRow[0]


    result = "%d#%d#%d#%s" % (firstRow, len(resultArray), rowCount, ";".join(resultArray))
    return  result

def getTownPartResults(queryParams, nameToken, smartAutocomplete, maxCount = 10):
    localityClause = ""
    if smartAutocomplete:
        locality = getQueryValue(queryParams, LOCALITY_QUERY_ID, "")
        if locality != "":
            localityClause = " nazev_obce = '%s' and " % locality

    searchSQL = u"select nazev_casti_obce, nazev_obce from %s where %s nazev_casti_obce ilike '%%%s%%'" % (AC_CASTI_OBCE, localityClause, nameToken)
    rows = getAutocompleteRows(searchSQL, 0, maxCount)

    return rows

def getStreetResults(queryParams, nameToken, smartAutocomplete, maxCount = 10):
    if smartAutocomplete:
        whereClause = getSQLWhereClause(queryParams, {"Locality" : u"nazev_obce", "LocalityPart" : u"nazev_casti_obce"}, False)
    else:
        whereClause = ""

    searchSQL = (u"select nazev_ulice, nazev_obce from %s where %s nazev_ulice ilike '%%%s%%' group by nazev_obce, nazev_ulice order by nazev_obce, nazev_ulice") % (AC_ULICE, whereClause, nameToken)
    rows = getAutocompleteRows(searchSQL, 0, maxCount)

    return rows

def getTownAutocompleteResults(queryParams, nameToken, smartAutocomplete, maxCount = 10):
    localityPart = getQueryValue(queryParams, LOCALITY_PART_QUERY_ID, "")
    if localityPart == "" or smartAutocomplete == False:
        searchSQL = u"select nazev_obce from %s where nazev_obce ilike '%%%s%%'" % (AC_OBCE, nameToken)
        rows = getRows(searchSQL)
        searchSQL = u"select nazev_casti_obce, nazev_obce from %s where nazev_casti_obce ilike '%%%s%%' and nazev_casti_obce <> nazev_obce" % (AC_CASTI_OBCE, nameToken)
        rows.extend(getRows(searchSQL, maxCount))
    else:
        searchSQL = u"select nazev_obce from %s where nazev_casti_obce = '%s' and nazev_obce ilike '%%%s%%'" % (AC_OBCE, localityPart, nameToken)
        rows = getRows(searchSQL, maxCount)

    return rows

def getZIPResults(queryParams, nameToken, smartAutocomplete, maxCount = 10):
    if smartAutocomplete:
        whereClause = getSQLWhereClause(queryParams, {"Locality" : u"nazev_obce", "LocalityPart" : u"nazev_casti_obce"}, False)
    else:
        whereClause = ""

    searchSQL = "select psc, nazev_obce from %s where %s psc like '%s%%' group by psc, nazev_obce order by psc, nazev_obce" % (AC_PSC, whereClause, nameToken)
    rows = getAutocompleteRows(searchSQL, 0, maxCount)

    return rows

def getIDResults(queryParams, nameToken, smartAutocomplete, maxCount = 10):
    searchSQL = "select cast(gid as text), address from ac_gids where cast(gid as text) like '" + nameToken + "%'"
    rows = getAutocompleteRows(searchSQL, 0, maxCount)

    return rows

def getHouseNumberAutocompleteResults(queryParams, nameToken, maxCount = 10):
    whereClause = getSQLWhereClause(queryParams, {"Locality" : u"nazev_obce", "LocalityPart" : u"nazev_casti_obce", "Street" : "nazev_ulice"}, False)

    if whereClause == "":
        return []
    else:
        searchSQL = "select cislo_domovni from %s where %s cast(cislo_domovni as text) like '%s%%' order by cislo_domovni" % (ADDRESSPOINTS_TABLENAME, whereClause, nameToken)

    rows = getAutocompleteRows(searchSQL, 0, maxCount)

    return rows

def getFullTextAutocompleteResults(queryParams, nameToken, resultFormat, maxCount = 10):
    hasNumber, searchSQL = parseFullTextToken(queryParams, nameToken)

    rows = []
    if searchSQL != "":
        searchSQL += " limit " + str(maxCount)

        try:
            db = PostGISDatabase()
            cursor = db.conection.cursor()
            cursor.execute(searchSQL)
        except psycopg2.Error as e:
            import sys
            return[e.pgerror, e.pgcode]

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
                idValue = row[0] + ", " + row[1]

            if rowLabel == None:
                rowLabel = ", ".join(htmlItems)

            rowValue = rowLabel

            value = '{"id":"' + idValue + '","label":"' + rowLabel + '","value":"' + rowValue + '"}'

            rows.append(value)

            if rowCount >= maxCount:
                break

    return rows

def getAutocompleteResults(queryParams, ruianType, nameToken, resultFormat, smartAutocomplete, maxCount = 10):
    if ruianType == "": ruianType == "town"
    nameToken = nameToken.lower()

    if ruianType == "townpart":
        return getTownPartResults(queryParams, nameToken, smartAutocomplete, maxCount)
    elif ruianType == "town":
        return getTownAutocompleteResults(queryParams, nameToken, smartAutocomplete, maxCount)
    elif ruianType == "housenumber":
        return getHouseNumberAutocompleteResults(queryParams, nameToken, maxCount)
    elif ruianType == ID_VALUE:
        return getIDResults(queryParams, nameToken, smartAutocomplete, maxCount)
    elif ruianType == "zip":
        return getZIPResults(queryParams, nameToken, smartAutocomplete, maxCount)
    elif ruianType == "street":
        return getStreetResults(queryParams, nameToken, smartAutocomplete, maxCount)
    else:
        return getFullTextAutocompleteResults(queryParams, nameToken, resultFormat, maxCount)

def __old_geDataListResponse(searchSQL, maxCount = 0):
    result = ""
    if searchSQL != "":
        if maxCount != 0:
            searchSQL += " limit " + str(maxCount)

        try:
            db = PostGISDatabase()
            cursor = db.conection.cursor()
            cursor.execute(searchSQL)
        except:
            import sys
            return[sys.exc_info()[0]]
            # TODO ošetřit výjimku

        resultList = []
        rowCount = 0
        for row in cursor:
            rowCount += 1
            resultList.append(str(row[0]))
            if maxCount != 0 and rowCount >= maxCount:
                break
        result = ",".join(resultList)

    return result

def sortNumberListAndLeaveEmpty(alist):
    alist = list(set(alist))
    foundEmpty = False
    result = []
    for item in alist:
        if item == "":
            if not foundEmpty:
               foundEmpty = True
        elif not item in result:
            result.append(item)
    result.sort(key=int)
    if foundEmpty:
        result.insert(0, "")
    return result

def getNumberValues(fieldName, whereClause, maxCount, noneValue = None):
    result = []

    searchSQL = "select %s from %s where %s group by %s" % (fieldName, ADDRESSPOINTS_TABLENAME, whereClause, fieldName)
    if maxCount != 0:
        searchSQL += " limit " + str(maxCount)

    try:
        db = PostGISDatabase()
        cursor = db.conection.cursor()
        cursor.execute(searchSQL)
    except:
        import sys
        return[sys.exc_info()[0]]
        # TODO ošetřit výjimku

    rowCount = 0
    for row in cursor:
        rowCount += 1
        if row[0] == None:
            if noneValue != None:result.append(noneValue)
        else:
            result.append(str(row[0]))

        if maxCount != 0 and rowCount >= maxCount:break

    return result


def getDataListValues(queryParams, maxCount = 50):
    result = '###'
    whereClause = getSQLWhereClause(queryParams, {"Locality" : u"nazev_obce", "LocalityPart" : u"nazev_casti_obce", "Street" : "nazev_ulice"}, False)
    whereClause = whereClause[:whereClause.rfind(" and")]

    if whereClause != "":
        houseNumberList = getNumberValues("cislo_domovni", whereClause + " and typ_so='č.p.' ", maxCount)
        recordNumberList = getNumberValues("cislo_domovni", whereClause + " and typ_so<>'č.p.' ", maxCount)
        orientationNumberList = getNumberValues("cislo_orientacni", whereClause, maxCount)
        orientationNumberCharacterList = getNumberValues("znak_cisla_orientacniho", whereClause, maxCount, "&nbsp;")

        houseNumberList = sortNumberListAndLeaveEmpty(houseNumberList)
        recordNumberList = sortNumberListAndLeaveEmpty(recordNumberList)
        orientationNumberList = sortNumberListAndLeaveEmpty(orientationNumberList)

        orientationNumberCharacterList = list(set(orientationNumberCharacterList))
        orientationNumberCharacterList.sort()
        if orientationNumberCharacterList == ["&nbsp;"]:
            orientationNumberCharacterList = []

        result = ",".join(houseNumberList) + "#"
        result += ",".join(recordNumberList) + "#"
        result += ",".join(orientationNumberList) + "#"
        result += ",".join(orientationNumberCharacterList)

    return result


def getMOPList(sqlQuery):
    try:
        db = PostGISDatabase()
        cursor = db.conection.cursor()
        cursor.execute(sqlQuery)
        resultList = {}
        for row in cursor:
            key = row[0]
            if resultList.has_key(key):
                resultList[key].append(row[1])
            else:
                resultList[key] = [row[1]]

        smallList = []
        for key in resultList:
            smallList.append('\t\t"%s" : "%s"' % (key, (",").join(resultList[key])))

        result = '{\n%s\n}' % (",\n").join(smallList)
    except:
        import sys
        return[sys.exc_info()[0]]

    return result

def getDistrictMOPs():
    return getMOPList("select nazev_casti_obce, nazev_mop from address_points where nazev_mop <> '' group by nazev_mop, nazev_casti_obce order by nazev_mop, nazev_casti_obce")

def getMOPDistricts():
    return getMOPList("select nazev_mop, nazev_casti_obce from address_points where nazev_mop <> '' group by nazev_casti_obce, nazev_mop order by nazev_mop, nazev_casti_obce")

def main():
    #print getAutocompleteResults("zip", "16")
    #print getAutocompleteResults("street", "Mrkvičkova 13")
    #print getAutocompleteResults("street", "Budovatelů 6")
    print getDistrictMOPs()
    #print getMOPDistricts()
    pass

if __name__ == '__main__':
    import sys
    reload(sys)
    sys.setdefaultencoding('utf-8')
    main()