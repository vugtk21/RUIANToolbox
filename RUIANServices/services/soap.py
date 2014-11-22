#!C:/Python27/python.exe
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        soap.py
# Purpose:     Implements soap interface to implemented functionality.
#
# Author:      Radek Augustýn
# Copyright:   (c) VUGTK, v.v.i. 2014
# License:     CC BY-SA 4.0
#-------------------------------------------------------------------------------

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
from config import config

path = SERVICES_WEB_PATH.split("/")
serverPathDepth = 0
for item in path:
    if item != "":
        serverPathDepth = serverPathDepth + 1

def getHTMLPath():
    paths = os.path.dirname(__file__).split("/")
    paths = paths[:len(paths) - 1]
    return "/".join(paths) + "/html/"

def getWSDLPath():
    paths = os.path.dirname(__file__).split("/")
    paths = paths[:len(paths) - 1]
    return "/".join(paths) + "/soap/"

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

    response.htmlData = getFileContent(getWSDLPath() + "Euradin_sluzby.wsdl") # TODO Implementovat vracení binárních souborů
    response.mimeFormat = "text/xml"
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
        response = ProcessRequest(page, web.input(), HTTPResponse(False))
        if response.handled:
            web.header("Content-Type", response.mimeFormat + ";charset=utf-8")
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
            print "Content-Type: " + response.mimeFormat + ";charset=utf-8"   # HTML is following
            print                                           # blank line, end of headers
            #print response.htmlData.encode('utf-8')
            sys.stdout.write(response.htmlData.encode('utf-8'))
        else:
            print "doProcessRequest Error"

    else:
        config.serverHTTP = config.noCGIAppServerHTTP
        SERVER_HTTP = config.noCGIAppServerHTTP
        config.portNumber = config.noCGIAppPortNumber
        PORT_NUMBER = config.noCGIAppPortNumber

        app = MyApplication(urls, globals())
        app.run(port = config.noCGIAppPortNumber)