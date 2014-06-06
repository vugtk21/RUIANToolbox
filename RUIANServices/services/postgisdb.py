__author__ = 'Augustyn'

import psycopg2
from RUIANConnection import *

DATABASE_HOST = "192.168.1.93"
PORT = "5432"
DATABSE_NAME = "euradin"
USER_NAME = "postgres"
PASSWORD = "postgres"
TABLE_NAME = "address_points"

ITEM_TO_DBFIELDS = {
    "id": "gid",
    "street": "nazev_ulice",
    "houseNumber": "cislo_domovni",
    "recordNumber": "cislo_domovni",
    "orientationNumber": "cislo_orientacni",
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

def _findAddress(ID):
    con = psycopg2.connect(host=DATABASE_HOST, database=DATABSE_NAME, port= PORT, user=USER_NAME, password=PASSWORD)
    cur = con.cursor()
    cur.execute("SELECT nazev_ulice, cislo_domovni, nazev_momc, cislo_orientacni, psc, nazev_obce, nazev_casti_obce, nazev_mop FROM " + TABLE_NAME + " WHERE gid = "+ str(ID))
    row = cur.fetchone()
    if row:
        return Address(noneToString(row[0]),numberToString(row[1]),noneToString(row[2]),numberToString(row[3]),numberToString(row[4]),noneToString(row[5]),noneToString(row[6]),noneToString(row[7]))
        #(street, houseNumber, recordNumber, orientationNumber, zipCode, locality, localityPart, districtNumber)
    else:
        return None

def _getNearbyLocalities(x,y,distance):
    con = psycopg2.connect(host=DATABASE_HOST, database=DATABSE_NAME, port= PORT, user=USER_NAME, password=PASSWORD)
    cur = con.cursor()
    query = "SELECT nazev_ulice, cislo_domovni, nazev_momc, cislo_orientacni, psc, nazev_obce, nazev_casti_obce, nazev_mop FROM " + TABLE_NAME + " WHERE ST_DWithin(the_geom,ST_GeomFromText('POINT(%s %s)',5514),%s)" % (str(y), str(x), str(distance),)
    query += " LIMIT 25;"
    cur.execute(query)
    rows = cur.fetchall()
    addresses = []
    for row in rows:
        adr = Address((noneToString(row[0]).decode("utf-8")),(noneToString(row[1]).decode("utf-8")),(noneToString(row[2]).decode("utf-8")),(noneToString(row[3]).decode("utf-8")),(noneToString(row[4]).decode("utf-8")),(noneToString(row[5]).decode("utf-8")),(noneToString(row[6]).decode("utf-8")),(noneToString(row[7]).decode("utf-8")))
        addresses.append(adr)
    return addresses

def _validateAddress(dictionary):
    first = True
    con = psycopg2.connect(host=DATABASE_HOST, database=DATABSE_NAME, port= PORT, user=USER_NAME, password=PASSWORD)
    cursor = con.cursor()

    query = "SELECT * FROM " + TABLE_NAME + " WHERE "

    for key in dictionary:
        if dictionary[key] != "":
            if first:
                query += ITEM_TO_DBFIELDS[key] + " = '" + dictionary[key] + "'"
                first = False
            else:
                query += " AND " + ITEM_TO_DBFIELDS[key] + " = '" + dictionary[key] + "'"

    cursor.execute(query)
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
    con = psycopg2.connect(host=DATABASE_HOST, database=DATABSE_NAME, port= PORT, user=USER_NAME, password=PASSWORD)
    cur = con.cursor()
    cur.execute("SELECT latitude, longitude FROM " + TABLE_NAME + " WHERE gid = "+ str(ID))
    row = cur.fetchone()
    if row:
        c = Coordinates(str("{:10.2f}".format(row[0])).strip(), str("{:10.2f}".format(row[1])).strip())
        return [c]
    else:
        return []

def _findCoordinatesByAddress(dictionary):
    first = True
    con = psycopg2.connect(host=DATABASE_HOST, database=DATABSE_NAME, port= PORT, user=USER_NAME, password=PASSWORD)
    cur = con.cursor()

    query = "SELECT latitude, longitude FROM " + TABLE_NAME + " WHERE "

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
            coordinates.append(Coordinates(str("{:10.2f}".format(row[0])).strip(),str("{:10.2f}".format(row[1])).strip()))
        else:
            pass    #co se ma stat kdyz adresa nema souradnice?
    return coordinates