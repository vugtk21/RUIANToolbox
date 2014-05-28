# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        HTTPShared
# Purpose:
#
# Author:      Radek Augustýn
#
# Created:     13/11/2013
# Copyright:   (c) Radek Augustýn 2013
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import urllib

services = []

def getResultFormatParam():
    return RestParam("/Format", u"Formát", u"Formát výsledku služby (HTML, XML, Text, JSON)")

def getSearchTextParam():
    return URLParam("SearchText", u"Adresa", u"Textový řetězec adresy")

def getAddressPlaceIdParamRest():
    return RestParam("/AddressPlaceId", u"Identifikátor", u"Identifikátor adresního místa")

def getAddressPlaceIdParamURL():
    return URLParam("AddressPlaceId", u"Identifikátor", u"Identifikátor adresního místa")

class HTTPResponse():
    def __init__(self, handled, mimeFormat = "text/html", htmlData = ""):
        self.handled = handled
        self.mimeFormat = mimeFormat
        self.htmlData = htmlData

class URLParam:
    def __init__(self, name, caption, shortDesc, htmlDesc = ""):
        self.name  = name
        self.caption   = caption
        self.shortDesc = shortDesc
        self.htmlDesc  = htmlDesc

class RestParam(URLParam):
    def __init__(self, pathName, caption, shortDesc, htmlDesc = ""):
        URLParam.__init__(self, pathName, caption, shortDesc, htmlDesc)

    def getPathName(self):
        return self.name

    pathName = property(getPathName, "REST path name")

def getMimeFormat(self, formatText):
    a = self[formatText].lower()
    if a in ["html"]:
        return "text/" + self[formatText].lower()
    elif a in ["xml", "json"]:
        return "application/" + self[formatText].lower()
    else: # Default value text
        return "text/plain"


class MimeBuilder:
    def __init__(self, formatText = "text"):
        self.formatText = formatText.lower()
        pass

    def getMimeFormat(self):
        if self.formatText in ["xml", "json"]:
            return "application/" + self.formatText
        elif self.formatText == "html":
            return "text/" + self.formatText
        else: # Default value text
            return "text/plain"

    def listToXML(self, listOfLines, lineSeparator = "\n", tag = "FormattedOutput"):
        result = '<?xml version="1.0" encoding="UTF-8"?>' + lineSeparator + "<xml>" + lineSeparator
        for line in listOfLines:
            #value = dataDict[key]
            #if type(value) == dict:
            #    value = self.dictToXML(value, lineSeparator)
            result += "<" + tag + ">" + line + "</" + tag + ">" + lineSeparator
        return result + "</xml>"

    def listToJSON(self, listOfLines, lineSeparator = "\n", tag = "FormattedOutputLine"):
        result = "{"
        index = 0
        for line in listOfLines:
            #value = dataDict[key]
            #if type(value) == dict:
            #    value = self.dictToJSON(value, lineSeparator)
            index += 1
            if index > 1:
                result += ','
            result += lineSeparator + '"' + tag + str(index) + '" : "' + line + '"'
        result += lineSeparator + "}"
        return result

    def listToText(self, listOfLines, lineSeparator = "\n"):
        result = ""
        for line in listOfLines:
            #value = dataDict[key]
            #if type(value) == dict:
            #    value = "<div>" + self.dictToText(value, lineSeparator) + "</div>"
            result += line + lineSeparator
        return result

    def listToHTML(self, listOfLines, lineSeparator = "<br>"):
        result = ""
        for line in listOfLines:
            if result != "":
                result += lineSeparator
            result += line
        return result

    def listToResponseText(self, ListOfLines):
        if self.formatText == "xml":
            return self.listToXML(ListOfLines)
        elif self.formatText == "html":
            return self.listToHTML(ListOfLines)
        elif self.formatText == "json":
            return self.listToJSON(ListOfLines)
        else: # default value text
            return self.listToText(ListOfLines)

    def coordinatesToXML(self, listOfCoordinates, lineSeparator = "\n", tag = "Coordinates"):
        result = '<?xml version="1.0" encoding="UTF-8"?>' + lineSeparator + "<xml>" + lineSeparator
        index = 0
        for coordinates in listOfCoordinates:
            index = index + 1
            result += "<" + tag + str(index) + ">" + lineSeparator + "<Y>" + coordinates.JTSKY + "</Y>" + lineSeparator + "<X>" + coordinates.JTSKX + "</X>" + lineSeparator + "</" + tag + str(index) + ">" + lineSeparator
        result += "</xml>"
        return result

    def coordinatesToHTML(self, listOfCoordinates, lineSeparator = "<br>"):
        result = ""
        for line in listOfCoordinates:
            if result != "":
                result += lineSeparator
            result += line.JTSKY + ", " + line.JTSKX
        return result

    def coordinatesToJSON(self, listOfCoordinates, lineSeparator = "\n", tag = "Coordinates"):
        result = "{"
        index = 0
        for line in listOfCoordinates:
            index += 1
            if index > 1:
                result += ','
            result += lineSeparator + '"' + tag + str(index) + '" : {' + lineSeparator + ' \t"Y": "' + line.JTSKY + '",' + lineSeparator + '\t"X": "' + line.JTSKX + '"' + lineSeparator + "\t}"
        result += lineSeparator + "}"
        return result

    def coordinatesToText(self, listOfCoordinates, lineSeparator = "\n"):
        result = ""
        for line in listOfCoordinates:
            result += line.JTSKY + ", " + line.JTSKX + lineSeparator
        return result

    def coordintesToResponseText(self, ListOfCoordinates):
        if self.formatText == "xml":
            return self.coordinatesToXML(ListOfCoordinates)
        elif self.formatText == "html":
            return self.coordinatesToHTML(ListOfCoordinates)
        elif self.formatText == "json":
            return self.coordinatesToJSON(ListOfCoordinates)
        else: # default value text
            return self.coordinatesToText(ListOfCoordinates)


