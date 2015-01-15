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
    if page.lower().startswith("mopdistricts"):
        response.htmlData = jqueryautocompletePostGIS.getMOPDistricts()
    elif page.lower().startswith("districtmops"):
        response.htmlData = jqueryautocompletePostGIS.getDistrictMOPs()
    elif queryParams:
        max_matches = int(getQueryValue(queryParams, 'max_matches', 40))
        if page.lower().startswith("fill"):
            response.htmlData = jqueryautocompletePostGIS.getFillResults(queryParams)
        elif page.lower().startswith("datalists"):
            dataListsLimit = int(getQueryValue(queryParams, 'max_matches', 150))
            response.htmlData = jqueryautocompletePostGIS.getDataListValues(queryParams, dataListsLimit)
        else:
            token = getQueryValue(queryParams, 'term', "")
            ruian_type = getQueryValue(queryParams, 'RUIANType', "zip")
            resultFormat = getQueryValue(queryParams, 'ResultFormat', "")
            smartAutocomplete = getQueryValue(queryParams, 'SmartAutocomplete', "False").lower() == "true"
            resultArray = jqueryautocompletePostGIS.getAutocompleteResults(queryParams, ruian_type, token, resultFormat, smartAutocomplete, max_matches)
            response.htmlData = "[\n\t" + ",\n\t".join(resultArray) + "\n]"
    else:
        response.htmlData = "[  ]"

    response.mimeFormat = "text/javascript"
    response.handled = True
    return response

if __name__ == '__main__':
    # Nastavení kódování češtiny na UTF-8
    import sys
    reload(sys)
    sys.setdefaultencoding('utf-8')

    # Spuštění serveru
    webserverbase.mainProcess(processRequest)