# -*- coding: utf-8 -*-
# Creates supporting tables for full text search and autocomplete functions
__author__ = 'raugustyn'

import psycopg2
import os, codecs, sys

from config import config
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
    path = os.path.dirname(__file__)
    sqlFileName = path + os.sep + sqlFileName
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
    sys.stdout.write("Creating temporary table _ac_gids")
    cursor = connection.cursor()
    try:
        cursor.execute("drop table if exists _ac_gids;")
        cursor.execute("CREATE TABLE _ac_gids (gid integer NOT NULL, address text);")
        print " - done."
    finally:
        cursor.close()

def getAddressRows(connection):
    sys.stdout.write("Retrieving address rows")
    cursor = connection.cursor()
    try:
        query = 'select nazev_ulice, cast(cislo_domovni as text), nazev_obce, cast(psc as text), cast(cislo_orientacni as text), znak_cisla_orientacniho, nazev_casti_obce, typ_so, nazev_mop, gid from address_points '
        cursor.execute(query)
        print " - hotovo."
        return cursor
    except:
        print "Error:Selecting address rows failed."
        exitApp()

def renameTempTable(connection):
    sys.stdout.write("Renaming table _ac_gids to ac_gids.")
    cursor = connection.cursor()
    cursor.execute("drop table if exists ac_gids;")
    cursor.execute("alter table _ac_gids rename to ac_gids;")
    cursor.close()
    print " - hotovo."

def buildGIDsTable():
    print "Vytvářím tabulku ac_gids"
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
                    insertSQL = "INSERT INTO _ac_gids (gid, address) VALUES (%s, '%s')" % (gid, rowLabel)
                    insertCursor.execute(insertSQL)
                    connection.commit()
                    if gaugecount >= 1000:
                        gaugecount = 0
                        print str(row_count) + " rows"

                except psycopg2.Error as e:
                    print "Error: " + str(row_count) + " " + insertSQL + " failed. " + e.pgerror
                    exitApp()
                    pass

            print "Done - %d rowns inserted." % row_count

        finally:
            cursor.close()

        print "Renaming table ac_gids to ac_gids."
        renameTempTable(connection)

        print "Table ac_gids done."
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
        SQLInfo("momc.sql", "Table ui_momc"),
        SQLInfo("mop.sql" , "Table ui_mop"),
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