class WebService:
    """ Webova sluzba
    """
    def __init__(self, pathName, caption, shortDesc, htmlDesc = "", restPathParams = [], queryParams = [],
                 processHandler = None, sendButtonCaption = u"Odeslat", htmlInputTemplate = ""):
        ''' Webova sluzba '''
        self.pathName  = pathName
        self.caption   = caption
        self.shortDesc = shortDesc
        self.htmlDesc  = htmlDesc
        self.restPathParams = restPathParams
        self.queryParams = queryParams
        self.processHandler = processHandler
        self.sendButtonCaption = sendButtonCaption
        self.htmlInputTemplate = htmlInputTemplate # Šablona elementu HTML, implicitně INPUT
        self._params = None
        pass

    def getParams(self):
        if self._params == None or len(self.restPathParams) + len(self.queryParams) != len(self._params):
            self._params = {}
            self._params.update(self.restPathParams)
            self._params.update(self.queryParams)

        return self._params

    params = property(getParams, "REST and Query params together")

    def getServicePath(self):
        result = "/REST" + self.pathName
        for param in self.restPathParams:
            result = result + "/&#60;" + param.pathName[1:] + "&#62;"
        if len(self.queryParams) > 0:
            queryParamsList = []
            result += "?"
            for param in self.queryParams:
                queryParamsList.append(param.name + "=")
            result += "&".join(queryParamsList)

        return result

    def buildServiceURL(self, queryParams):
        result = self.pathName
        for param in self.restPathParams:
            result = result + param.pathName
        if len(self.queryParams) > 0:
            queryParamsList = []
            result += "?"
            for param in self.queryParams:
                if queryParams.has_key(param.name):
                    valueStr = queryParams[param.name]
                else:
                    valueStr = ""
                queryParamsList.append(param.name + "=" + valueStr)
            result += "&".join(queryParamsList)

        return result

    def processHTTPRequest(self, path, queryParams):
        pass

def p(queryParams, name, defValue = ""):
    if queryParams.has_key(name):
        a = urllib.unquote(queryParams[name])
        return urllib.unquote(queryParams[name])
    else:
        return defValue
