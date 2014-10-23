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

    config.issueNumber = "60"
    config.issueShortDescription = u"""
<br><br>
<table>
    <tr valign='top'>
        <td>Popis:</td><td>Kontrola číselných položek na portálu<br>
V číselných polích formulářů, jejichž které jsou kontrolovány funkcí isNumber,
reaguje klávesnice pouze na znaky 0..9, všechny ostatní klávesy jsou ignorovány. Jedná se také o řídící klávesy
typu Backspace, delete, pohyb kurzoru apod.<br>
Jedná se o následující pole: Identifikátor, Číslo popisné, Číslo evidenční, Číslo orientační, PSČ, Číslo městského
obvodu v Praze, JTSK Y, JTSK X.
</td>
    </tr>
    <tr valign='top'>
        <td>Řešení:</td>
        <td>
Tato chyba se projevuje pouze v prohlížeči Firefox.<br>
Firefox posílá na rozdíl od ostatních prohlížečů do události onkeypress všechny stisknutí klávesnice včetně řídících znaků.
Událost event, kterou je možno využít má proto navíc vlastnost isChar, která je True pokud se nejedná o řídící znak.
<br>
<code>
<pre>
function isNumber(event, scope, numDigits, maxValue)
{
 if ((event.isChar == undefined) || (event.isChar)) {
    value = scope.value +  String.fromCharCode(event.charCode);
    numValue = Number(value);
    if (isNaN(value)) return false;
    if ( (numDigits > 0) && (value.length > numDigits) ) return false;
    if ( (maxValue > 0) && (numValue > maxValue)) return false;
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



