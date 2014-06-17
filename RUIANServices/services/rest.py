#!C:/Python27/python.exe
# -*- coding: utf-8 -*-

import web
import re
from HTTPShared import *

import addresswebservices
import web
import os

from config import SERVER_HTTP
from config import PORT_NUMBER
from config import SERVICES_WEB_PATH
from config import HTMLDATA_URL

path = SERVICES_WEB_PATH.split("/")
serverPathDepth = 0
for item in path:
    if item != "":
        serverPathDepth = serverPathDepth + 1

def getHTMLPath():
    paths = os.path.dirname(__file__).split("/")
    paths = paths[:len(paths) - 1]
    return "/".join(paths) + "/html/"


def getFileContent(fileName):
    if os.path.exists(fileName):
        f = open(fileName, "rb")
        s = f.read()
        f.close()
        return s
    else:
        return "File " + fileName + " not found."

def ProcessRequest(page, queryParams, response):
    addresswebservices.console.clear()
    pageBuilder = addresswebservices.ServicesHTMLPageBuilder()
    if page in ["/", ""]:
        response.htmlData = pageBuilder.getServicesHTMLPage("", {})
        response.handled = True
    elif page.find(".") >= 0 and page[:len(SERVICES_WEB_PATH)] != SERVICES_WEB_PATH:
        path = getHTMLPath()
        page = page.replace(HTMLDATA_URL, path)
        response.htmlData = getFileContent(page) # TODO Implementovat vracení binárních souborů
        response.handled = True
    else:
        fullPathList = page.replace("//", "/")
        fullPathList = fullPathList.split("/")                                # REST parametry
        if serverPathDepth != 0:
            fullPathList = fullPathList[serverPathDepth:]
        #TODO PathInfo by mělo být až za adresou serveru - zkontolovat jak je to na Apache
        servicePathInfo = "/" + fullPathList[0]                       # první rest parametr
        pathInfos = fullPathList[1:]                                  # ostatní

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
            addresswebservices.console.addMsg(u"Neznámá služba " + servicePathInfo)
            response.htmlData = pageBuilder.getServicesHTMLPage(servicePathInfo, queryParams)
            response.handled = True
    return response

urls = ('/favicon.ico', 'favicon', '/(.*)', 'handler')

class MyApplication(web.application):
    def run(self, port = PORT_NUMBER, *middleware):
        func = self.wsgifunc(*middleware)
        return web.httpserver.runsimple(func, (SERVER_HTTP, port))


class favicon:
    def GET(self):
        pass


class handler:
    def doProcessRequest(self, page):
        response = ProcessRequest(page, web.input(), HTTPResponse(False))
        if response.handled:
            web.header("Content-Type", response.mimeFormat)
            return response.htmlData
        else:
            return "doProcessRequest Error"

    def GET(self, page):
        return self.doProcessRequest(page)

    def POST(self, page):
        return self.doProcessRequest(page)


if __name__ == "__main__":
    import sys
    reload(sys)
    sys.setdefaultencoding('utf-8')
    import os
    serverPathDepth = 0
    if os.environ.has_key('SERVER_SOFTWARE'):
        import cgi
        import cgitb
        cgitb.enable()

        form = cgi.FieldStorage()
        if os.environ.has_key('PATH_INFO'):
	        pathInfo = os.environ['PATH_INFO']
        else:
	        pathInfo = ""
        if pathInfo[:1] == "/":
            pathInfo = pathInfo[1:]

        query = {}
        list = form.list
        for item in list:
            query[item.name] = unicode(item.value, "utf-8")

        response = ProcessRequest(pathInfo, query, HTTPResponse(False))
        if response.handled:
            print "Content-Type: " + response.mimeFormat    # HTML is following
            print                                           # blank line, end of headers
            print response.htmlData.encode('utf-8')
        else:
            print "doProcessRequest Error"

    else:
        app = MyApplication(urls, globals())
        app.run(port = PORT_NUMBER)