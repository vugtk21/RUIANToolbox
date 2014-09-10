# -*- coding: utf-8 -*-
__author__ = 'Augustyn'

# Setup path to RUIANToolbox
import os.path, sys
basePath = os.path.join(os.path.dirname(__file__), "../..")
if not basePath in sys.path: sys.path.append(basePath)

from SharedTools.config import Config
import os

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

    # htmlDataURL nemá mít lomítko na začátku
    if config.htmlDataURL != "" and config.htmlDataURL[:1] == "/":
        config.htmlDataURL = config.htmlDataURL[1:]



config = Config("RUIANServices.cfg",
            {
                "serverHTTP" : 'www.vugtk.cz',
                "portNumber" : 80,
                "servicesWebPath" : "euradin/services/rest.py/",
                "htmlDataDir"  : "Downloads\\",
                "htmlDataURL"  : '/euradin/ruian_html/',
                "databaseHost" : "192.168.1.93",
                "databasePort" : "5432",
                "databaseName" : "euradin",
                "databaseUserName" : "postgres",
                "databasePassword" : "postgres",
                "noCGIAppServerHTTP" : "localhost",
                "noCGIAppPortNumber" : 5689
            },
           convertServicesCfg,
           moduleFile = __file__)



def getPortSpecification():
    if config.portNumber == 80:
        return ""
    else:
        return ":" + str(config.portNumber)

SERVER_HTTP = config.serverHTTP

PORT_NUMBER = config.portNumber
SERVICES_WEB_PATH = config.servicesWebPath
HTMLDATA_URL = config.htmlDataURL



