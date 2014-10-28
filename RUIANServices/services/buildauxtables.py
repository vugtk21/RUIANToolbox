# -*- coding: utf-8 -*-
__author__ = 'raugustyn'

import psycopg2
from config import config
import HTTPShared
import compileaddress

def main():
    conection = psycopg2.connect(
        host = config.databaseHost,
        database = config.databaseName,
        port = config.databasePort,
        user = config.databaseUserName, password = config.databasePassword
    )
    cursor = conection.cursor()
    cursor.execute("drop table if exists ac_gids;")
    cursor.execute("CREATE TABLE ac_gids (gid integer NOT NULL, address text);")
    cursor.close()

    cursor = conection.cursor()
    query = 'select nazev_ulice, cast(cislo_domovni as text), nazev_obce, cast(psc as text), cast(cislo_orientacni as text), znak_cisla_orientacniho, nazev_casti_obce, typ_so, nazev_mop, gid from address_points '
    cursor.execute(query)

    builder = HTTPShared.MimeBuilder("texttoonerow")

    row_count = 0
    gaugecount = 0
    insertCursor = conection.cursor()

    for row in cursor:
        row_count += 1
        gaugecount += 1
        street, houseNumber, locality, zipCode, orientationNumber, orientationNumberCharacter, localityPart, typ_so, nazev_mop, gid = row
        houseNumber, recordNumber = HTTPShared.analyseRow(typ_so, houseNumber)
        districtNumber = HTTPShared.extractDictrictNumber(nazev_mop)

        rowLabel = compileaddress.compileAddress(builder, street, houseNumber, recordNumber, orientationNumber, orientationNumberCharacter, zipCode, locality, localityPart, districtNumber)
        insertSQL = "INSERT INTO ac_gids (gid, address) VALUES (%s, '%s')" % (gid, rowLabel)
        insertCursor.execute(insertSQL)
        conection.commit()
        if gaugecount >= 1000:
            gaugecount = 0
            print row_count

    cursor.close()
    conection.close()
    pass


if __name__ == '__main__':
    import sys
    reload(sys)
    sys.setdefaultencoding('utf-8')
    main()

