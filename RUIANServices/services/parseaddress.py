# -*- coding: utf-8 -*-
__author__ = 'raugustyn'

import psycopg2

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
        cursor.execute("SELECT obce FROM obce WHERE nazev_obce ilike '%" + name + "%' limit 25")

        rows = []
        row_count = 0
        for row in cursor:
              row_count += 1
              data = row[0]
              data = data[1:len(data) - 1]
              rows.append(data)
        return rows

    def getUliceByName(self, name):
        cursor = self.conection.cursor()
        cursor.execute("SELECT nazev_ulice FROM ulice WHERE nazev_ulice ilike '%" + name + "%' limit 25")

        rows = []
        row_count = 0
        for row in cursor:
              row_count += 1
              data = row[0]
              data = data[1:len(data) - 1]
              rows.append(data)
        return rows

    def getCastObceByName(self, name):
        cursor = self.conection.cursor()
        cursor.execute("SELECT nazev_casti_obce FROM casti_obce WHERE nazev_casti_obce ilike '%" + name + "%' limit 25")

        rows = []
        row_count = 0
        for row in cursor:
              row_count += 1
              data = row[0]
              data = data[1:len(data) - 1]
              rows.append(data)
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


ORIENTATION_NUMBER_SEPARATOR = "/"
RECORD_NUMBER_ID = "č.ev."
DESCRIPTION_NUMBER_ID = "č.p."

class AddressItem:
    def __init__(self, value):
        self.value = value
        self.town = None
        self.townPart = None
        self.street = None
        self.isRecordNumber = False
        self.isOrientationNumber = False
        self.isZIP = False
        self.isHouseNumber = False
        self.number = None
        self.orientationNumberID = False
        self.recordNumberID = False
        self.analyseValue()

    def __repr__(self):
        result = ""
        if self.isZIP: result += "PSČ "

        if self.isOrientationNumber: result += ORIENTATION_NUMBER_SEPARATOR

        if self.isRecordNumber: result += RECORD_NUMBER_ID + " "

        #if self.isHouseNumber: result += DESCRIPTION_NUMBER_ID + " "

        if self.number == None:
            result += '"' + self.value + '"'
        else:
            result += self.number

        return result

    def analyseValue(self):
        if isInt(self.value):
            self.number = self.value
            pass
        elif self.value == ORIENTATION_NUMBER_SEPARATOR:
            self.orientationNumberID = True
        elif self.value == RECORD_NUMBER_ID:
            self.recordNumberID = True
        else:
            self.town = ruianDatabase.getObecByName(self.value)
            self.street = ruianDatabase.getUliceByName(self.value)
            self.townPart = ruianDatabase.getCastObceByName(self.value)

class AddressParser:
    RECORD_NUMBER_MAX_LEN = 4
    ORIENTATION_NUMBER_MAX_LEN = 3
    HOUSE_NUMBER_MAX_LEN = 4
    ZIPCODE_LEN = 5


    def normaliseSeparators(self, address):
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
        address = address.replace("čp.", DESCRIPTION_NUMBER_ID)
        return address

    def expandNad(self, address):
        address = address.replace(" n ", " nad ")
        address = address.replace(" n.", " nad ")
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
        address = self.expandNad(address)
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
            if item.orientationNumberID or item.recordNumberID:
                if item.orientationNumberID:
                    maxLen = self.ORIENTATION_NUMBER_MAX_LEN
                else:
                    maxLen = self.RECORD_NUMBER_MAX_LEN

                if nextItem == None or nextItem.number == None or len(nextItem.number) > maxLen:
                    toBeSkipped = True
                    # Error, za indikátorem č.ev. nebo č.or. nenásleduje číslice
                else:
                    item.number = nextItem.number
                    nextItemToBeSkipped = True
                    if item.orientationNumberID:
                        item.isOrientationNumber = True
                    else:
                        item.isRecordNumber = True

            elif item.number != None:
                if len(item.number) == 3 and nextItem.number != None and len(nextItem.number) == 2:
                    item.number += nextItem.number
                    nextItemToBeSkipped = True

                if len(item.number) == self.ZIPCODE_LEN:
                    item.isZIP = True
                elif len(item.number) <= self.HOUSE_NUMBER_MAX_LEN:
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

    def testAnalyse(self, address, expectedResult):
        result = self.analyse(address)
        if str(result) == expectedResult:
            print "   ok :", address, "-->", result
        else:
            print "chyba :", address, "-->", result, "<>", expectedResult

def initModule():
    global ruianDatabase
    ruianDatabase = RUIANDatabase()

def main():
    initModule()
    parser = AddressParser()
    #parser.testAnalyse("16300", "[PSČ 16300]")
    #parser.testAnalyse("163 00", "[PSČ 16300]")
    #parser.testAnalyse("Pod lesem 1370 č. ev. 1530, Březová", '["Pod lesem", 1370, č.ev. 1530, "Březová"]')
    parser.testAnalyse("Brněnská 1370 č. p. 113, Březová", '["Brněnská", 1370, "č.p.", 113, "Březová"]')
    #parser.testAnalyse("Pod lesem 1370 č. ev. 1530 Roudnice nad Labem", '["Pod lesem", 1370, č.ev. 1530, "Roudnice nad Labem"]')
    #parser.testAnalyse("Pod lesem 1370 č. ev. 1530 Svatý Jan p skalou", '["Pod lesem", 1370, č.ev. 1530, "Svatý Jan pod skalou"]')
    #parser.testAnalyse("Pod lesem 1370 č. ev. 1530 Lipník n ", '["Pod lesem", 1370, č.ev. 1530, "Lipník nad "]')

if __name__ == '__main__':
    main()