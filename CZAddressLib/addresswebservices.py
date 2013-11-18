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

services = []
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

class URLParam:
    def __init__(self, name, caption, shortDesc, htmlDesc = ""):
        self.name  = name
        self.caption   = caption
        self.shortDesc = shortDesc
        self.htmlDesc  = htmlDesc

class RestParam(URLParam):
    def __init__(self, pathName, caption, shortDesc, htmlDesc = ""):
        URLParam.__init__(self, pathName, caption, shortDesc, htmlDesc)

    def getPathName(self):
        return self.name

    pathName = property(getPathName, "REST path name")


class WebService:
    def __init__(self, pathName, caption, shortDesc, htmlDesc = "", restPathParams = [], queryParams = [],
                 processHandler = None, sendButtonCaption = u"Odeslat"):
        ''' '''
        self.pathName  = pathName
        self.caption   = caption
        self.shortDesc = shortDesc
        self.htmlDesc  = htmlDesc
        self.restPathParams = restPathParams
        self.queryParams = queryParams
        self.processHandler = processHandler
        self.sendButtonCaption = sendButtonCaption
        self._params = None
        pass

    def getParams(self):
        if self._params == None or len(self.restPathParams) + len(self.queryParams) != len(self._params):
            self._params = {}
            self._params.update(self.restPathParams)
            self._params.update(self.queryParams)

        return self._params

    params = property(getParams, "REST and Query params together")

    def getServicePath(self):
        result = self.pathName
        for param in self.restPathParams:
            result = result + "/&#60;" + param.pathName[1:] + "&#62;"
        if len(self.queryParams) > 0:
            queryParamsList = []
            result += "?"
            for param in self.queryParams:
                queryParamsList.append(param.name + "=")
            result += "&".join(queryParamsList)

        return result

    def buildServiceURL(self, queryParams):
        result = self.pathName
        for param in self.restPathParams:
            result = result + param.pathName
        if len(self.queryParams) > 0:
            queryParamsList = []
            result += "?"
            for param in self.queryParams:
                if queryParams.has_key(param.name):
                    valueStr = queryParams[param.name]
                else:
                    valueStr = ""
                queryParamsList.append(param.name + "=" + valueStr)
            result += "&".join(queryParamsList)

        return result

    def processHTTPRequest(self, path, queryParams):
        pass


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
 urlSpanElem.innerHTML = servicePath + s + "\\n";
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
    <h2>Info</h2>
    <br>
    V rámci vytvoření a ověření postupů popsaných v této metodice byly zprovozněny referenční služby na adrese http://www.vugtk.cz/euradin/Services.
    Tyto služby jsou určeny ke kontrole správné funkčnosti implementací, které budou v souladu s touto metodikou a procesů, které je využívají.
    <img src="./Geocode.png" \>
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
        result += '<input name="' + formName + '_' + param.name + '" ' + valueStr + 'title="' + param.shortDesc + \
                  '" onchange="' + onChangeProcCode + '" />'
        result += '<td>' + param.name + ' </td><td>'
        result += '</tr>'
        return result

    def getServicesHTMLPage(self, pathInfo, queryParams):
        result = self.pageTemplate.replace("#PAGETITLE#", u"Webové služby RÚIAN")
        queryParams = self.normalizeQueryParams(queryParams)

        tabCaptions = ""
        tabDivs = ""

        i = 1
        tabIndex = 0
        for service in services:
            tabCaptions += '<li><a href="#tabs-' + str(i) + '">' + service.caption + '</a></li>\n'
            tabDivs += '<div id="tabs-' + str(i) + '">   <h2>' + service.shortDesc + '</h2>\n'
            tabDivs += service.htmlDesc
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
            tabDivs += u'REST <span name="' + urlSpanName + '" id="' + urlSpanName + '" >' + service.getServicePath() + "</span>\n"
            tabDivs += '</form>\n'
            #tabDivs += u"URL služby:" + service.buildServiceURL(queryParams) + "<br>\n"

            tabDivs += u"<p>Adresa služby:" + service.pathName + "</p>\n"
            tabDivs += '<p>\n<img src=".' + service.pathName + '.png"></p>\n'

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

def geoCodeServiceHandler(queryParams):
    return False

def dummyServiceHandler(queryParams):
    return False

RESULT_FORMAT_DESCRIPTION = "(HTML, XML, Text, JSON)"

def getResultFormatParam():
    return RestParam("/Format", u"Formát výsledku", u"Formát výsledku služby " + RESULT_FORMAT_DESCRIPTION)

def getSearchTextParam():
    return URLParam("SearchText", u"Adresa", u"Textový řetězec adresy")

def getAddressPlaceIdParamRest():
    return RestParam("/AddressPlaceId", u"Identifikátor", u"Identifikátor adresního místa")

def getAddressPlaceIdParamURL():
    return URLParam("AddressPlaceId", u"Identifikátor", u"Identifikátor adresního místa")

#TODO Blank todo
def createServices():
    services.append(
        WebService("/Geocode", u"Geokódování", u"Vyhledávání adresního bodu adresního místa",
            u"""<p>Tato webová služba umožňuje klientům jednotným způsobem získat souřadnice zadaného adresního místa.
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
        WebService("/CompileAddress", u"Sestavení adresy", u"Formátování adresy ve standardizovaném tvaru",
            u"""Tato webová služba sestavit zápis adresy ve standardizovaném tvaru podle § 6 vyhlášky č. 359/2011 Sb.,
            kterou se provádí zákon č. 111/2009 Sb., o základních registrech, ve znění zákona č. 100/2010 Sb.
            Adresní místo lze zadat buď pomocí jeho identifikátoru RÚIAN, textového řetězce adresy nebo jednotlivých prvků adresy.""",
            [
                getResultFormatParam()
            ],
            [
                getAddressPlaceIdParamURL(),
                getSearchTextParam()
            ],
            dummyServiceHandler,
            sendButtonCaption = u"Sestav adresu"
        )
    )
    services.append(
        WebService("/FullTextSearch", u"Fulltextové vyhledávání", u"Vyhledávání adresního místa podle řetězce",
            u"""Tato webová služba umožňuje nalézt a zobrazit seznam pravděpodobných adres na základě textového řetězce adresy.
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
                   u"""Tato webová služba umožňuje ověřit zadanou adresu. Adresa je zadána pomocí jednotlivých
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
    services.append(
        WebService("/ValidateAddressId", u"Ověření identifikátoru adresy", u"Ověřuje existenci daného identifikátoru adresy",
                   u"""Tato webová služba umožňuje ověřit existenci zadaného identifikátoru adresy RÚIAN v databázi.""",
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
        WebService("/SearchAddressPoints", u"Blízké adresy", u"Hledá adresu nejbližší daným souřadnicím",
                   u"""Tato webová služba nám umožní vyhledat adresní místa v okolí zadaných souřadnic do určité vzdálenosti.
                   Vrací záznamy databáze RÚIAN setříděné podle vzdálenosti od zadaných souřadnic.""",
            [
                getResultFormatParam(),
                RestParam("/JTSKX", u"JTSK X", u"Souřadnice X v systému S-JTSK"),
                RestParam("/JTSKY", u"JTSK Y", u"Souřadnice Y v systému S-JTSK")
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