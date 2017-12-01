# -*- coding: utf-8 -*-
# Creates supporting tables for full text search and autocomplete functions
__author__ = 'raugustyn'

import psycopg2
import os, codecs, sys

from config import config

import shared; shared.setupPaths()
from sharedtools.log import logger

from sharedtools.config import getRUIANServicesSQLScriptsPath

import HTTPShared
import compileaddress

def exitApp():
    sys.exit()

def logPsycopg2Error(e):
    if e:
        if e.pgerror:
            msg = str(e.pgerror)
        else:
            msg = str(e)
    else:
        msg = "Not specified"
    logger.error("Database error:" + msg)

def execSQLScript(sql):
    logger.info("   Executing SQL commands")
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
        logPsycopg2Error(e)
    finally:
        cursor.close()
        connection.close()
    logger.info("   Executing SQL commands - done.")
    pass

def execSQLScriptFile(sqlFileName, msg, exitIfFileNotFound = True):
    logger.info(msg)
    sqlFileName = getRUIANServicesSQLScriptsPath() + sqlFileName
    logger.info("   Loading SQL commands from %s" % sqlFileName)

    if not os.path.exists(sqlFileName):
        if exitIfFileNotFound:
            logger.error("ERROR: File %s not found." % sqlFileName)
            exitApp()
        else:
            logger.warning("ERROR: File %s not found." % sqlFileName)
            return

    inFile = codecs.open(sqlFileName, "r", "utf-8")
    sql = inFile.read()
    inFile.close()
    logger.info("   Loading SQL commands - done.")
    execSQLScript(sql)

def createTempTable(connection):
    logger.info("Creating table ac_gids")
    cursor = connection.cursor()
    try:
        cursor.execute("drop table if exists ac_gids;")
        cursor.execute("CREATE TABLE ac_gids (gid integer NOT NULL, address text);")
        logger.info("Done.")
    finally:
        cursor.close()

def getAddressRows(connection):
    logger.info("Retrieving address rows")
    cursor = connection.cursor()
    try:
        query = 'select nazev_ulice, cast(cislo_domovni as text), nazev_obce, cast(psc as text), cast(cislo_orientacni as text), znak_cisla_orientacniho, nazev_casti_obce, typ_so, nazev_mop, gid from address_points '
        cursor.execute(query)
        logger.info("Done.")
        return cursor
    except:
        logger.error("Error:Selecting address rows failed.")
        exitApp()

def renameTempTable(connection):
    logger.info("Renaming table _ac_gids to ac_gids.")
    cursor = connection.cursor()
    cursor.execute("drop table if exists ac_gids;alter table _ac_gids rename to ac_gids;")
    cursor.close()
    logger.info("Done.")

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
                    logPsycopg2Error(e)
                    logger.error(str(row_count))
                    exitApp()
                    pass

            print "Done - %d rows inserted." % row_count

        finally:
            cursor.close()



    finally:
        connection.close()

def buildGIDsTable():
    logger.info("Building table ac_gids")
    logger.info("------------------------")
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

            logger.info("Inserting rows")
            logger.info("----------------------")
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
                        logger.info(str(row_count) + " rows")

                except psycopg2.Error as e:
                    logPsycopg2Error(e)
                    logger.error(str(row_count) + " " + insertSQL + " failed. ")
                    exitApp()
                    pass

            logger.info("Done - %d rows inserted." % row_count)

        finally:
            cursor.close()

        #renameTempTable(connection)

        logger.info("Building table ac_gids done.")
    finally:
        connection.close()
    pass

class SQLInfo:
    def __init__(self, fileName, description, exitIfScriptNotFound = True):
        self.fileName = fileName
        self.description = description
        self.exitIfScriptNotFound = exitIfScriptNotFound

def buildServicesTables():
    scriptList = [
        SQLInfo("TypStObjektu.sql", "Table typ_st_objektu"),
        SQLInfo("AddressPoints.sql" , "Table address_points"),
        SQLInfo("FullText.sql" , "Table fulltext"),
        SQLInfo("ExplodeArray.sql" , "Table explode_array"),
        SQLInfo("gids.sql" , "Table gids"),
        SQLInfo("AfterImport.sql" , "User SQL commands AfterImport.sql", False)
    ]

    for sqlInfo in scriptList:
        execSQLScriptFile(sqlInfo.fileName, sqlInfo.description, sqlInfo.exitIfScriptNotFound)

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
