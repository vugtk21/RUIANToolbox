#!C:/Python27/python.exe
# -*- coding: utf-8 -*-

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

def getMimeFormat(formatText):
    if formatText in ["xml", "html"]:
        return "text/" + formatText
    else: # Default value text
        return "text/plain"

class MimeBuilder:
    def __init__(self, formatText = "text"):
        self.formatText = formatText.lower()
        pass

    def getMimeFormat(self):
        if self.formatText in ["xml", "html", "json"]:
            return "text/" + self.formatText
        else: # Default value text
            return "text/plain"

    def dictToXML(self, dataDict, lineSeparator = "\n"):
        result = ""
        for key in dataDict:
            value = dataDict[key]
            if type(value) == dict:
                value = self.dictToXML(value, lineSeparator)
            result += "<" + key + ">" + value + "</" + key + ">" + lineSeparator

        return result

    def dictToJSON(self, dataDict, lineSeparator = "\n"):
        result = ""
        for key in dataDict:
            value = dataDict[key]
            if type(value) == dict:
                value = self.dictToJSON(value, lineSeparator)
            result += key + ' : "' + value + '"' + lineSeparator

        return result

    def dictToText(self, dataDict, lineSeparator = "\n"):
        result = ""
        for key in dataDict:
            value = dataDict[key]
            if type(value) == dict:
                value = "<div>" + self.dictToText(value, lineSeparator) + "</div>"
            result += value + lineSeparator

        return result

    def dictToHTML(self, dataDict, lineSeparator = "<br>\n"):
        result = ""
        for key in dataDict:
            value = dataDict[key]
            if type(value) == dict:
                value = self.dictToHTML(value, lineSeparator)
            result += value + lineSeparator

        return result

    def dictToResponseText(self, dataDict):
        if self.formatText == "xml":
            return self.dictToXML(dataDict)
        elif self.formatText == "html":
            return self.dictToHTML(dataDict)
        elif self.formatText == "json":
            return self.dictToJSON(dataDict)
        else: # default value text
            return self.dictToText(dataDict)


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
