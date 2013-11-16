# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        sharedTools
# Purpose:     y
#
# Author:      Radek Augustýn
#
# Created:     04/05/2013
# Copyright:   (c) Radek Augustýn 2013
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import os
import configRUIAN, configGUI

def pathWithLastSlash(path):
    sepIdx = path.rfind(os.sep)
    if sepIdx == len(path) - 1:
        return path
    else:
        return path + os.sep

def getFileExtension(fileName):
    sepIdx = fileName.rfind(os.extsep)
    if sepIdx >= 0:
        return fileName[sepIdx + 1:]
    else:
        return ""

def isImportedTable(tableName):
    result = False
    if configRUIAN.tableDef.has_key(tableName):
        treeViewSet = configGUI.configData['treeViewSet']
        if treeViewSet.has_key(tableName):
            tableSettings = treeViewSet[tableName]
            for fieldName in tableSettings:
                if tableSettings[fieldName] == "True":
                    return True
    return result

def alignStrLeft(v, numChars):
    while (len(v) < numChars):
        v = " " + v
    return v

def alignStrRight(v, numChars):
    while (len(v) < numChars):
        v = v + " "
    return v