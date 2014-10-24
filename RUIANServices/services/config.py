# -*- coding: utf-8 -*-
__author__ = 'Augustyn'

import shared; shared.setupPaths(depth = 2)

from SharedTools.config import Config

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

    config.issueNumber = "63"
    config.issueShortDescription = u"""
<br><br>
<table>
    <tr valign='top'>
        <td>Popis:</td><td>Optimalizovat pořadí vstupních polí. Pořadí vstupních polí při zadání jednotlivých prvků adresy optimalizovat tak,
        aby odpovídalo přístupu ČÚZK, za vzor je možné si vzít aktuální VDP.
        Například obec by měla být určena dříve než ulice.</td>
    </tr>
    <tr valign='top'>
        <td>Řešení:</td>
        <td>
Pořadí vstupních polí pro zadávání adresy bylo voleno podle vzoru z VDP <code>Ověření adresy</code>.
Nově bude pořadí připraveno podle vzoru <code>Adresní místo</code>.
<br>Cíle osvětové činnosti v tomto směru mi nesjou zcela zřejmé, samotné vyhledávání adresního místa na VDP je poměrně
nepřehledné, zřejmě proto, že charakteristika adresního místa vznikala historicky různorodými požadavky.
<br>Jestli jsem dobře pochopil, cílem je předřadit vstupní pole <code>Obec</code> a <code>Část obce</code> před pole ulice na záložkách
<code>Geokódování</code>, <code>Sestavení adresy</code> a <code.Ověření adresy</code>. Takto je to realizováno.
        </td>
    </tr>
</table>"""

    # htmlDataURL nemá mít lomítko na začátku
    #if config.htmlDataURL != "" and config.htmlDataURL[:1] == "/":
    #    config.htmlDataURL = config.htmlDataURL[1:]

config = Config("RUIANServices.cfg",
            {
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
                "issueShortDescription" : ""
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



