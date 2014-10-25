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

    config.issueNumber = "73.2"
    config.issueShortDescription = u"""
<br><br>
<table>
    <tr valign='top'>
        <td>Popis:</td><td>Maska pro vstupní pole <code>Písmeno čísla orientačního</code><br>
Ve vstupním poli "písmeno čísla orientačního" by měly být možné zadat pouze hodnoty české abecedy bez háčků a čárek,
"a..z", "A..Z", včetně "ch" a "CH".
        </td>
    </tr>
    <tr valign='top'>
        <td>Řešení:</td>
        <td>Ve vstupních polích na záložkách <code>Geokódování</code>, <code>Sestavení adresy</code> a
<code>Ověření adresy</code> se kontrolují zadávané hodnoty tak, aby byl akceptován pouze jeden znak z anglické abecedy
(tj. české abecedy bez diakritiky) a česká písmena <code>ch</code> a <code>CH</code>.
<code>
    <pre>
function isCZLetter(event, scope)
{
 if ((event.isChar == undefined) || (event.isChar)) {
    value = scope.value +  String.fromCharCode(event.charCode);
    if (scope.value != "") {
       return (value == "ch") || (value == "CH");
    }
    else {
        charStr = String.fromCharCode(event.charCode);
        return "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ".indexOf(charStr) != -1;
    }
 }

 return true;
}
    </pre>
</code>
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



