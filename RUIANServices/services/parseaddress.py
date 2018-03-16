# -*- coding: utf-8 -*-
__author__ = 'raugustyn'

from collections import defaultdict
import psycopg2
import codecs
import compileaddress
from HTTPShared import *

import shared; shared.setupPaths()
import sharedtools.log as log

from config import config

DATABASE_HOST = config.databaseHost
PORT          = config.databasePort
DATABASE_NAME = config.databaseName
USER_NAME     = config.databaseUserName
PASSWORD      = config.databasePassword

ADDRESSPOINTS_TABLENAME = "address_points"
FULLTEXT_TABLENAME = "fulltext"

TOWNNAME_FIELDNAME   = "nazev_obce"
STREETNAME_FIELDNAME = "nazev_ulice"
TOWNPART_FIELDNAME   = "nazev_casti_obce"
GID_FIELDNAME        = "gid"
GIDS_FIELDNAME       = "gids"
TYP_SO_FIELDNAME     = "typ_so"
CISLO_DOMOVNI_FIELDNAME = "cislo_domovni"
CISLO_ORIENTACNI_FIELDNAME = "cislo_orientacni"
ZNAK_CISLA_ORIENTACNIHO_FIELDNAME = "znak_cisla_orientacniho"
ZIP_CODE_FIELDNAME = "psc"
MOP_NUMBER         = "nazev_mop"

# Konstanty pro logickou strukturu databáze
MAX_TEXT_COUNT = 3 # maximální počet textových položek v adrese ulice, obec, část obce = 3
ORIENTATION_NUMBER_ID = "/"
RECORD_NUMBER_ID = "č.ev."
DESCRIPTION_NUMBER_ID = "č.p."
RECORD_NUMBER_MAX_LEN = 4
ORIENTATION_NUMBER_MAX_LEN = 3
DESCRIPTION_NUMBER_MAX_LEN = 3
HOUSE_NUMBER_MAX_LEN = 4
ZIPCODE_LEN = 5


class RUIANDatabase():
    def __init__(self):
        try:
            self.conection = psycopg2.connect(host = DATABASE_HOST, database = DATABASE_NAME, port = PORT, user = USER_NAME, password = PASSWORD)
        except psycopg2.Error as e:
            log.logger.error("Could not connect to database %s at %s:%s as %s\n%s" % (DATABASE_NAME, DATABASE_HOST, PORT, USER_NAME, str(e)))
            self.conection = None


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
        cursor.execute("SELECT {0} FROM {1} WHERE {0} ilike '%{2}%' group by {0} limit 25".format(TOWNNAME_FIELDNAME, "obce", name))

        rows = []
        row_count = 0
        for row in cursor:
              row_count += 1
              rows.append(row[0])
        return rows


    def getUliceByName(self, name):
        cursor = self.conection.cursor()
        cursor.execute("SELECT {0} FROM {1} WHERE {0} ilike '%{2}%' group by {0} limit 25".format(STREETNAME_FIELDNAME, "ulice", "name"))

        rows = []
        row_count = 0
        for row in cursor:
              row_count += 1
              rows.append(row[0])
        return rows


    def getCastObceByName(self, name):
        cursor = self.conection.cursor()
        cursor.execute("SELECT nazev_casti_obce FROM casti_obce WHERE nazev_casti_obce ilike '%" + name + "%' group by nazev_casti_obce limit 25")

        rows = []
        row_count = 0
        for row in cursor:
              row_count += 1
              rows.append(row[0])
        return rows


    def getSelectResults(self, sqlSelectClause):
        cursor = self.conection.cursor()
        cursor.execute(sqlSelectClause)

        rows = []
        row_count = 0
        for row in cursor:
              row_count += 1
              rows.append(row)
        return rows


ruianDatabase = None


def isInt(value):
    if value == "" or value == None:
        return False
    else:
        for i in range(len(value)):
            if "0123456789".find(value[i:i + 1]) < 0:
                return False
        return True


