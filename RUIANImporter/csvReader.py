#-------------------------------------------------------------------------------
# Name:        csvreader.py
# Purpose:
#
# Author:      Radecek
#
# Created:     19/05/2013
# Copyright:   (c) Radecek 2013
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import csv, os
import configRUIAN, textFile_DBHandler

dbHandler = textFile_DBHandler.Handler("I:\\02_OpenIssues\\07_Euradin\\04_Cisleniky\\")

def extractFileName(fullFileName, removeExtension = True):
    startIdx = fullFileName.rfind(os.sep)
    if removeExtension and fullFileName.find(os.extsep) >= 0:
        endIdx = fullFileName.find(os.extsep)
    else:
        endIdx = len(fullFileName)

    return fullFileName[startIdx + 1:endIdx]

def importCiselnik(csvFileName):
    def fileEncode(file):
        for line in file:
            yield line.decode('windows-1250').encode('utf-8')

    csvReader = csv.reader(fileEncode(open(csvFileName)), delimiter=';', quotechar='|')
    fisrtRow = True
    for row in csvReader:
        if fisrtRow:
            print csvFileName, "\t", ', '.join(row)
            print "############################################"
            tableName = extractFileName(csvFileName)
            configRUIAN.tableDef[tableName] = { "fields":{} }
            fields = configRUIAN.tableDef[tableName][configRUIAN.FIELDS_KEY_NAME]
            for fieldName in row:
                fields[fieldName] = { "type" : "String" }
            print ',\n'.join(fields)
            dbHandler.createTable(tableName)
            fisrtRow = False
        else:
            currentFields = {}
            i = 0
            for fieldName in fields:
                currentFields[fieldName] = row[i]
                i = i + 1
            dbHandler.writeRowToTable(tableName, currentFields)
    pass

def importCiselnikDirectory(path):
    for dirItem in os.listdir(path):
        if dirItem.find(".csv") > 0:
            importCiselnik(path + dirItem)


if __name__ == '__main__':
    importCiselnikDirectory("I:\\02_OpenIssues\\07_Euradin\\04_Cisleniky\\")
