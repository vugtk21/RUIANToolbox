#!C:\Python27\python.exe -u
import cgitb; cgitb.enable()
import cgi
import os

import jqueryautocompletePostGIS

import webserverbase

def getQueryValue(queryParams, id, defValue):
    if queryParams.has_key(id):
        return queryParams[id]
    else:
        return defValue

def processRequest(page, servicePathInfo, pathInfos, queryParams, response):
    if queryParams:
        token = getQueryValue(queryParams, 'term', "")
        max_matches = int(getQueryValue(queryParams, 'max_matches', 40))
        use_similar = getQueryValue(queryParams, 'use_similar', "false")
        ruian_type = getQueryValue(queryParams, 'RUIANType', "zip")
        resultArrray = jqueryautocompletePostGIS.getAutocompleteResults(ruian_type, token, max_matches)
    else:
        resultArrray = []

    response.mimeFormat = "text/javascript"
    response.htmlData = "[\n" + ",\n\t".join(resultArrray) + "\n]"
    response.handled = True
    return response

if __name__ == '__main__':
    import sys
    reload(sys)
    sys.setdefaultencoding('utf-8')
    webserverbase.mainProcess(processRequest)
