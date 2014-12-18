# -*- coding: utf-8 -*-
# Creates supporting tables for full text search and autocomplete functions
__author__ = 'raugustyn'

import psycopg2
import os, codecs, sys

from config import config
from SharedTools.config import getRUIANServicesSQLScriptsPath

import HTTPShared
import compileaddress

def exitApp():
    sys.exit()

def execSQLScript(sql):
    sys.stdout.write("   Executing SQL commands")
    connection = psycopg2.connect(host=config.databaseHost, database=config.databaseName, port=config.databasePort,
                           user=config.databaseUserName, password=config.databasePassword)
    cursor = connection.cursor()
    try:
        if (True):
            cursor.execute(sql)
            connection.commit()
        else:
            sqlItems = sql.split(";")
            for sqlItem in sqlItems:
                cursor.execute(sqlItem)
                connection.commit()

    except psycopg2.Error as e:
        print "ERROR:" + e.pgerror
    finally:
        cursor.close()
        connection.close()
    print " - done."
    pass

def execSQLScriptFile(sqlFileName, msg):
    print msg
    sqlFileName = getRUIANServicesSQLScriptsPath() + sqlFileName
    if not os.path.exists(sqlFileName):
        print "ERROR: File %s not found." % sqlFileName
        exitApp()

    sys.stdout.write("   Loading SQL commands from %s" % sqlFileName)
    inFile = codecs.open(sqlFileName, "r", "utf-8")
    sql = inFile.read()
    inFile.close()
    print " - done."
    execSQLScript(sql)

def createTempTable(connection):
    sys.stdout.write("Creating table ac_gids")
    cursor = connection.cursor()
    try:
        cursor.execute("drop table if exists ac_gids;")
        cursor.execute("CREATE TABLE ac_gids (gid integer NOT NULL, address text);")
        print " - done."
    finally:
        cursor.close()

def getAddressRows(connection):
    sys.stdout.write("Retrieving address rows")
    cursor = connection.cursor()
    try:
        query = 'select nazev_ulice, cast(cislo_domovni as text), nazev_obce, cast(psc as text), cast(cislo_orientacni as text), znak_cisla_orientacniho, nazev_casti_obce, typ_so, nazev_mop, gid from address_points '
        cursor.execute(query)
        print " - done."
        return cursor
    except:
        print "Error:Selecting address rows failed."
        exitApp()

def renameTempTable(connection):
    sys.stdout.write("Renaming table _ac_gids to ac_gids.")
    cursor = connection.cursor()
    cursor.execute("drop table if exists ac_gids;alter table _ac_gids rename to ac_gids;")
    cursor.close()
    print " - done."

def buildTownsNoStreets():

    def _createTable(connection):
        sys.stdout.write("Creating table ac_townsnostreets")
        cursor = connection.cursor()
        try:
            cursor.execute("drop table if exists ac_townsnostreets;")
            cursor.execute("CREATE TABLE ac_townsnostreets (nazev_obce text, nazev_casti_obce text);")
            print " - done."
        finally:
            cursor.close()

    def _getRows(connection):
        sys.stdout.write("Retrieving records to be processes")
        cursor = connection.cursor()
        try:
            query = 'select nazev_ulice, nazev_casti_obce, nazev_obce from address_points group by nazev_casti_obce, nazev_ulice, nazev_obce order by nazev_casti_obce, nazev_ulice, nazev_obce'
            cursor.execute(query)
            print " - done."
            return cursor
        except:
            print "Error:Selecting towns with no streets failed."
            exitApp()

    print "Building table ac_townsnostreets"
    print "------------------------"
    connection = psycopg2.connect(
        host = config.databaseHost,
        database = config.databaseName,
        port = config.databasePort,
        user = config.databaseUserName, password = config.databasePassword
    )
    try:
        #_createTable(connection)
        cursor = _getRows(connection)

        try:
            if cursor == None: return

            print "Inserting rows"
            print "----------------------"
            insertCursor = connection.cursor()

            def insertRow(nazev_casti_obce, nazev_obce):
                insertSQL = "INSERT INTO ac_townsnostreets (nazev_casti_obce, nazev_obce) VALUES ('%s', '%s')" % (nazev_casti_obce, nazev_obce)
                insertCursor.execute(insertSQL)
                connection.commit()
                pass

            row_count = 0
            gaugecount = 0
            last_nazev_casti_obce = None
            last_nazev_obce = None
            numStreets = 0
            for row in cursor:
                gaugecount += 1
                try:
                    nazev_ulice, nazev_casti_obce, nazev_obce = row

                    if (last_nazev_casti_obce == None or last_nazev_casti_obce == nazev_casti_obce) and \
                        (last_nazev_obce == None or last_nazev_obce == nazev_obce):
                        if nazev_ulice != None and nazev_ulice <> "": numStreets = numStreets + 1
                    else:
                        if last_nazev_casti_obce != "":
                            if numStreets == 0:
                                insertRow(nazev_casti_obce, nazev_obce)
                                row_count += 1

                        numStreets = 0
                        last_nazev_casti_obce = None
                        last_nazev_obce = None

                    last_nazev_casti_obce = nazev_casti_obce
                    last_nazev_obce = nazev_obce


                    if gaugecount >= 1000:
                        gaugecount = 0
                        print str(row_count) + " rows"

                except psycopg2.Error as e:
                    print "Error: " + str(row_count) + e.pgerror
                    exitApp()
                    pass

            print "Done - %d rows inserted." % row_count

        finally:
            cursor.close()



    finally:
        connection.close()

