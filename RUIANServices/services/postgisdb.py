# -*- coding: utf-8 -*-
__author__ = 'Augustyn'

import psycopg2
from RUIANConnection import *
import re

from config import config

DATABASE_HOST = config.databaseHost
PORT          = config.databasePort
DATABASE_NAME = config.databaseName
USER_NAME     = config.databaseUserName
PASSWORD      = config.databasePassword

TABLE_NAME = "address_points"

ITEM_TO_DBFIELDS = {
    "id": "gid",
    "street": "nazev_ulice",
    "houseNumber": "cislo_domovni",
    "recordNumber": "cislo_domovni",
    "orientationNumber": "cislo_orientacni",
    "orientationNumberCharacter": "znak_cisla_orientacniho",
    "zipCode": "psc",
    "locality": "nazev_obce",
    "localityPart": "nazev_casti_obce",
    "districtNumber": "nazev_mop",
    "JTSKX": "latitude",
    "JTSKY": "longitude"
}

def noneToString(item):
    if item is None:
        return ""
    else:
        return item

def numberToString(number):
    if number is None:
        return ""
    else:
        return str(number)

def formatToQuery(item):
    if item == "":
        return None
    elif item.strip().isdigit():
        return int(item)
    else:
        return item

def numberValue(str):
    if str != "":
        s = str.split(" ")
        return s[1]
    else:
        return ""

def _findAddress(ID):
    con = psycopg2.connect(host=DATABASE_HOST, database=DATABASE_NAME, port= PORT, user=USER_NAME, password=PASSWORD)
    cur = con.cursor()
    cur.execute("SELECT nazev_ulice, cislo_domovni, typ_so, cislo_orientacni, znak_cisla_orientacniho, psc, nazev_obce, nazev_casti_obce, nazev_mop FROM " + TABLE_NAME + " WHERE gid = "+ str(ID))
    row = cur.fetchone()
    if row:
        if row[2][-3:] == ".p.":
            houseNumber = numberToString(row[1])
            recordNumber = ""
        elif row[2][-3:] == "ev.":
            houseNumber = ""
            recordNumber = numberToString(row[1])
        else:
            return None
        a= numberValue(noneToString(row[8]))
        return Address(noneToString(row[0]),houseNumber,recordNumber,numberToString(row[3]), noneToString(row[4]),numberToString(row[5]),noneToString(row[6]),noneToString(row[7]),a)
        #(street, houseNumber, recordNumber, orientationNumber, orientationNumberCharacter, zipCode, locality, localityPart, districtNumber)
    else:
        return None



def _getNearbyLocalities(y,x,distance):
    con = psycopg2.connect(host=DATABASE_HOST, database=DATABASE_NAME, port= PORT, user=USER_NAME, password=PASSWORD)
    cur = con.cursor()
    query = "SELECT gid, nazev_obce, nazev_casti_obce, nazev_ulice, typ_so, cislo_domovni, cislo_orientacni, znak_cisla_orientacniho, psc, nazev_mop FROM " + TABLE_NAME + " WHERE ST_DWithin(the_geom,ST_GeomFromText('POINT(-%s -%s)',5514),%s)" % (str(x), str(y), str(distance),)
    query += " LIMIT 25;"
    cur.execute(query)
    rows = cur.fetchall()
    return rows
    #addresses = []
    #for row in rows:
    #    if row[4][-3:] == ".p.":
    #        houseNumber = numberToString(row[5])
    #        recordNumber = ""
    #    elif row[4][-3:] == "ev.":
    #        houseNumber = ""
    #        recordNumber = numberToString(row[5])
    #    else:
    #        continue
    #    #psc = (numberToString(row[5]).decode("utf-8"))
    #    adr = Address((noneToString(row[1]).decode("utf-8")),houseNumber,recordNumber,(noneToString(row[4]).decode("utf-8")),(noneToString(row[5]).decode("utf-8")),(numberToString(row[6]).decode("utf-8")),(noneToString(row[7]).decode("utf-8")),(noneToString(row[8]).decode("utf-8")),(noneToString(row[9]).decode("utf-8")))
    #    addresses.append(adr)
    #return addresses

def addToQuery(atribute, comparator, first):
    if first:
        query = atribute + " " + comparator + " %s"
    else:
        query = " AND " + atribute + " " + comparator + " %s"
    return query

def _validateAddress(dictionary):
    first = True
    oneHouseNumber = False
    con = psycopg2.connect(host=DATABASE_HOST, database=DATABASE_NAME, port= PORT, user=USER_NAME, password=PASSWORD)
    cursor = con.cursor()

    query = "SELECT * FROM " + TABLE_NAME + " WHERE "
    tuple = ()
    for key in dictionary:
        if key == "houseNumber":
            if dictionary[key] != "":
                if oneHouseNumber:
                    return ["False"]
                else:
                    oneHouseNumber = True
                query += addToQuery("typ_so","=",first)
                first = False
                tuple = tuple + (u"č.p.",)
            else:
                continue
        if key == "recordNumber":
            if dictionary[key] != "":
                if oneHouseNumber:
                    return ["False"]
                else:
                    oneHouseNumber = True
                query += addToQuery("typ_so","=",first)
                first = False
                tuple = tuple + (u"č.ev.",)
            else:
                continue

        if key == "districtNumber" and dictionary[key] != "":
            value = formatToQuery(dictionary["locality"] + " " + dictionary["districtNumber"])
        else:
            value = formatToQuery(dictionary[key])
        tuple = tuple + (value,)

        if value is None:
            comparator = "is"
        else:
            comparator = "="
        query += addToQuery(ITEM_TO_DBFIELDS[key], comparator, first)
        first = False

    a = cursor.mogrify(query,tuple)
    cursor.execute(a)
    row = cursor.fetchone()
    if row:
        return ["True"]
    else:
        return ["False"]

