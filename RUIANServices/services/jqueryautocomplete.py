#!C:\Python27\python.exe -u
# -*- coding: utf-8 -*-
import cgitb; cgitb.enable()

# *****************************************************************************
# Tento CGI skript vrací hodnoty pro Autocomplete
# *****************************************************************************

import jqueryautocompletePostGIS

import webserverbase

def getQueryValue(queryParams, id, defValue):
    # Vrací hodnotu URL Query parametruy id, pokud neexistuje, vrací hodnotu defValue
    if queryParams.has_key(id):
        return queryParams[id]
    else:
        return defValue

def processRequest(page, servicePathInfo, pathInfos, queryParams, response):
    # Zpracovává HTTP request
    if queryParams:
        token = getQueryValue(queryParams, 'term', "")
        max_matches = int(getQueryValue(queryParams, 'max_matches', 40))
        ruian_type = getQueryValue(queryParams, 'RUIANType', "zip")
        resultFormat = getQueryValue(queryParams, 'ResultFormat', "")
        resultArrray = jqueryautocompletePostGIS.getAutocompleteResults(ruian_type, token, resultFormat, max_matches)
    else:
        resultArrray = []

    response.mimeFormat = "text/javascript"
    response.htmlData = "[\n" + ",\n\t".join(resultArrray) + "\n]"
    response.handled = True
    return response

if __name__ == '__main__':
    # Nastavení kódování češtiny na UTF-8
    import sys
    reload(sys)
    sys.setdefaultencoding('utf-8')

    # Spuštění serveru
    webserverbase.mainProcess(processRequest)
