# -*- coding: utf-8 -*-
__author__ = 'raugustyn'

import psycopg2
from config import config
import HTTPShared
import compileaddress

def createTempTable(connection):
    print "Creating temporary table _ac_gids"
    cursor = connection.cursor()
    try:
        cursor.execute("drop table if exists _ac_gids;")
        cursor.execute("CREATE TABLE _ac_gids (gid integer NOT NULL, address text);")
    finally:
        cursor.close()

def getAddressRows(connection):
    print "Retrieving address rows...."
    cursor = connection.cursor()
    try:
        query = 'select nazev_ulice, cast(cislo_domovni as text), nazev_obce, cast(psc as text), cast(cislo_orientacni as text), znak_cisla_orientacniho, nazev_casti_obce, typ_so, nazev_mop, gid from address_points '
        cursor.execute(query)
        return cursor
    except:
        print "Error:Selecting address rows failed."
        return None

def renameTempTable(connection):
    print "Renaming table _ac_gids to ac_gids."
    cursor = connection.cursor()
    cursor.execute("drop table if exists ac_gids;")
    cursor.execute("alter table _ac_gids rename to ac_gids;")
    cursor.close()

def main():
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
        finally:
            cursor.close()

        renameTempTable(connection)

    finally:
        connection.close()
    pass

if __name__ == '__main__':
    import sys
    reload(sys)
    sys.setdefaultencoding('utf-8')
    main()