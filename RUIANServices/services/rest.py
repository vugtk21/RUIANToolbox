#!C:/Python27/python.exe
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        rest.py
# Purpose:     Implementuje funkcionalitu služeb dle standardu REST
#
# Author:      Radek Augustýn
# Copyright:   (c) VUGTK, v.v.i. 2014
# License:     CC BY-SA 4.0
#-------------------------------------------------------------------------------

#import web
import re
import os
import shared as sharedModule
import urllib
import codecs

from HTTPShared import *

import addresswebservices
import web
import RUIANConnection

from config import SERVICES_WEB_PATH
from config import HTMLDATA_URL
from config import config

from downloader.downloadruian import getDataDirFullPath

serverPathDepth = 0

def getHTMLPath():
    paths = os.path.dirname(__file__).split("/")
    paths = paths[:len(paths) - 1]
    return "/".join(paths) + "/html/"

def getTestingPath():
    paths = os.path.dirname(__file__).split("/")
    paths = paths[:len(paths) - 1]
    return "/".join(paths) + "/testing/"
    return

DATABASE_DETAILS_PATH = "/dbdetails"
AUTOCOMPLETES_PATH = '/autocomplete'
DATA_ALIASES = {
        "/html": getHTMLPath,
        "/downloaded": getDataDirFullPath,
        "/testing" : getTestingPath
}

def getFileContent(fileName):
    if os.path.exists(fileName):
        if os.path.isfile(fileName):
            f = open(fileName, "rb")
            s = f.read()
            f.close()
            return s
        else:
            return fileName + " is a directory, can't be sent over http."
    else:
        return "File " + fileName + " not found."

def fileNameToMimeFormat(fileName):
    knownMimeFormats = {
        ".js": "text/javascript",
        ".png" : "image/png",
        ".ico" : "image/png",
        ".jpg" : "image/jpeg",
        ".jpeg" : "image/jpeg",
        ".htm" : "text/html",
        ".html" : "text/html",
        ".txt" : "text/plain",
        ".log" : "text/plain",
        ".css" : "text/css"
    }
    fileExt = fileName[fileName.rfind("."):]
    if knownMimeFormats.has_key(fileExt):
        return knownMimeFormats[fileExt]
    else:
        return None


def ProcessRequest(fullPathList, queryParams, response):
    addresswebservices.console.clear()

    addresswebservices.console.addInfo(u"SERVICES_WEB_PATH: " + SERVICES_WEB_PATH)
    addresswebservices.console.addInfo(u"HTMLDATA_URL: " + HTMLDATA_URL)
    if addresswebservices.console.debugMode:
        import shared
        import config as configModule
        addresswebservices.console.addInfo(u"configModule.getHTMLDataURL(): " + configModule.getHTMLDataURL())
        addresswebservices.console.addInfo(u"shared.isCGIApplication(): " + str(shared.isCGIApplication))
        addresswebservices.console.addInfo(u"configModule.HTMLDATA_URL: " + configModule.HTMLDATA_URL)
        addresswebservices.console.addInfo(u"configModule.SERVER_HTTP: " + configModule.SERVER_HTTP)
        addresswebservices.console.addInfo(u"configModule.getPortSpecification(): " + configModule.getPortSpecification())

    pageBuilder = addresswebservices.ServicesHTMLPageBuilder()
    if fullPathList in [["/"], []]:
        response.htmlData = pageBuilder.getServicesHTMLPage(__file__,"", {})
        response.handled = True
    else:
        if fullPathList == []:
            servicePathInfo = "/"
        else:
            servicePathInfo = "/" + fullPathList[0]                       # první rest parametr

        if DATA_ALIASES.has_key(servicePathInfo.lower()):
            fileName = DATA_ALIASES[servicePathInfo.lower()]() + "/".join(fullPathList[1:])
            response.htmlData = getFileContent(fileName)
            mimeFormat = fileNameToMimeFormat(fileName)
            if mimeFormat != None:
                response.mimeFormat = mimeFormat
                if mimeFormat == "text/plain":
                    response.htmlData = response.htmlData.replace("\r\n", "\n")
            response.handled = True
        elif servicePathInfo.lower().startswith(AUTOCOMPLETES_PATH):
            import jqueryautocomplete
            response = jqueryautocomplete.processRequest("/".join(fullPathList[1:]), "", "", queryParams, response)
        elif servicePathInfo.lower().startswith(DATABASE_DETAILS_PATH):
            RUIANConnection._getDBDetails(fullPathList[1:], queryParams, response)
        else:
            pathInfos = fullPathList[1:]  # ostatní

            for service in addresswebservices.services:
                if (service.pathName == servicePathInfo) and (service.processHandler != None):
                    #TODO Tohle by si asi měla dělat service sama
                    i = 0
                    for pathValue in pathInfos:
                        if i < len(service.restPathParams):
                            queryParams[service.restPathParams[i].pathName[1:]] = pathValue   #přidání do slovníku, přepíše hodnotu se stejným klíčem
                        else:
                            # Too many parameters
                            addresswebservices.console.addMsg(u"Nadbytečný REST parametr č." + str(i) + "-" + pathValue)

                        i = i + 1
                    service.processHandler(queryParams, response)
                    break

            if not response.handled:
                if pathInfos != []:
                    addresswebservices.console.addMsg(u"Neznámá služba: " + servicePathInfo)
                response.htmlData = pageBuilder.getServicesHTMLPage(__file__, servicePathInfo, queryParams)
                response.handled = True

    return response

