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

class RestParam:
    def __init__(self, pathName, caption, shortDesc, htmlDesc = ""):
        self.pathName  = pathName
        self.caption   = caption
        self.shortDesc = shortDesc
        self.htmlDesc  = htmlDesc

class WebService:
    def __init__(self, pathName, caption, shortDesc, htmlDesc = "", restPathParams = [], processHandler = None):
        ''' '''
        self.pathName  = pathName
        self.caption   = caption
        self.shortDesc = shortDesc
        self.htmlDesc  = htmlDesc
        self.restPathParams = restPathParams
        self.processHandler = processHandler
        pass

    def getServicePath(self):
        result = self.pathName
        for param in self.restPathParams:
            result = result + param.pathName
        return result

    def processHTTPRequest(self, path, queryParams):
        pass

def getServicesHTMLPage():
    result = u'''
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
    $( "#tabs" ).tabs();
});
    </script>
    <body>
    <h1>#PAGETITLE#</h1>
<div id="tabs">
  <ul>
    <li><a href="#tabs-0">Info</a></li>
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
    result = result.replace("#PAGETITLE#", u"Webové služby RÚIAN")

    tabCaptions = ""
    tabDivs = ""
    def tablePropertyRow(name, value):
        return '<tr><td>' + name + ' </td><td><input></td><td>' + value + '</td></tr>\n'

    i = 1
    for service in services:
        tabCaptions += '<li><a href="#tabs-' + str(i) + '">' + service.caption + '</a></li>\n'
        tabDivs += '<div id="tabs-' + str(i) + '">   <h2>' + service.shortDesc + '</h2>\n'
        tabDivs += '<table>\n'
        tabDivs += u"Adresa služby" + service.getServicePath()
        tabDivs += '<form id="form_' + str(i) + '" name="form_' + str(i) + '" action="WebServices.html" method="get">'
        for param in service.restPathParams:
            tabDivs += tablePropertyRow(param.pathName, param.caption)
        tabDivs += '</form>'
        tabDivs += '</table>\n'
        tabDivs += '<input type="submit" value="Submit">\n'
        tabDivs += '<br>\n<img src=".' + service.pathName + '.png">\n'
        tabDivs += '</div>\n'
        i = i + 1

    result = result.replace("<#TABCAPTIONS#/>", tabCaptions)
    result = result.replace("<#TABDIVS#/>", tabDivs)
    return result

def main():
    services.append(
        WebService("/Geocode", u"Geokódování", u"Vyhledávání adresního bodu adresního místa", "",
                [
                    RestParam("/Format", u"Formát výsledku služby", "XML, Text, HTML"),
                    RestParam("/AddressPlaceId", u"Identifikátor adresního místa, kterou chceme geokódovat", "")
                ],
                None
        )

    )
    services.append(
        WebService("/CompileAddress", u"Sestavení adresy", u"Formátování adresy ve standardizovaném tvaru", "",
            [
                RestParam("/Format", u"Formát výsledku služby", "XML, Text, HTML"),
                RestParam("/AddressPlaceId", u"Identifikátor adresního místa, kterou chceme geokódovat", ""),
                RestParam("/ResultFormat", u"Výsledný formát adresy", "")
            ],
            None
        )
    )
    services.append(
        WebService("/FullTextSearch", u"Fulltextové vyhledávání", u"Vyhledávání adresního místa podle řetězce", "",
            [
                RestParam("/Format", u"Datový formát výsledku", "XML, Text, HTML"),
                RestParam("/<SearchFlag>", u"Upřesnění způsobu vyhledávání", u"Nearest record - nejbližší adresa, All records - podobné adresy")
                #RestParam("SearchText", u"Vyhledávaný řetězec"),
                #RestParam("ReturnOptions", u"Specifikace úplnosti vrácené")

            ],
            None)
    )
    services.append(
        WebService("/Validate", u"Ověření adresy", u"Ověřuje existenci dané adresy", "", [], None)
    )

    file = codecs.open("..//html//WebServices.html", "w", "utf-8")
    file.write(getServicesHTMLPage())
    file.close()
    pass

if __name__ == '__main__':
    main()
