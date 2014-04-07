# -*- coding: utf-8 -*-

import web
import re
from HTTPShared import *

import addresswebservices
import web

from rest_config import SERVER_HTTP
from rest_config import PORT_NUMBER
from rest_config import SERVICES_WEB_PATH
from rest_config import SERVER_PATH_DEPTH

def getFileContent(fileName):
    f = open(fileName)
    s = f.read()
    f.close()
    return s

def ProcessRequest(page, queryParams, response):
    addresswebservices.console.clear()
    pageBuilder = addresswebservices.ServicesHTMLPageBuilder()
    if page in ["/", ""]:
        response.htmlData = pageBuilder.getServicesHTMLPage("", {})
        response.handled = True
    elif page.find(".") >= 0:
        response.htmlData =  getFileContent(SERVICES_WEB_PATH + page) # TODO Implementovat vracení binárních souborů
        response.handled = True
    else:
        fullPathList = page.split("/")                                # REST parametry
        if SERVER_PATH_DEPTH != 0:
            fullPathList = fullPathList[SERVER_PATH_DEPTH:]
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
    import os
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
            query[item.name] = item.value

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