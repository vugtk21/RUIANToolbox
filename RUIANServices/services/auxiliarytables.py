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
    sys.stdout.write("   Executing script")
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
    print " - Done."
    pass

def execSQLScriptFile(sqlFileName, msg):
    print "%s - %s" % (msg, sqlFileName)
    if not os.path.exists(sqlFileName):
        print "ERROR: File %s not found." % sqlFileName
        exitApp()

    sys.stdout.write("   Loading script")
    inFile = codecs.open(sqlFileName, "r", "utf-8")
    sql = inFile.read()
    inFile.close()
    print " - Done."
    execSQLScript(sql)

def createTempTable(connection):
    sys.stdout.write("Creating temporary table _ac_gids")
    cursor = connection.cursor()
    try:
        cursor.execute("drop table if exists _ac_gids;")
        cursor.execute("CREATE TABLE _ac_gids (gid integer NOT NULL, address text);")
        print " - Done."
    finally:
        cursor.close()

def getAddressRows(connection):
    sys.stdout.write("Retrieving address rows")
    cursor = connection.cursor()
    try:
        query = 'select nazev_ulice, cast(cislo_domovni as text), nazev_obce, cast(psc as text), cast(cislo_orientacni as text), znak_cisla_orientacniho, nazev_casti_obce, typ_so, nazev_mop, gid from address_points '
        cursor.execute(query)
        print " - Done."
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
    print " - Done."

def buildGIDsTable():
    print "Building ac_gids table"
    print "----------------------"
    connection = psycopg2.connect(
        host = config.databaseHost,
        database = config.databaseName,
        port = config.databasePort,
        user = config.databaseUserName, password = config.databasePassword
    )
    try:
        createTempTable(connection)

        print "Selecting source rows"
        cursor = getAddressRows(connection)
        if cursor == None: return

        print "Inserting rows"
        print "----------------------"
        insertCursor = connection.cursor()
        builder = HTTPShared.MimeBuilder("texttoonerow")
        try:
            row_count = 0
            gaugecount = 0

            for row in cursor:
                row_count += 1
                gaugecount += 1
                street, houseNumber, locality, zipCode, orientationNumber, orientationNumberCharacter, localityPart, typ_so, nazev_mop, gid = row
                houseNumber, recordNumber = HTTPShared.analyseRow(typ_so, houseNumber)
                districtNumber = HTTPShared.extractDictrictNumber(nazev_mop)

                rowLabel = compileaddress.compileAddress(builder, street, houseNumber, recordNumber, orientationNumber, orientationNumberCharacter, zipCode, locality, localityPart, districtNumber)
                insertSQL = "INSERT INTO _ac_gids (gid, address) VALUES (%s, '%s')" % (gid, rowLabel)
                insertCursor.execute(insertSQL)
                connection.commit()
                if gaugecount >= 1000:
                    gaugecount = 0
                    print row_count + " rows"
            print "Done - " + str(row_count) + " inserted."

        except:
            print "Error: " + insertSQL + " failed."
            exitApp()
        finally:
            cursor.close()

        renameTempTable(connection)

        print "Done building ac_gids table"
    finally:
        connection.close()
    pass

class SQLInfo:
    def __init__(self, fileName, description):
        self.fileName = fileName
        self.description = description

def buildServicesTables():
    scriptList = [
        SQLInfo("TypStObjektu.sql", u"Číselník typu stavebního objektu typ_st_objektu"),
        SQLInfo("momc.sql", u"Číselník městských částí ui_momc"),
        SQLInfo("mop.sql" , u"Číselník městských částí v Praze ui_mop"),
        SQLInfo("AddressPoints.sql" , u"Tabulka adresních bodů address_points"),
        SQLInfo("FullText.sql" , u"Tabulka pro fulltextové vyhledávání fulltext"),
        SQLInfo("ExplodeArray.sql" , u"Funkce pro rozbalování souřadnic explode_array"),
        SQLInfo("gids.sql" , u"Tabulka RÚIAN ID gids")
    ]

    for sqlInfo in scriptList:
        execSQLScriptFile(sqlInfo.fileName, sqlInfo.description)

def buildAutocompleteTables():
    execSQLScriptFile("AutocompleteTables.sql", u"Tabulky pro HTML našeptávače")
    buildGIDsTable()

def buildAll():
    buildServicesTables()
    buildAutocompleteTables
    pass

if __name__ == '__main__':
    import sys
    reload(sys)
    sys.setdefaultencoding('utf-8')
    buildAll()