#    rows = []
#    row_count = 0
#    for row in cursor:
#        row_count += 1
#        strRow = str(row[0])
#        rows.append(str(row[0]))

#    return rows

def _findCoordinates(ID):
    con = psycopg2.connect(host=DATABASE_HOST, database=DATABASE_NAME, port= PORT, user=USER_NAME, password=PASSWORD)
    cur = con.cursor()
    cur.execute("SELECT latitude, longitude, gid, nazev_obce, nazev_casti_obce, nazev_ulice, cislo_domovni, typ_so, cislo_orientacni, znak_cisla_orientacniho, psc, nazev_mop FROM " + TABLE_NAME + " WHERE gid = "+ str(ID))
    row = cur.fetchone()
    if row and row[0] is not None and row[1] is not None:
        if row[7] == "č.p.":
            houseNumber = numberToString(row[6])
            recordNumber = ""
        elif row[7] == "č.ev.":
            houseNumber = ""
            recordNumber = numberToString(row[6])
        c = (str("{:10.2f}".format(row[0])).strip(), str("{:10.2f}".format(row[1])).strip(), row[2], row[3], noneToString(row[4]), noneToString(row[5]), houseNumber, recordNumber, numberToString(row[8]), noneToString(row[9]), numberToString(row[10]), numberValue(noneToString(row[11])))
        return [c]
    else:
        return []

def _findCoordinatesByAddress(dictionary):
    first = True
    con = psycopg2.connect(host=DATABASE_HOST, database=DATABASE_NAME, port= PORT, user=USER_NAME, password=PASSWORD)
    cur = con.cursor()

    query = "SELECT latitude, longitude, gid, nazev_obce, nazev_casti_obce, nazev_ulice, cislo_domovni, typ_so, cislo_orientacni, znak_cisla_orientacniho, psc, nazev_mop FROM " + TABLE_NAME + " WHERE "

    for key in dictionary:
        if dictionary[key] != "":
            if first:
                query += ITEM_TO_DBFIELDS[key] + " = '" + dictionary[key] + "'"
                first = False
            else:
                query += " AND " + ITEM_TO_DBFIELDS[key] + " = '" + dictionary[key] + "'"

    query += "LIMIT 25"
    cur.execute(query)
    rows = cur.fetchall()
    coordinates = []

    for row in rows:
        if (row[0] is not None) and (row[1] is not None):
            if row[7] == "č.p.":
                houseNumber = numberToString(row[6])
                recordNumber = ""
            elif row[7] == "č.ev.":
                houseNumber = ""
                recordNumber = numberToString(row[6])
            coordinates.append((str("{:10.2f}".format(row[0])).strip(),str("{:10.2f}".format(row[1])).strip(), row[2], row[3], noneToString(row[4]), noneToString(row[5]), houseNumber, recordNumber, numberToString(row[8]), noneToString(row[9]), numberToString(row[10]), numberValue(noneToString(row[11]))))
        else:
            pass    #co se ma stat kdyz adresa nema souradnice?
    return coordinates

def _getRUIANVersionDate():
    result = "unassigned _getRUIANVersionDate"
    connection = psycopg2.connect(host=DATABASE_HOST, database=DATABASE_NAME, port= PORT, user=USER_NAME, password=PASSWORD)
    cursor = connection.cursor()
    try:
        query = 'select * from ruian_dates'
        cursor.execute(query)
        row = cursor.fetchone()
        result = row[1]
    finally:
        cursor.close()
        connection.close()

    return result

def _saveRUIANVersionDateToday():
    connection = psycopg2.connect(host=DATABASE_HOST, database=DATABASE_NAME, port= PORT, user=USER_NAME, password=PASSWORD)
    cursor = connection.cursor()
    try:
        query = 'DROP TABLE IF EXISTS ruian_dates;'
        query += 'CREATE TABLE ruian_dates (id serial PRIMARY KEY, validfor varchar);'
        import time
        value = time.strftime("%d.%m.20%y")
        query += "INSERT INTO ruian_dates (validfor) VALUES ('%s')" % value
        cursor.execute(query)
        connection.commit()
    finally:
        cursor.close()
        connection.close()
    pass

#_saveRUIANVersionDateToday()

#DROP TABLE IF EXISTS ruian_dates;
#CREATE TABLE ruian_dates (id serial PRIMARY KEY, validfor varchar);
#INSERT INTO ruian_dates (validfor) VALUES ('16.10.2014');