urls = ('/favicon.ico', 'favicon', '/(.*)', 'handler')

class MyApplication(web.application):
    def run(self, port = config.noCGIAppPortNumber, *middleware):
        func = self.wsgifunc(*middleware)
        return web.httpserver.runsimple(func, (config.noCGIAppServerHTTP, port))

class favicon:
    def GET(self):
        pass


class handler:
    def doProcessRequest(self, page):
        sharedModule.isCGIApplication = False
        response = ProcessRequest(page.split("/"), web.input(), HTTPResponse(False))
        if response.handled:
            web.header("Content-Type", response.mimeFormat + ";charset=utf-8")
            return response.htmlData
        else:
            return "doProcessRequest Error"

    def GET(self, page):
        sharedModule.isCGIApplication = False
        return self.doProcessRequest(page)

    def POST(self, page):
        sharedModule.isCGIApplication = False
        return self.doProcessRequest(page)

if __name__ == "__main__":
    # Nastavení znakové sady na utf-8
    import sys
    reload(sys)
    sys.setdefaultencoding('utf-8')

    import os
    if os.environ.has_key('SERVER_SOFTWARE'):
        # Script spuštěn jako CGI
        import cgi
        import cgitb
        cgitb.enable()

        sharedModule.isCGIApplication = True

        path = SERVICES_WEB_PATH.split("/")
        serverPathDepth = 0
        for item in path:
            if item != "":
                serverPathDepth = serverPathDepth + 1

        form = cgi.FieldStorage()
        if os.environ.has_key('PATH_INFO'):
	        pathInfo = os.environ['PATH_INFO']
        else:
	        pathInfo = ""
        if pathInfo[:1] == "/":
            pathInfo = pathInfo[1:]

        fullPathList = pathInfo.replace("//", "/")
        fullPathList = fullPathList.split("/")                                # REST parametry

        query = {}
        list = form.list
        for item in list:
            decodedValue = urllib.unquote(item.value)
            try:
                decodedValue = unicode(decodedValue, "utf-8")
            except:
                decodedValue = codecs.decode(decodedValue, "latin-1")
            decodedValue = urllib.unquote(decodedValue)
            query[item.name] = decodedValue

        response = ProcessRequest(fullPathList, query, HTTPResponse(False))
        if response.handled:
            if response.mimeFormat in ["text/html", "text/javascript", "text/plain"]:
                print "Content-Type: " + response.mimeFormat + ";charset=utf-8"   # HTML is following
                print                                           # blank line, end of headers
                sys.stdout.write(response.htmlData.encode('utf-8'))
            else:
                print "Content-Type: " + "application/octet-stream" #response.mimeFormat
                print                                           # blank line, end of headers
                if sys.platform != "win32":
                    sys.stdout.write(response.htmlData)
                    sys.stdout.flush()
                else:
                    import os, msvcrt
                    msvcrt.setmode(sys.stdout.fileno(), os.O_BINARY)
                    sys.stdout.write(response.htmlData)
                    sys.stdout.flush()
                    msvcrt.setmode(sys.stdout.fileno(), os.O_TEXT)


        else:
            print "ProcessRequest not handled"

    else:
        # Script je spuštěn jako samostatný server
        config.serverHTTP = config.noCGIAppServerHTTP
        SERVER_HTTP = config.noCGIAppServerHTTP
        #SERVICES_WEB_PATH = ""
        config.portNumber = config.noCGIAppPortNumber
        PORT_NUMBER = config.noCGIAppPortNumber

        app = MyApplication(urls, globals())
        app.run(port = config.noCGIAppPortNumber)