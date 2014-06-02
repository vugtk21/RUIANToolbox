# -*- coding: utf-8 -*-
__author__ = 'raugustyn'

import psycopg2
import codecs

ORIENTATION_NUMBER_ID = "/"
RECORD_NUMBER_ID = "č.ev."
DESCRIPTION_NUMBER_ID = "č.p."
RECORD_NUMBER_MAX_LEN = 4
ORIENTATION_NUMBER_MAX_LEN = 3
DESCRIPTION_NUMBER_MAX_LEN = 3
HOUSE_NUMBER_MAX_LEN = 4
ZIPCODE_LEN = 5

class RUIANDatabase():
    DATABASE_HOST = "localhost"
    PORT          = "5432"
    DATABASE_NAME = "adresspoints"
    USER_NAME     = "postgres"
    PASSWORD      = "ahoj"


    def __init__(self):
        self.conection = psycopg2.connect(host = self.DATABASE_HOST, database = self.DATABASE_NAME, port = self.PORT, user = self.USER_NAME, password = self.PASSWORD)

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
        cursor.execute("SELECT nazev_obce FROM obce WHERE nazev_obce ilike '%" + name + "%' limit 25")

        rows = []
        row_count = 0
        for row in cursor:
              row_count += 1
              rows.append(row[0])
        return rows

    def getUliceByName(self, name):
        cursor = self.conection.cursor()
        cursor.execute("SELECT nazev_ulice FROM ulice WHERE nazev_ulice ilike '%" + name + "%' limit 25")

        rows = []
        row_count = 0
        for row in cursor:
              row_count += 1
              rows.append(row[0])
        return rows

    def getCastObceByName(self, name):
        cursor = self.conection.cursor()
        cursor.execute("SELECT nazev_casti_obce FROM casti_obce WHERE nazev_casti_obce ilike '%" + name + "%' limit 25")

        rows = []
        row_count = 0
        for row in cursor:
              row_count += 1
              rows.append(row[0])
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
    #try:
    #    v = int(value)
    #    return True
    #except ValueError:
    #    return False


class AddressItem:
    def __init__(self, value):
        self.value = value
        self.town = None
        self.townPart = None
        self.street = None
        self.isRecordNumber = False
        self.isOrientationNumber = False
        self.isDescriptionNumber = False
        self.isZIP = False
        self.isHouseNumber = False
        self.number = None
        self.maxNumberLen = 0
        self.isNumberID = False
        self.analyseValue()

    def __repr__(self):
        result = ""
        if self.isZIP: result += "PSČ "

        if self.isOrientationNumber: result += "č.or. "

        if self.isRecordNumber: result += RECORD_NUMBER_ID + " "

        if self.isDescriptionNumber: result += DESCRIPTION_NUMBER_ID + " "

        if self.number == None:
            result += '"' + self.value + '"'
        else:
            result += self.number

        return result

    def __str__(self):
        result = ""
        if self.isZIP: result += "PSČ "

        if self.isOrientationNumber: result += "č.or. "

        if self.isRecordNumber: result += RECORD_NUMBER_ID + " "

        if self.isDescriptionNumber: result += DESCRIPTION_NUMBER_ID + " "

        if self.number == None:
            result += '"' + self.value + '" ' + str(len(self.street)) + "," + str(len(self.town)) + "," + str(len(self.townPart))
        else:
            result += self.number

        return result

    def analyseValue(self):
        if isInt(self.value):
            self.number = self.value
            pass
        elif self.value == ORIENTATION_NUMBER_ID:
            self.isOrientationNumber = True
            self.isNumberID = True
            self.maxNumberLen = ORIENTATION_NUMBER_MAX_LEN
        elif self.value == RECORD_NUMBER_ID:
            self.isRecordNumber = True
            self.isNumberID = True
            self.maxNumberLen = RECORD_NUMBER_MAX_LEN
        elif self.value == DESCRIPTION_NUMBER_ID:
            self.isDescriptionNumber = True
            self.isNumberID = True
            self.maxNumberLen = DESCRIPTION_NUMBER_MAX_LEN
        else:
            self.town = ruianDatabase.getObecByName(self.value)
            self.street = ruianDatabase.getUliceByName(self.value)
            self.townPart = ruianDatabase.getCastObceByName(self.value)

