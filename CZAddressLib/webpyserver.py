#!C:/Python27/python.exe
# -*- coding: utf-8 -*-

import web
import re
import addresswebservices
import web

from webpyserver_config import SERVER_HTTP
from webpyserver_config import PORT_NUMBER
from webpyserver_config import SERVICES_WEB_PATH

def getFileContent(fileName):
    f = open(fileName)
    s = f.read()
    f.close()
    return s

def ProcessRequest(page, queryParams):
    addresswebservices.console.clear()
    if page in ["/", ""]:
        return addresswebservices.getServicesHTMLPage("", [])
    elif page.find(".") >= 0:
        return getFileContent(SERVICES_WEB_PATH + page) # TODO Implementovat vracení binárních souborů
    else:
        fullPathList = page.split("/")                                # REST parametry
        servicePathInfo = "/" + fullPathList[0]                       # první rest parametr
        pathInfos = fullPathList[1:]                                  # ostatní
        handled = False
        for service in addresswebservices.services:
            if (service.pathName == servicePathInfo) and (service.processHandler <> None):
                i = 0
                for pathValue in pathInfos:
                    if i < len(service.restPathParams):
                        queryParams[service.restPathParams[i].pathName[1:]] = pathValue   #přidání do slovníku, přepíše hodnotu se stejným klíčem
                    else:
                        # Too many parameters
                        addresswebservices.console.addMsg(u"Nadbytečný REST parametr č." + str(i) + "-" + pathValue)

                    i = i + 1
                handled = service.processHandler(queryParams)
                break

        if not handled:
            s = addresswebservices.getServicesHTMLPage(servicePathInfo, queryParams)
            return s

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
        s = ProcessRequest(page, web.input(_unicode=False))
        if s <> "":
            web.header("Content-Type", 'text/html') # Set the Header

        return s

    def GET(self, page):
        return self.doProcessRequest(page)

    def POST(self, page):
        return self.doProcessRequest(page)

if __name__ == "__main__":
    app = MyApplication(urls, globals())
    app.run(port = PORT_NUMBER)