def remove_accents(s):
    import unicodedata

    s = unicode(s)
    return ''.join(c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn')


class AddressItem:
    RECORD_NUMBER = 1
    ORIENTATION_NUMBER = 2
    DESCRIPTION_NUMBER = 3
    ZIP = 4
    HOUSE_NUMBER = 5
    ORIENTATION_NUMBER_SEPARATOR = 6
    ORIENTATION_NUMBER_LETTER = 7

    GID_FIELDINDEX = 0
    TOWNPART_FIELDINDEX = 2
    TOWNNAME_FIELDINDEX = 1
    STREETNAME_FIELDINDEX = 3
    TYP_SO_FIELDINDEX = 4
    CISLO_DOMOVNI_FIELDINDEX = 5
    CISLO_ORIENTACNI_FIELDINDEX = 6
    ZNAK_CISLA_ORIENTACNIHO_FIELDINDEX = 7
    ZIP_CODE_FIELDINDEX = 8
    MOP_NUMBER_FIELDINDEX = 9


    def __init__(self, value, searchDB = True):
        self.type = 0
        self.value = value
        self.towns = []
        self.townParts = []
        self.streets = []
        self.number = None
        self.maxNumberLen = 0
        self.isNumberID = False
        self.isTextField = False
        self.searchDB = searchDB
        self.analyseValue()


    def matchPercent(self, candidateValue, fieldIndex, ignoreAccents = False):
        result = self._matchPercent(candidateValue, fieldIndex, ignoreAccents)
        if result == 0 and not ignoreAccents:
            result = self._matchPercent(candidateValue, fieldIndex, True)

        return result

    def _matchPercent(self, candidateValue, fieldIndex, ignoreAccents = False):
        candidateValue = unicode(candidateValue).lower()
        value = self.value
        if ignoreAccents:
            value = remove_accents(self.value)
            candidateValue = remove_accents(candidateValue)

        if self.type == AddressItem.ZIP:
            if fieldIndex != AddressItem.ZIP_CODE_FIELDINDEX or len(candidateValue) != 5:
                return 0
        else:
            if fieldIndex == AddressItem.GID_FIELDINDEX:
                if len(candidateValue) != len(value):
                    return 0
            if fieldIndex == AddressItem.ZIP:
                if len(candidateValue) == 5 and candidateValue == value:
                    return 1
                else:
                    return 0

        lowerValue = unicode(value).lower()
        if candidateValue.find(lowerValue) != 0:
            return 0
        else:
            return 1.0*len(lowerValue)/len(candidateValue)


    def __repr__(self):
        return self.__str__()


    def __str__(self):
        result = ""

        msgs =  {
            AddressItem.ZIP: "PSČ ",
            AddressItem.ORIENTATION_NUMBER: "č.or. ",
            AddressItem.ORIENTATION_NUMBER_SEPARATOR: "č.or. separator ",
            AddressItem.RECORD_NUMBER: RECORD_NUMBER_ID + " ",
            AddressItem.DESCRIPTION_NUMBER: DESCRIPTION_NUMBER_ID + " ",
            AddressItem.ORIENTATION_NUMBER_LETTER: "p.or. "
        }
        if self.type in msgs:
            result += msgs[self.type]

        if self.number == None:
            result += "'%s'" % self.value
            if self.searchDB and self.type <> AddressItem.ORIENTATION_NUMBER_SEPARATOR:
                result += '" ' + str(len(self.streets)) + "," + str(len(self.towns)) + \
                      "," + str(len(self.townParts))
        else:
            result += self.number

        return result


    def analyseValue(self):
        if isInt(self.value):
            self.number = self.value
        elif self.value == ORIENTATION_NUMBER_ID:
            self.type = AddressItem.ORIENTATION_NUMBER_SEPARATOR
        elif self.value == RECORD_NUMBER_ID:
            self.type = AddressItem.RECORD_NUMBER
            self.isNumberID = True
            self.maxNumberLen = RECORD_NUMBER_MAX_LEN
        elif self.value == DESCRIPTION_NUMBER_ID:
            self.type = AddressItem.DESCRIPTION_NUMBER
            self.isNumberID = True
            self.maxNumberLen = DESCRIPTION_NUMBER_MAX_LEN
        else:
            self.isTextField = True
            if self.searchDB:
                self.towns = ruianDatabase.getObecByName(self.value)
                self.streets = ruianDatabase.getUliceByName(self.value)
                self.townParts = ruianDatabase.getCastObceByName(self.value)


class _SearchItem:
    def __init__(self, item, text, fieldName):
        self.item = item
        self.text = text
        self.fieldName = fieldName


    def __repr__(self):
        return self.text + " (" + self.item.value + ")"


    def getWhereItem(self):
        if self.item == None:
            return ""
        else:
            return self.fieldName + "= '" + self.text + "'"


    def getID(self):
        return self.fieldName + ':' + self.text


def replaceByDict(str, valuesDict):
    for key, value in valuesDict.iteritems():
        str = str.replace(key, value)
    
    return str



def replaceByPairs(str, pairs):
    for pair in pairs:
        key, value = pair
        str = str.replace(key, value)

    return str



class AddressParser:
    def normaliseSeparators(self, address):
        address = replaceByPairs(address, [
            (ORIENTATION_NUMBER_ID, ',' + ORIENTATION_NUMBER_ID + ","),
            ("  ", " "),
            (" ,", ","),
            (", ", ","),
            ("\r\r", "\r"),
            ("\r", ","),
            ("\n\n", ","),
            ("\n", ","),
            (",,", ",")
        ])

        while address.find(",,") >= 0:
            address = address.replace(",,", ",")

        return address


    def normaliseDescriptionNumberID(self, address):
        return replaceByDict(address, {
            "čp ": DESCRIPTION_NUMBER_ID + " ",
            "č. p.": DESCRIPTION_NUMBER_ID,
            "čp.": DESCRIPTION_NUMBER_ID
        })


    def expandNadPod(self, address):
        return replaceByDict(address, {
            " n ": " nad ",
            " n.": " nad ",
            " p ": " pod ",
            " p.": " pod "
        })


    def normaliseRecordNumberID(self, address):
        address = replaceByDict(address, {
            "ev.č.":  RECORD_NUMBER_ID,
            "ev č.":  RECORD_NUMBER_ID,
            "evč.":   RECORD_NUMBER_ID,
            "eč.":    RECORD_NUMBER_ID,
            "ev. č.": RECORD_NUMBER_ID,
            "č. ev.": RECORD_NUMBER_ID,
            "čev.":   RECORD_NUMBER_ID
        })
        if address.find("č.ev") >= 0 and address.find("č.ev") != address.find(RECORD_NUMBER_ID):
            address = address.replace("č.ev",   RECORD_NUMBER_ID, 1)
        return address


    def separateNumbers(self, address):
        newAddress = ""
        wasNumber = False
        for i in range(len(address)):
            actChar = address[i:i+1]
            if "0123456789".find(actChar) >= 0:
                if i > 0 and not wasNumber:
                     newAddress += ","
                wasNumber = True
                newAddress += actChar
            elif wasNumber:
                newAddress += actChar + ","
                wasNumber = False
            else:
                newAddress += actChar

        return self.normaliseSeparators(newAddress)


    def normalize(self, address):
        address = self.normaliseSeparators(address)
        address = self.normaliseDescriptionNumberID(address)
        address = self.normaliseRecordNumberID(address)
        address = self.expandNadPod(address)
        address = self.separateNumbers(address)
        if address[len(address)-1:] == ",":
            address = address[:len(address)-1]

        return address


    def parse(self, address, searchDB = True):
        log.logger.openSection("AddressParser.parse('%s')" % address)
        normalizedAddress = self.normalize(address)
        stringItems = normalizedAddress.split(",")
        items = []
        for value in stringItems:
            item = AddressItem(value, searchDB)
            items.append(item)

        log.logger.closeSection("Done : %s" % str(items))
        return items


    def analyseItems(self, items):
        log.logger.openSection("AddressParser.analyseItems(%s)" % str(items))
        prevItem = None
        newItems = []
        nextItemToBeSkipped = False
        for item, index in zip(items, range(len(items))):
            if nextItemToBeSkipped:
                nextItemToBeSkipped = False
                continue

            if index == len(items) - 1:
                nextItem = None
            else:
                nextItem = items[index + 1]

            toBeSkipped = False

            if item.type == AddressItem.ORIENTATION_NUMBER_SEPARATOR:
                toBeSkipped = True
                if prevItem and prevItem.isNumberID:
                    prevItem.type = AddressItem.HOUSE_NUMBER

                if nextItem and nextItem.isNumberID:
                    nextItem.type = AddressItem.HOUSE_NUMBER

            if item.isNumberID:
                if nextItem == None or nextItem.number == None or len(nextItem.number) > item.maxNumberLen:
                    toBeSkipped = True
                    # Error, za indikátorem č.ev.,č.or.,/ nenásleduje číslice nebo je příliš dlouhá
                else:
                    item.number = nextItem.number
                    nextItemToBeSkipped = True

            elif item.number != None:
                if nextItem != None and nextItem.number != None and len(item.number) + len(nextItem.number) == ZIPCODE_LEN:
                    item.number += nextItem.number
                    nextItemToBeSkipped = True

                if len(item.number) == ZIPCODE_LEN:
                    item.type = AddressItem.ZIP
                elif len(item.number) <= HOUSE_NUMBER_MAX_LEN:
                    item.type = AddressItem.HOUSE_NUMBER
                else:
                    # Error, příliš dlouhé číslo domovní nebo evidenční
                    pass

            else:
                valueLength = len(item.value)
                if valueLength > 1:
                    header = item.value[:valueLength-1]
                    tail = item.value[valueLength-1:]
                    if header.isdigit():
                        item.value = header
                        item.type = AddressItem.ORIENTATION_NUMBER
                        item.number = header
                        item.maxNumberLen = ORIENTATION_NUMBER_MAX_LEN
                        item.isNumberID = True
                        item.isTextField = False
                        toBeSkipped = True
                        newItems.append(item)

                        letterItem = AddressItem(tail, False)
                        letterItem.type = AddressItem.ORIENTATION_NUMBER_LETTER
                        newItems.append(letterItem)

            prevItem = item
            if not toBeSkipped:
                newItems.append(item)


        log.logger.closeSection("Done : %s" % str(newItems))
        return newItems


    def analyse(self, address, searchDB = True):
        items = self.parse(address, searchDB)
        items = self.analyseItems(items)

        return items


    def old_getCombinedTextSearches(self, items):
        sqlList = []
        sqlSubList = []

        def addCombination(sqlCondition):
            #global sqlSubList
            if sqlSubList == []:
                sqlSubList.append(sqlCondition)
            else:
                for i in range(len(sqlSubList)):
                    sqlSubList[i] += " and " + sqlCondition

        def addCandidates(fieldName, list):
            if list != None and list != []:
                for item in list:
                    addCombination(fieldName + " = '" + item + "'")

        for item in items:
            if item.isTextField():
                sqlSubList = []
                addCandidates(TOWNNAME_FIELDNAME,   item.towns)
                addCandidates(TOWNPART_FIELDNAME,   item.townParts)
                addCandidates(STREETNAME_FIELDNAME, item.streets)

                if sqlList == []:
                    sqlList.extend(sqlSubList)
                else:
                    newList = []
                    for oldItem in sqlList:
                        for newItem in sqlSubList:
                            newList.append(oldItem + " and " + newItem)
                    sqlList = []
                    sqlList.extend(newList)
        return sqlList


    def getTextItems(self, items):
        result = []
        for item in items:
            if item.isTextField():
                result.append(item)
            if len(result) == MAX_TEXT_COUNT:
                break
        return result


    def getTextVariants(self, textItems):
        streets = []
        towns = []
        townParts = []

        for item in textItems:
            for street in item.streets:
                streets.append(_SearchItem(item, street, STREETNAME_FIELDNAME))
            for town in item.towns:
                towns.append(_SearchItem(item, town, TOWNNAME_FIELDNAME))
            for townPart in item.townParts:
                townParts.append(_SearchItem(item, townPart, TOWNPART_FIELDNAME))

        if streets == []:
            streets = [_SearchItem(None, None, None)]

        if towns == []:
            towns = [_SearchItem(None, None, None)]

        if townParts == []:
            townParts = [_SearchItem(None, None, None)]

        return (streets, towns, townParts)


    def expandedTextItems(self, searchItems):
        result = []
        for item in searchItems:
            for street in item.streets:
                result.append(_SearchItem(item, street, STREETNAME_FIELDNAME))

            for town in item.towns:
                result.append(_SearchItem(item, town, TOWNNAME_FIELDNAME))

            for townPart in item.townParts:
                result.append(_SearchItem(item, townPart, TOWNPART_FIELDNAME))

        return result


    def getCombinedTextSearches(self, items):
        textItems = self.getTextItems(items)
        sqlItems = []
        for item in textItems:
            sqlItems.append()

        return []


    def getCandidateValues(self, analysedItems):
        candidates = []

        sqlItems = []
        for item in analysedItems:
            if item.isTextField and len(item.value) >= 2:
                sqlItems.append("unaccent(searchstr) ilike unaccent('%" + item.value + "%')")

        if sqlItems:
            innerSql = "select explode_array({0}) from {1} where {2}".format(GIDS_FIELDNAME, FULLTEXT_TABLENAME, " and ".join(sqlItems))

            sql = "select {0}, {1}, {2}, {3}, {4}, {5}, {6}, {7}, {8}, {11} from {9} where gid IN ({10} limit 1000) order by {0}".format(
                GID_FIELDNAME, TOWNNAME_FIELDNAME, TOWNPART_FIELDNAME, STREETNAME_FIELDNAME, TYP_SO_FIELDNAME, \
                CISLO_DOMOVNI_FIELDNAME, CISLO_ORIENTACNI_FIELDNAME, ZNAK_CISLA_ORIENTACNIHO_FIELDNAME, ZIP_CODE_FIELDNAME, ADDRESSPOINTS_TABLENAME, str(innerSql), MOP_NUMBER)

            candidates = ruianDatabase.getQueryResult(sql)

        return candidates


    def compare(self, items, candidates, ignoreAccents = False):
        sumMatchPercent = 0
        numMatches = 0
        for item in items:
            found = False
            for candidate, fieldIndex in zip(candidates, range(len(candidates))):
                matchPercent = item.matchPercent(candidate, fieldIndex, ignoreAccents)
                if matchPercent > 0:
                    sumMatchPercent = sumMatchPercent + matchPercent
                    numMatches = numMatches + 1
                    found = True
                    break

            if not found:
                return 0

        return sumMatchPercent/numMatches


    def buildAddress(self, builder, candidates, withID, withDistance = False):
        items = []
        for item in candidates:
            if item[4] == "č.p.":
                houseNumber = str(item[5])
                recordNumber = ""
            else:
                houseNumber = ""
                recordNumber = str(item[5])

            mop = noneToString(item[9])
            if mop != "":
                pom = mop.split()
                districtNumber = pom[1]
            else:
                districtNumber = ""

            subStr = compileaddress.compileAddress(
                builder,
                noneToString(item[3]),
                houseNumber,
                recordNumber,
                noneToString(item[6]),
                noneToString(item[7]),
                str(item[8]),
                noneToString(item[1]),
                noneToString(item[2]),
                districtNumber
            )

            if withID:
                subStr = self.addId("id", str(item[0]), subStr, builder)

            if withDistance:
                subStr = self.addId("distance", str(item[10]), subStr, builder)

            items.append(subStr)
        return items


    def addId(self, id, value, str, builder):
        if builder.formatText == "json":
            return '\t"%s": %s,\n%s' % (id, value, str)
        elif builder.formatText == "xml":
            return '\t<%s>%s</%s>\n%s' % (id, value, id, str)
        else:
            return value + builder.lineSeparator + str


    def fullTextSearchAddress(self, address, ignoreAccents = False):
        log.logger.openSection("AddressParser.fullTextSearchAddress('%s')" % address)
        addressItems = self.analyse(address, False)
        candidates = self.getCandidateValues(addressItems)

        resultsDict = defaultdict(list)
        for candidate in candidates:
            matchPercent = self.compare(addressItems, candidate, ignoreAccents)
            if matchPercent > 0:
                if resultsDict.has_key(matchPercent):
                    resultsDict[matchPercent].append(candidate)
                else:
                    resultsDict[matchPercent] = [candidate]


        results = []

        exactMatchNeeded = False

        def addCandidate(key, candidate):
            if not results:
                global exactMatchNeeded
                exactMatchNeeded = key == 1

            continueLoop = not exactMatchNeeded or (exactMatchNeeded and key == 1)
            if continueLoop:
                results.append(candidate)
            return continueLoop

        for key in reversed(sorted(resultsDict)):
            candidateItem = resultsDict[key]
            if isinstance(candidateItem, list):
                for candidate in candidateItem:
                    addCandidate(key, candidate)
            else:
                addCandidate(key, candidateItem)

        log.logger.closeSection("Done:%s" % str(results))
        return results


def initModule():
    global ruianDatabase
    ruianDatabase = RUIANDatabase()


class FormalTester:
    def __init__(self, caption, desc, compilingPerson, tester):
        self.numTests = 0
        self.caption = caption
        self.desc = desc
        self.compilingPerson = compilingPerson
        self.tester = tester
        self.testsHTML = """
<table>
    <tr>
            <th>#</th><th></th><th>Vstup</th><th>Výsledek</th><th>Pozn</th>
    </tr>
"""

    def addTest(self, inputs, result, expectedResult, errorMessage = ""):
        self.numTests = self.numTests + 1

        if str(result) == expectedResult:
            status = "checked"
            print "   ok :", inputs, "-->", result
            expectedResultMessage = ""
        else:
            status = ""
            expectedResultMessage = " &lt; &gt; " + expectedResult
            print "chyba :", inputs, "-->", result, "<>", expectedResult, errorMessage
        self.testsHTML += "<tr>\n"
        self.testsHTML += "    <td>" + str(self.numTests) + "</td>"
        self.testsHTML += "    <td>" + '<input type="checkbox" value=""' + status + ' \>' + "</td>"

        self.testsHTML += "    <td>" + inputs + "</td>"
        self.testsHTML += "    <td>--> " + str(result) + expectedResultMessage + "</td>"
        self.testsHTML += "    <td>" + errorMessage + "</td>"
        self.testsHTML += "</tr>\n"


    def getHTML(self):
        result = """
<html>
    <head>
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
	    <meta http-equiv="X-UA-Compatible" content="IE=edge" />
	</head>
	<body>"""
        if self.caption != "": result += "<h1>" + self.caption + "</h1>\n"
        if self.desc != "": result += "<p>" + self.desc + "</p>\n"
        result += self.testsHTML + "</table>"
        result += """
    </body>
</html>"""

        return result


def testAnalyse():
    parser = AddressParser()
    tester = FormalTester("Rozpoznávání typů adresních položek",
"""Skupina testů zajišťujících rozpoznání jednotlivých typů adresních položek v adresním řetězci.
Jednotlivé testy spadají do kategorie tzv. "unit testů", tj. hodnoty a kombinace nemusí být zcela reálné, cílem je
úplná sada eliminující možné chyby.
V této skupině testů je také testováno párování identifikátorů jednotlivých položek se svými hodnotami.
""", "Ing. Tomáš Vacek", "Ing. Radek Makovec")

    def doTest(value, expectedValue, ErrorMessage = ""):
        tester.addTest(value, parser.analyse(value), expectedValue, ErrorMessage)

    doTest("Pod lesem 1370 č. ev. 1530 Lipník n ", '["Pod lesem", 1370, č.ev. 1530, "Lipník nad "]')

    doTest("3/13", "[3, č.or. 13]", "Rozpoznání čísla orientačního")
    doTest("3/ 13", "[3, č.or. 13]", "Rozpoznání čísla orientačního")
    doTest("3 / 13", "[3, č.or. 13]", "Rozpoznání čísla orientačního")

    doTest("č. p. 113 Bělá", '[č.p. 113, "Bělá"]', 'Rozpoznání čísla popisného')
    doTest("čp. 113 Bělá", '[č.p. 113, "Bělá"]', 'Rozpoznání čísla popisného')
    doTest("č.p. 113 Bělá", '[č.p. 113, "Bělá"]', 'Rozpoznání čísla popisného')
    doTest("č.p.113 Bělá", '[č.p. 113, "Bělá"]', 'Rozpoznání čísla popisného')
    doTest("čp 113 Bělá", '[č.p. 113, "Bělá"]', 'Rozpoznání čísla popisného')
    doTest("čp113 Bělá", '[č.p. 113, "Bělá"]', 'Rozpoznání čísla popisného')

    doTest("16300",  "[PSČ 16300]", 'Rozpoznání PSČ')
    doTest("1 6300", "[PSČ 16300]", 'Rozpoznání PSČ')
    doTest("16 300", "[PSČ 16300]", 'Rozpoznání PSČ')
    doTest("163 00", "[PSČ 16300]", 'Rozpoznání PSČ')
    doTest("1630 0", "[PSČ 16300]", 'Rozpoznání PSČ')

    doTest("Pod lesem 1370 č. ev. 1530, Březová", '["Pod lesem", 1370, č.ev. 1530, "Březová"]', 'Rozpoznání čísla evidenčního')
    doTest("Pod lesem 1370 č.ev. 1530, Březová", '["Pod lesem", 1370, č.ev. 1530, "Březová"]', 'Rozpoznání čísla evidenčního')
    doTest("Pod lesem 1370 č. ev.1530, Březová", '["Pod lesem", 1370, č.ev. 1530, "Březová"]', 'Rozpoznání čísla evidenčního')
    doTest("Pod lesem 1370 č.ev 1530, Březová", '["Pod lesem", 1370, č.ev. 1530, "Březová"]', 'Rozpoznání čísla evidenčního')
    doTest("Pod lesem 1370 č.ev1530, Březová", '["Pod lesem", 1370, č.ev. 1530, "Březová"]', 'Rozpoznání čísla evidenčního')
    doTest("Pod lesem 1370 čev.1530, Březová", '["Pod lesem", 1370, č.ev. 1530, "Březová"]', 'Rozpoznání čísla evidenčního')

    doTest("Roudnice n Labem", '["Roudnice nad Labem"]', "Chybný zápis nad")
    doTest("Roudnice n. Labem", '["Roudnice nad Labem"]', "Chybný zápis nad")

    doTest("Brněnská 1370 č. p. 113, Březová", '["Brněnská", 1370, č.p. 113, "Březová"]')

    doTest("Pod lesem 1370 č. ev. 1530 Svatý Jan p skalo", '["Pod lesem", 1370, č.ev. 1530, "Svatý Jan pod skalo"]')
    doTest("Pod lesem 1370 č. ev. 1530 Lipník n ", '["Pod lesem", 1370, č.ev. 1530, "Lipník nad "]')

    with codecs.open("parseaddress_tests.html", "w", "utf-8") as outFile:
        htmlContent = tester.getHTML()
        outFile.write(htmlContent.decode("utf-8"))
        outFile.close()


def testFullTextSearchAddress():
    parser = AddressParser()
    tester = FormalTester("Rozpoznávání typů adresních položek",
"""Skupina testů zajišťujících rozpoznání jednotlivých typů adresních položek v adresním řetězci.
Jednotlivé testy spadají do kategorie tzv. "unit testů", tj. hodnoty a kombinace nemusí být zcela reálné, cílem je
úplná sada eliminující možné chyby.
V této skupině testů je také testováno párování identifikátorů jednotlivých položek se svými hodnotami.
""", "Ing. Tomáš Vacek", "Ing. Radek Makovec")

    def doTest(value, expectedValue, ErrorMessage = ""):
        tester.addTest(value, parser.analyse(value), expectedValue, ErrorMessage)

    #parser.fullTextSearchAddress("Klostermannova 586, Hořovice, 26801")
    #parser.fullTextSearchAddress("Hořo, Klostermann 586, 26801")
    parser.fullTextSearchAddress("Hořo, Klostermann 7, 26801")
    parser.fullTextSearchAddress("Budovatelů 677")
    parser.fullTextSearchAddress("Budovatelů 676")
    parser.fullTextSearchAddress("Budovatelů 678")

    with codecs.open("parseaddress.html", "w", "utf-8") as outFile:
        htmlContent = tester.getHTML()
        outFile.write(htmlContent.decode("utf-8"))
        outFile.close()


def testAddresses():
    addresses = [
        'Hamerská 599a',
        "Chvalínská 2078",
        "Podlusky 2278",
        "Opava, ostravská 350",
        "Fialková, Čakovičky",
        "Budovatelů, Chodov 677",
        "Klobouky u Brna 884",
        u"Gočárova třída 516/18 50002 Hradec Králové",
        "Mezilesní 550/18",
        "U kamene 181",
        "Na lánech 598/13",
        "1 Cílkova",
        "67 budovatelů"
    ]
    parser = AddressParser()

    foundCount = 0
    for address in addresses:
        addressItems = parser.fullTextSearchAddress(address)
        if addressItems:
            foundCount += 1
        log.logger.debug("%s'%s': %s" % (["", "NOT FOUND!!! "][int(addressItems==[])], address, str(addressItems)))
        break

    if foundCount == len(addresses):
        log.logger.info("All %d addresses found" % foundCount)
    else:
        log.logger.info("Found %d out of %d addresses" % (foundCount, len(addresses)))


initModule()

def main():
    #testAnalyse()
    #testFullTextSearchAddress()
    testAddresses()


if __name__ == '__main__':
    import sys
    reload(sys)
    sys.setdefaultencoding('utf-8')

    log.createLogger("parseaddress.log")
    import logging
    log.logger.setLevel(logging.DEBUG)

    main()