class AddressParser:
    def normaliseSeparators(self, address):
        address = address.replace(ORIENTATION_NUMBER_ID, " " + ORIENTATION_NUMBER_ID)
        address = address.replace("  ", " ")

        address = address.replace(",,", ",")
        address = address.replace(" ,", ",")
        address = address.replace(", ", ",")

        address = address.replace("\r\r", "\r")
        address = address.replace("\r", ",")

        address = address.replace("\n\n", ",")
        address = address.replace("\n", ",")

        return address

    def normaliseDescriptionNumberID(self, address):
        address = address.replace("čp ", DESCRIPTION_NUMBER_ID + " ")
        address = address.replace("č. p.", DESCRIPTION_NUMBER_ID)
        address = address.replace("čp.", DESCRIPTION_NUMBER_ID)
        return address

    def expandNadPod(self, address):
        address = address.replace(" n ", " nad ")
        address = address.replace(" n.", " nad ")
        address = address.replace(" p ", " pod ")
        address = address.replace(" p.", " pod ")
        return address

    def normaliseRecordNumberID(self, address):
        address = address.replace("ev.č.",  RECORD_NUMBER_ID)
        address = address.replace("ev č.",  RECORD_NUMBER_ID)
        address = address.replace("evč.",   RECORD_NUMBER_ID)
        address = address.replace("eč.",    RECORD_NUMBER_ID)
        address = address.replace("ev. č.", RECORD_NUMBER_ID)
        address = address.replace("č. ev.", RECORD_NUMBER_ID)
        address = address.replace("čev.",   RECORD_NUMBER_ID)
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

        return address

    def parse(self, address):
        address = self.normalize(address)
        stringItems = address.split(",")
        items = []
        for value in stringItems:
            item = AddressItem(value)
            items.append(item)
        return items

    def analyseItems(self, items):
        newItems = []
        index = 0
        nextItemToBeSkipped = False
        for item in items:
            if nextItemToBeSkipped:
                nextItemToBeSkipped = False
                continue

            if index == len(items) - 1:
                nextItem = None
            else:
                nextItem = items[index + 1]

            toBeSkipped = False
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
                    item.isZIP = True
                elif len(item.number) <= HOUSE_NUMBER_MAX_LEN:
                    item.isHouseNumber = True
                else:
                    # Error, příliš dlouhé číslo domovní nebo evidenční
                    pass
            else:
                #else textový řetezec
                pass

            if not toBeSkipped:
                newItems.append(item)

            index = index + 1

        return newItems


    def analyse(self, address):
        items = self.parse(address)
        return self.analyseItems(items)

    def fullTextSearchAddress(self, address):
        items = self.analyse(address)
        for item in items:
            print str(item)
        return ""

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
    doTest("Pod lesem 1370 čev1530, Březová", '["Pod lesem", 1370, č.ev. 1530, "Březová"]', 'Rozpoznání čísla evidenčního')
    doTest("Pod lesem 1370 čev.1530, Březová", '["Pod lesem", 1370, č.ev. 1530, "Březová"]', 'Rozpoznání čísla evidenčního')

    doTest("Roudnice n Labem", '["Roudnice nad Labem"]', "Chybný zápis nad")
    doTest("Roudnice n. Labem", '["Roudnice nad Labem"]', "Chybný zápis nad")

    doTest("Brněnská 1370 č. p. 113, Březová", '["Brněnská", 1370, č.p. 113, "Březová"]')

    doTest("Pod lesem 1370 č. ev. 1530 Svatý Jan p skalo", '["Pod lesem", 1370, č.ev. 1530, "Svatý Jan pod skalou"]')
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

    parser.fullTextSearchAddress("Klostermannova 586, Hořovice")
    #parser.fullTextSearchAddress("Hořo, Klostermann 586")

    with codecs.open("parseaddress_FullTextSearchTests.html", "w", "utf-8") as outFile:
        htmlContent = tester.getHTML()
        outFile.write(htmlContent.decode("utf-8"))
        outFile.close()

def main():
    initModule()
    #testAnalyse()
    testFullTextSearchAddress()

if __name__ == '__main__':
    main()