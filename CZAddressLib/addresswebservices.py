# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      raugustyn
#
# Created:     13/11/2013
# Copyright:   (c) raugustyn 2013
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import codecs

from HTTPShared import *
import compileaddress
from rest_config import *

SERVICES_PATH = '' # 'services'
class Console():
    consoleLines = ""
    def addMsg(self, msg):
        msg = '<div class="ui-widget">' \
                '<div class="ui-state-error ui-corner-all" style="padding: 0 .7em;">' \
                '<p><span class="ui-icon ui-icon-alert" style="float: left; margin-right: .3em;"></span>' \
                '<strong>Chyba: </strong>' + msg + '</p></div></div>'
        self.consoleLines += msg + "\n"

    def clear(self):
        self.consoleLines = ''

console = Console()

class ServicesHTMLPageBuilder:
    pageTemplate = u'''
<html>
    <meta http-equiv="Content-type" content="text/html; charset=utf-8" />
    <style>
        body { font-family: Tahoma }
    </style>
    <title>#PAGETITLE#</title>
    <link rel="stylesheet" href="http://code.jquery.com/ui/1.10.3/themes/smoothness/jquery-ui.css" />
    <script src="http://code.jquery.com/jquery-1.9.1.js"></script>
    <script src="http://code.jquery.com/ui/1.10.3/jquery-ui.js"></script>
    <link rel="stylesheet" href="http://jqueryui.com/resources/demos/style.css" />
    <script>
$(function() {
    $( "#tabs" ).tabs(#TABSOPTIONS#);
});
    </script>

    <script>
function onChangeProc(formElem, urlSpanElem, servicePath)
{
 formNameLen = formElem.name.length + 1;
 console = document.getElementById("console");
 elements = formElem.elements;
 s = ""
 needToOpenQuery = true
 for (i=0; i < elements.length; i++){
    name = elements[i].name.substr(formNameLen);
	if (name.charAt(0) == "/") {
		if (elements[i].value == "") {
			s = s + "/&#60;" + name.substr(1) + "&#62;";
		}
		else {
			s = s + "/" + elements[i].value;
		}
	}
	else {
		if (needToOpenQuery) {
			delimeter = "?";
			needToOpenQuery = false;
		}
		else {
			delimeter = "&";
		}
		if (name != "") {
			s = s + delimeter + name + "=" + escape(elements[i].value);
		}
	}

 }
 urlSpanElem.innerHTML = "/REST" + servicePath + s + "\\n";
}
    </script>
      <style>
  label {
    display: inline-block;
    width: 5em;
  }
  </style>

    <body>
    <h1>#PAGETITLE#</h1>
    #CONSOLELINES#
<div id="tabs">
  <ul>
    <li><a href="#tabs-0">Popis služeb</a></li>
    <#TABCAPTIONS#/>
  </ul>
    <div id="tabs-0">
    <p>
    Tento portál umožňuje využívat kopii databáze Registru Územních Identifikací, Adres a Nemovitostí (RÚIAN) pomocí webových služeb.
    <br>
    <br>
    Jednotlivé služby je možné využívat pomocí standardů Representational State Transfer (REST) a
    Simple Object Access Protocol (SOAP)/Web Services Description Language (WSDL).
    Každá záložka obsahuje popis jedné služby včetně parametrů.
    </p>
    <img src="#HTMLDATA_URL#WebServices.png" >
    </div>
  <#TABDIVS#/>
</div>


    </body>
</html>
    '''
    def normalizeQueryParams(self, queryParams):
        """ Parametry odesílané v URL requestu do query z HTML fomulářů musí být použity bez jména formuláře,
        tj. 'form_2_/AddressPlaceId' se spráně jmenuje 'AddressPlaceId'.
        """
        result = {}
        for key in queryParams:
            result[key[key.find("/") + 1:]] = queryParams[key]
        return result

    def tablePropertyRow(self, param, formName, paramTypeStr, queryParams, onChangeProcCode):
        keyName = param.name[1:]
        if queryParams.has_key(keyName):
            valueStr = 'value = "' + queryParams[keyName] + '"'
        else:
            valueStr = ""

        result = '<tr>'
        result += '<td>' + param.caption + ' </td><td>'
        result += '<input name="' + formName + '_' + param.name + '" ' + valueStr + 'title="' + \
                  param.shortDesc + ', parametr ' + param.name + \
                  '" onchange="' + onChangeProcCode + '" />'
        #result += '<td>' + param.name + ' </td><td>'
        result += '</tr>'
        return result

    def getServicesHTMLPage(self, pathInfo, queryParams):
        result = self.pageTemplate.replace("#PAGETITLE#", u"Webové služby RÚIAN")
        result = result.replace("#HTMLDATA_URL#", HTMLDATA_URL)

        queryParams = self.normalizeQueryParams(queryParams)

        tabCaptions = ""
        tabDivs = ""

        i = 1
        tabIndex = 0
        for service in services:
            tabCaptions += '<li><a href="#tabs-' + str(i) + '">' + service.caption + '</a></li>\n'
            tabDivs += '<div id="tabs-' + str(i) + '">   <h2>' + service.shortDesc + '</h2>\n'
            tabDivs += service.htmlDesc
            tabDivs += u"<br><p>Adresa služby:" + service.pathName + "</p>\n"
            formName = "form_" + str(i)
            urlSpanName = formName + "_urlSpan"
            onChangeProcCode = 'onChangeProc(' + formName + "," + urlSpanName + ", '" + service.pathName + "')"
            if service.pathName == pathInfo:
                tabIndex = i

            tabDivs += '<form id="' + formName + '" name="' + formName + '" action="' + SERVICES_PATH + service.pathName + '" method="get">\n'

            # Parameters list
            tabDivs += '<table>\n'
            for param in service.restPathParams:
                tabDivs += self.tablePropertyRow(param, formName, u"REST", queryParams, onChangeProcCode)

            for param in service.queryParams:
                tabDivs += self.tablePropertyRow(param, formName, u"Query", queryParams, onChangeProcCode)

            tabDivs += '</table>\n'
            tabDivs += '<input type="button" value="' + service.sendButtonCaption + '" onclick="' + onChangeProcCode + '">\n'
            tabDivs += u'<span name="' + urlSpanName + '" id="' + urlSpanName + '" >' + service.getServicePath() + "</span>\n"
            tabDivs += '</form>\n'

            tabDivs += '<p>\n<img src="' + HTMLDATA_URL + service.pathName + '.png"></p>\n'

            tabDivs += '</div>\n'
            i = i + 1

        if tabIndex == 0:
            newStr = ""
        else:
            newStr = '{ active: ' + str(tabIndex) + ' }'
        result = result.replace("#TABSOPTIONS#", newStr)

        result = result.replace("#CONSOLELINES#", console.consoleLines)
        result = result.replace("<#TABCAPTIONS#/>", tabCaptions)
        result = result.replace("<#TABCAPTIONS#/>", tabCaptions)
        result = result.replace("<#TABDIVS#/>", tabDivs)
        return result

