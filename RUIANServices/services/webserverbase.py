#!C:/Python27/python.exe
# -*- coding: utf-8 -*-
__author__ = 'raugustyn'

# =============================================================================
"""
Knihovna pro zabalení funkcionality serveru.

Př.

import webserverbase

def processRequest(page, servicePathInfo, pathInfos, queryParams, response):
    response.htmlData = "<html><body>Empty</body></html>"
    response.handled = True
    return response

webserverbase.processRequestProc = processRequest

if __name__ == "__main__":
    webserverbase.mainProcess(processRequest)

"""
#  =============================================================================

import web
from HTTPShared import *
import os

from config import SERVER_HTTP, PORT_NUMBER, SERVICES_WEB_PATH

path = SERVICES_WEB_PATH.split("/")
serverPathDepth = 0
for item in path:
    if item != "":
        serverPathDepth = serverPathDepth + 1

SERVER_PATH_DEPTH = serverPathDepth

EMPTY_HTML_DATA = "<html><body>Empty</body></html>"

def _parsedProcessRequestProc(page, servicePathInfo, pathInfos, queryParams, response):
    response.htmlData = EMPTY_HTML_DATA
    response.handled = True
    return response

processRequestProc = _parsedProcessRequestProc

def _processRequestProc(page, queryParams, response):
    if page in ["/", ""]:
        response.htmlData = EMPTY_HTML_DATA
        response.handled = True
    elif page.find(".") >= 0:
        if os.path.exists(SERVICES_WEB_PATH + page):
            f = open(SERVICES_WEB_PATH + page)
            response.htmlData = f.read()  # TODO Implementovat vracení binárních souborů
            f.close()
            response.handled = True
        else:
            response.htmlData = EMPTY_HTML_DATA
            response.handled = True
    else:
        fullPathList = page.split("/")                                # REST parametry
        if SERVER_PATH_DEPTH != 0:
            fullPathList = fullPathList[SERVER_PATH_DEPTH:]
        #TODO PathInfo by mělo být až za adresou serveru - zkontolovat jak je to na Apache
        if len(fullPathList) > 0:
            servicePathInfo = "/" + fullPathList[0]                       # první rest parametr
        else:
            servicePathInfo = "/"

        pathInfos = fullPathList[1:]                                  # ostatní
        response = processRequestProc(page, servicePathInfo, pathInfos, queryParams, response)

    return response

urls = ('/(.*)', 'handler')

class ServerApplication(web.application):
    def run(self, port, *middleware):
        func = self.wsgifunc(*middleware)
        return web.httpserver.runsimple(func, (SERVER_HTTP, port))

class favicon:
    def GET(self):
        pass

class handler:
    def doProcessRequest(self, page):
        response = _processRequestProc(page, web.input(), HTTPResponse(False))
        if response.handled:
            web.header("Content-Type", response.mimeFormat + ";charset=utf-8")
            return response.htmlData
        else:
            return "doProcessRequest Error"

    def GET(self, page):
        return self.doProcessRequest(page)

    def POST(self, page):
        return self.doProcessRequest(page)

def mainProcess(aProcessRequestProc):
    global processRequestProc
    processRequestProc = aProcessRequestProc
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
            query[item.name] = unicode(item.value, "utf-8")

        response = _processRequestProc(pathInfo, query, HTTPResponse(False))
        if response.handled:
            print "Content-Type: " + response.mimeFormat + ";charset=utf-8"   # HTML is following
            print                                           # blank line, end of headers
            print response.htmlData.encode('utf-8')
        else:
            print "doProcessRequest Error"

    else:
        app = ServerApplication(urls, globals())
        app.run(port = 4567) #PORT_NUMBER)