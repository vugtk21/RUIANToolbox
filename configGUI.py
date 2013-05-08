# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        configGUI
# Purpose:     Ukládá nastavení zvolené uživatelem v GUI
#
# Author:      Radek Augustýn
#
# Created:     03.05.2013
# Copyright:   (c) Radek Augustýn 2013
# Licence:     <your licence>
#-------------------------------------------------------------------------------

configData = {
    "databaseTypes" : {
      "textFile_DBHandler" : "Databáze uložená do souborů v adresáři",
      "postGIS_DBHandler"  : "Databáze PostGIS",
    },
    "selectedDatabaseType" : "textFile_DBHandler",
    "textFile_DBHandler" : {
      "dataDirectory" : "I:\\02_OpenIssues\\07_Euradin\\01_Data"
    },
    "postGIS_DBHandler" : {
        "dbname" : "euradin",
        "host" : "localhost",
        "port" : "5432",
        "user" : "postgres",
        "password" : "postgres",
        "schemaName" : "public"
    }
}