def geoCodeServiceHandler(queryParams, response):
    return response

def dummyServiceHandler(queryParams, response):
    return response

#TODO Blank todo
def createServices():
    services.append(
        WebService("/Geocode", u"Geokódování", u"Vyhledávání adresního bodu adresního místa",
            u"""<p>Umožňuje klientům jednotným způsobem získat souřadnice zadaného adresního místa.
            Adresní místo zadáme buď pomocí jeho identifikátoru RÚIAN nebo pomocí textového řetězce adresy.<br>""",
            [
                getResultFormatParam()
            ],
            [
                getAddressPlaceIdParamURL(),
                getSearchTextParam()
            ],
            geoCodeServiceHandler,
            sendButtonCaption = u"Najdi polohu"
        )

    )
    services.append(
        WebService("/FullTextSearch", u"Fulltextové vyhledávání", u"Vyhledávání adresního místa podle řetězce",
            u"""Umožňuje nalézt a zobrazit seznam pravděpodobných adres na základě textového řetězce adresy.
            Textový řetězec adresy může být nestandardně formátován, nebo může být i neúplný.""",
            [
                getResultFormatParam(),
                RestParam("/SearchFlag", u"Způsob vyhledávání", u"Upřesnění způsobu vyhledávání (Match, Similar)")
            ],
            [
                getSearchTextParam()
            ],
            dummyServiceHandler,
            sendButtonCaption = u"Vyhledej adresu"
        )
    )
    services.append(
        WebService("/Validate", u"Ověření adresy", u"Ověřuje existenci dané adresy",
                   u"""Umožňuje ověřit zadanou adresu. Adresa je zadána pomocí jednotlivých
                   prvků adresního místa.""",
            [
                getResultFormatParam(),
                RestParam("/Street",      u"Ulice", u"Název ulice"),
                RestParam("/Locality",    u"Obec", u"Obec"),
                RestParam("/HouseNumber", u"Číslo popisné", ""),
            ],
            [
                URLParam("ZIPCode",           u"PSČ", u"Poštovní směrovací číslo"),
                URLParam("LocalityPart",      u"Část obce", u"Část obce, pokud je známa"),
                URLParam("OrientationNumber", u"Číslo orientační", "")
            ],
            dummyServiceHandler,
            sendButtonCaption = u"Ověř adresu"
        )
    )
    compileaddress.createServiceHandlers()
    services.append(
        WebService("/ValidateAddressId", u"Ověření identifikátoru adresy", u"Ověřuje existenci daného identifikátoru adresy",
                   u"""Umožňuje ověřit existenci zadaného identifikátoru adresy RÚIAN v databázi.""",
            [
                getResultFormatParam(),
                getAddressPlaceIdParamRest()
            ],
            [ ],
            dummyServiceHandler,
            sendButtonCaption = u"Ověř identifikátor adresy"
        )
    )
    services.append(
        WebService("/NearbyAddresses", u"Blízké adresy", u"Hledá adresu nejbližší daným souřadnicím",
                   u"""Umožňuje vyhledat adresní místa v okolí zadaných souřadnic do určité vzdálenosti.
                   Vrací záznamy databáze RÚIAN setříděné podle vzdálenosti od zadaných souřadnic.""",
            [
                getResultFormatParam(),
                RestParam("/JTSKX", u"JTSK X", u"Souřadnice X v systému S-JTSK"),
                RestParam("/JTSKY", u"JTSK Y", u"Souřadnice Y v systému S-JTSK"),
                RestParam("/Distance", u"Vzdálenost", u"Vzdálenost v metrech od vloženého bodu")
            ],
            [ ],
            dummyServiceHandler,
            sendButtonCaption = u"Hledej blízké adresy"
        )
    )

    pass

createServices()

def main():
    # Build HTML page with service description
    pageBuilder = ServicesHTMLPageBuilder()
    pageContent = pageBuilder.getServicesHTMLPage("", {})

    # Write result into file
    file = codecs.open("..//html//WebServices.html", "w", "utf-8")
    file.write(pageContent)
    file.close()

    pass

if __name__ == '__main__':
    main()