def buildGIDsTable():
    print "Building table ac_gids"
    print "------------------------"
    connection = psycopg2.connect(
        host = config.databaseHost,
        database = config.databaseName,
        port = config.databasePort,
        user = config.databaseUserName, password = config.databasePassword
    )
    try:
        createTempTable(connection)

        cursor = getAddressRows(connection)
        try:
            if cursor == None: return

            print "Inserting rows"
            print "----------------------"
            insertCursor = connection.cursor()
            builder = HTTPShared.MimeBuilder("texttoonerow")
            row_count = 0
            gaugecount = 0

            for row in cursor:
                row_count += 1
                gaugecount += 1
                try:
                    street, houseNumber, locality, zipCode, orientationNumber, orientationNumberCharacter, localityPart, typ_so, nazev_mop, gid = row
                    houseNumber, recordNumber = HTTPShared.analyseRow(typ_so, houseNumber)
                    districtNumber = HTTPShared.extractDictrictNumber(nazev_mop)

                    rowLabel = compileaddress.compileAddress(builder, street, houseNumber, recordNumber, orientationNumber, orientationNumberCharacter, zipCode, locality, localityPart, districtNumber)
                    insertSQL = "INSERT INTO ac_gids (gid, address) VALUES (%s, '%s')" % (gid, rowLabel)
                    insertCursor.execute(insertSQL)
                    connection.commit()
                    if gaugecount >= 1000:
                        gaugecount = 0
                        print str(row_count) + " rows"

                except psycopg2.Error as e:
                    print "Error: " + str(row_count) + " " + insertSQL + " failed. " + e.pgerror
                    exitApp()
                    pass

            print "Done - %d rows inserted." % row_count

        finally:
            cursor.close()

        #renameTempTable(connection)

        print "Building table ac_gids done."
    finally:
        connection.close()
    pass

class SQLInfo:
    def __init__(self, fileName, description):
        self.fileName = fileName
        self.description = description

def buildServicesTables():
    scriptList = [
        SQLInfo("TypStObjektu.sql", "Table typ_st_objektu"),
        SQLInfo("AddressPoints.sql" , "Table address_points"),
        SQLInfo("FullText.sql" , "Table fulltext"),
        SQLInfo("ExplodeArray.sql" , "Table explode_array"),
        SQLInfo("gids.sql" , "Table gids")
    ]

    for sqlInfo in scriptList:
        execSQLScriptFile(sqlInfo.fileName, sqlInfo.description)

def buildAutocompleteTables():
    execSQLScriptFile("AutocompleteTables.sql", "Autocomplete tables.")
    buildGIDsTable()

def buildAll():
    buildServicesTables()
    buildAutocompleteTables()
    pass

if __name__ == '__main__':
    import sys
    reload(sys)
    sys.setdefaultencoding('utf-8')
    buildAll()

