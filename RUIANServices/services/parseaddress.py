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
        cursor.execute("SELECT obce FROM obce WHERE nazev_obce ilike '%" + name + "%'")

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
        cursor.execute("SELECT nazev_ulice FROM ulice WHERE nazev_ulice ilike '%" + name + "%'")

        rows = []
        row_count = 0
        for row in cursor:
              row_count += 1
              data = row[0]
              data = data[1:len(data) - 1]
              rows.append(data)
        return rows

def isInt(value):
    try:
        v = int(value)
        return True
    except ValueError:
        return False

class AddressParser:
    NUMBER_CHARS = "0123456789"
    ORIENTATION_NUMBER_SEPARATOR = "/"
    DESCRIPTION_NUMBER_ID = "č.p."
    RECORD_NUMBER_ID = "č.ev."

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
        address = address.replace("čp ", self.DESCRIPTION_NUMBER_ID + " ")
        address = address.replace("čp.", self.DESCRIPTION_NUMBER_ID)
        return address

    def expandNadPod(self, address):
        address = address.replace(" n ", " nad ")
        address = address.replace(" n.", " nad ")
        address = address.replace(" p ", " pod ")
        address = address.replace(" p.", " pod ")
        return address

    def normaliseRecordNumberID(self, address):
        address = address.replace("ev.č.",  self.RECORD_NUMBER_ID)
        address = address.replace("ev č.",  self.RECORD_NUMBER_ID)
        address = address.replace("evč.",   self.RECORD_NUMBER_ID)
        address = address.replace("eč.",    self.RECORD_NUMBER_ID)
        address = address.replace("ev. č.", self.RECORD_NUMBER_ID)
        address = address.replace("č. ev.", self.RECORD_NUMBER_ID)
        address = address.replace("čev.",   self.RECORD_NUMBER_ID)
        return address

    def separateNumbers(self, address):
        newAddress = ""
        wasNumber = False
        for i in range(0, len(address)):
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
        parsed = []
        self.number = ""

        address = self.normaliseSeparators(address)
        address = self.normaliseDescriptionNumberID(address)
        address = self.normaliseRecordNumberID(address)
        address = self.expandNadPod(address)
        address = self.separateNumbers(address)

        return address

    def search(self, address):
        address = self.normalize(address)
        items = address.split(",")

        db = RUIANDatabase()
        for item in items:
            if isInt(item):
                pass
            elif item == self.ORIENTATION_NUMBER_SEPARATOR:
                pass
            elif item == self.RECORD_NUMBER_ID:
                pass
            else:
                obce = db.getObecByName(item)
                if obce <> []:
                    print "Obec:", obce
                ulice = db.getUliceByName(item)
                if ulice <> []:
                    print "ulice:", ulice
        db = None
        print items


parser = AddressParser()
parser.search("Pod lesem 1370 č. ev. 1530, Březová")
parser.search("Brněnská 1370 č. p. 113, Březová")
parser.search("Pod lesem 1370 č. ev. 1530 Roudnice nad Labem")
parser.search("Pod lesem 1370 č. ev. 1530 Svatý Jan p skalou")
parser.search("Pod lesem 1370 č. ev. 1530 Lipník n ")