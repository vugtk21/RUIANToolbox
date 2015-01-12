# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        config
# Purpose:     Implements services config class.
#
# Author:      Radek Augustýn
# Copyright:   (c) VUGTK, v.v.i. 2014
# License:     CC BY-SA 4.0
#-------------------------------------------------------------------------------

import shared; shared.setupPaths(depth = 2)

from SharedTools.config import Config, RUIANImporterConfig

servicesConfigAttrs = {
                "serverHTTP" : 'www.vugtk.cz',
                "portNumber" : 80,
                "servicesWebPath" : "euradin/services/rest.py/",
                "databaseHost" : "192.168.1.93",
                "databasePort" : "5432",
                "databaseName" : "euradin",
                "databaseUserName" : "postgres",
                "databasePassword" : "postgres",
                "noCGIAppServerHTTP" : "localhost",
                "noCGIAppPortNumber" : 5689,
                "issueNumber": "",
                "issueShortDescription" : "",
                "ruianVersionDate" : "",
                "disableGUISwitch" : "false"
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

    config.issueNumber = "pro úpravy po 5.1.2015"
    config.issueShortDescription = u""", <a href="https://github.com/vugtk21/RUIANToolbox/issues?q=milestone%3A%22Konzultace+5.1.2014%22">podrobnosti na GitHub</a>.
<br>
<br>
<br><a href="https://github.com/vugtk21/RUIANToolbox/issues/132">#132 Zobrazený text při rozbalení našeptávače Ulice</a>
<br>Tak myslím že to funguje. Opět je to otázka názoru jak moc je to intuitivní, ale uvidíme.
<br>
<br><a href="https://github.com/vugtk21/RUIANToolbox/issues/133">#133 Funkce doplň adresu při více než jednom záznamu</a>
<br>Zvolil jsem stránku o 15 záznamech tak, aby byla podobně vysoká jako blok vstupních polí adresy. Dynamicky se tlačítka Další, případně Předchozí, pokud je to potřeba. Také se zobrazí celkový počet záznamů, pokud je seznam větší než stránka.
<br>
<br>Po vybrání adresy se kromě vyplnění vstupních polí adresa zobrazí na stránce.
<br>
<br>Příklad: školní, nádražní, budovatelů, rooseveltova apod.
<br>
<br><a href="https://github.com/vugtk21/RUIANToolbox/issues/134">#134 Zobrazený text při rozbalení našeptávače Ulice</a>
<br>Po úpravě viz #133 se najdou tři záznamy 187, 188, 1800 a je možno si z nich vybrat.
<br>
<br><a href="https://github.com/vugtk21/RUIANToolbox/issues/135">#135 Písmeno čísla orientačního může být také prázdné</a>
<br>
<br><a href="https://github.com/vugtk21/RUIANToolbox/issues/136">#136 Nádražní, Lhotka neumožní číslo popisné</a>
<br>Doplněna hláška, když v dané kombinaci nejde nalézt adresu.
<br>
<br><a href="https://github.com/vugtk21/RUIANToolbox/issues/138">#138 Neověří adresu Mezilesní 550</a>
<br>
<br><a href="https://github.com/vugtk21/RUIANToolbox/issues/139">#139 Neověří a nedoplní Mezilesní 550 bez PSČ</a>
<br>
<br><a href="https://github.com/vugtk21/RUIANToolbox/issues/140">#140 Nedoplní PSČ pro Mezilesní 550 s vyplněným MOP</a>
<br>
<br><a href="https://github.com/vugtk21/RUIANToolbox/issues/141">#141 Ošetření asynchronních volání</a>
<br>
<br><a href="https://github.com/vugtk21/RUIANToolbox/issues/145">#145 Doplnit datalisty u obcí bez ulic</a>
"""

    # htmlDataURL nemá mít lomítko na začátku
    #if config.htmlDataURL != "" and config.htmlDataURL[:1] == "/":
    #    config.htmlDataURL = config.htmlDataURL[1:]

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


config = Config("RUIANServices.cfg", servicesConfigAttrs, convertServicesCfg, moduleFile = __file__)

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
    if _isFirstCall and not shared.isCGIApplication:
        global SERVER_HTTP
        SERVER_HTTP = config.noCGIAppServerHTTP

        global PORT_NUMBER
        PORT_NUMBER = config.noCGIAppPortNumber

        global SERVICES_WEB_PATH
        SERVICES_WEB_PATH = ""

        global HTMLDATA_URL
        HTMLDATA_URL = "html/"

    global _isFirstCall
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