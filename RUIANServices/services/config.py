# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
# Name:        config
# Purpose:     Implements services config class.
#
# Author:      Radek Augustýn
# Copyright:   (c) VUGTK, v.v.i. 2014
# License:     CC BY-SA 4.0
# -------------------------------------------------------------------------------

import shared
shared.setupPaths(depth=2)

from sharedtools.config import Config, RUIANImporterConfig

servicesConfigAttrs = {
                "serverHTTP": 'www.vugtk.cz',
                "portNumber": 80,
                "servicesWebPath": "euradin/services/rest.py/",
                "databaseHost": "192.168.1.93",
                "databasePort": "5432",
                "databaseName": "euradin",
                "databaseUserName": "postgres",
                "databasePassword": "postgres",
                "noCGIAppServerHTTP": "localhost",
                "noCGIAppPortNumber": 5689,
                "issueNumber": "",
                "issueShortDescription": "",
                "ruianVersionDate": "",
                "disableGUISwitch": "false"
            }

def convertServicesCfg(config):
    if config == None: return

    if config.portNumber == "":
        config.portNumber = 80
    else:
        config.portNumber = int(config.portNumber)
    pass

    config.noCGIAppPortNumber = int(config.noCGIAppPortNumber)

    # noCGIAppServerHTTP nemůže být prázdné
    if config.noCGIAppServerHTTP == "":
        config.noCGIAppServerHTTP = "localhost"

    # servicesWebPath nemá mít lomítko na konci
    if config.servicesWebPath[len(config.servicesWebPath)-1:] == "/":
        config.servicesWebPath = config.servicesWebPath[:len(config.servicesWebPath) - 1]

    config.disableGUISwitch = config.disableGUISwitch.lower() == "true"

    config.issueNumber = "2.0.00"
    config.issueShortDescription = '' # u""", <a href="https://github.com/vugtk21/RUIANToolbox/issues?q=milestone%3A%22Konzultace+5.1.2014%22">podrobnosti na GitHub</a>."""

    importerAttrsMapper = {
        "databaseHost" : "host",
        "databasePort" : "port",
        "databaseName" : "dbname",
        "databaseUserName" : "user",
        "databasePassword" : "password"
    }
    importerConfig = RUIANImporterConfig()
    for servicesAttr in importerAttrsMapper:
        if config.attrs[servicesAttr] == servicesConfigAttrs[servicesAttr]:
            config.setAttr(servicesAttr, importerConfig.attrs[importerAttrsMapper[servicesAttr]])


config = Config("RUIANServices.cfg", servicesConfigAttrs, convertServicesCfg, moduleFile=__file__)

def getPortSpecification():
    if config.portNumber == 80:
        return ""
    else:
        return ":" + str(config.portNumber)

SERVER_HTTP = config.serverHTTP
PORT_NUMBER = config.portNumber
SERVICES_WEB_PATH = config.servicesWebPath
HTMLDATA_URL = "html/"

_isFirstCall = True
def setupVariables():
    global _isFirstCall
    global SERVER_HTTP
    global PORT_NUMBER
    global SERVICES_WEB_PATH
    global HTMLDATA_URL

    if _isFirstCall and not shared.isCGIApplication:
        SERVER_HTTP = config.noCGIAppServerHTTP
        PORT_NUMBER = config.noCGIAppPortNumber
        SERVICES_WEB_PATH = ""
        HTMLDATA_URL = "html/"

    _isFirstCall = False

def getCGIPath():
    serverItems = "/".split(SERVER_HTTP)
    return "/".join(serverItems[:len(serverItems) - 1])

def getHTMLDataURL():
    result = getServicesURL()
    if HTMLDATA_URL != "":
        result = result + "/" + HTMLDATA_URL
    return result

def getServicesURL():
    setupVariables()
    result = "http://" + SERVER_HTTP + getPortSpecification()
    if SERVICES_WEB_PATH != "":
        result = result + "/" + SERVICES_WEB_PATH
    return result

def getServicesPath():
    result = getServicesURL().split("/")
    result = result[:len(result) - 1]
    return "/".join(result)