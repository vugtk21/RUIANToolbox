#!C:/Python27/python.exe
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        addresswebservices
# Purpose:
#
# Author:      Ing. Radek Augustýn
#
# Created:     13/11/2013
# Copyright:   (c) raugustyn 2013
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import codecs

import fulltextsearch
import validate
import geocode
import nearbyaddresses
import validateaddressid
#import IDCheck

from HTTPShared import *
import compileaddress
from config import SERVER_HTTP
from config import getPortSpecification
from config import SERVICES_WEB_PATH
from config import HTMLDATA_URL

SERVICES_PATH = '' # 'services'

PAGE_TEMPLATE = u'''
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
    <link rel="shortcut icon" type="image/x-icon" href="#HTMLDATA_URL#" />
    <script>
$(function() {
    $( "#tabs" ).tabs(#TABSOPTIONS#);
});
    </script>


    <script>
    $(document).ready(function() {
      $('input:radio[name="radio/Geocode"],input:radio[name="radio/CompileAddress"]').change(function() {
        if (this.value == 'vstup') {
            $(this).parent().find("td input").removeAttr("disabled");
            $(this).parent().find("td input").eq(0).attr("disabled", "disabled");
            $(this).parent().find("td input").eq(1).attr("disabled", "disabled");
        }
        else if (this.value == 'id') {
            $(this).parent().find("td input").attr("disabled", "disabled");
            $(this).parent().find("td input").eq(0).removeAttr("disabled");
            $(this).parent().find("td input").eq(11).removeAttr("disabled");
        }
        else if (this.value == 'adresa') {
            $(this).parent().find("td input").attr("disabled", "disabled");
            $(this).parent().find("td input").eq(11).removeAttr("disabled");
            $(this).parent().find("td input").eq(1).removeAttr("disabled");
        }
      });
    });
  </script>

    <script type="text/javascript" charset="utf-8">

	function displayResult(id, servicePath){
        var url = "<#SERVICES_URL>" + temp
		var xmlHttp;
		try {// Firefox, Opera 8.0+, Safari
			xmlHttp = new XMLHttpRequest();
		} catch (e) {// Internet Explorer
			try {
				xmlHttp = new ActiveXObject("Msxml2.XMLHTTP");
			} catch (e) {
				try {
					xmlHttp = new ActiveXObject("Microsoft.XMLHTTP");
				} catch (e) {
					alert("Your browser does not support AJAX!");
					return false;
				}
			}
		}

		xmlHttp.onreadystatechange = function(){
			if (xmlHttp.readyState == 4) {
				//Get the response from the server and extract the section that comes in the body section of the second html page avoid inserting the header part of the second page in your first page's element
				//var respText = xmlHttp.responseText.split('<body>');
				//elem.innerHTML = respText[1].split('</body>')[0];
				elem.innerText = xmlHttp.responseText.replace(/<br>/g,"\\n");
			}
		}

		var elem = document.getElementById(id);
		if (!elem) {
			alert('The element with the passed ID'+ id +' does not exists in your page');
			return;
		}

		xmlHttp.open("GET", url, true);
		xmlHttp.send(null);


	}
    </script>


    <script type="text/javascript" charset="utf-8">
var temp;
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
			s = s + "/" + name.substr(1);
		}
		else {
			s = s + "/" + elements[i].value;
		}
	}
	else {
		if (needToOpenQuery) {
			delimeter = "";
			s = s + "?"
			needToOpenQuery = false;
		}
		else {
			delimeter = "&";
		}
		if (name != "" && name != "de") {
		    if (elements[i].value!="") {
			    s = s + delimeter + name + "=" + encodeURI(elements[i].value);
			}
		}
	}

 }
 urlSpanElem.innerHTML = "<#SERVICES_URL>"+ servicePath + s + "\\n";
 temp = servicePath + s;
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

<div style="width:80%">
<br>
<br>
<br>
<p>
<center>
<table>
    <tr>
        <td><img src="#HTMLDATA_URL#tacr_eng.png" height="55"></td>
        <td>
Webové služby RÚIAN byly vytvořeny v rámci čtvrté etapy projektu
TB01CUZK004: Výzkum uplatnění závěrů projektu eContentplus s názvem EURADIN v podmínkách RUIAN    (2012-2014)
        </td>
    </tr>
</table>
</center>
</p>
</div>

    </body>
</html>
    '''

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
        if param.name == '/Format':
            result += '<select input name="' + formName + '_' + param.name + 'title="' + param.shortDesc + ', parametr ' + param.name + '" onchange="' + onChangeProcCode + '">' + \
                            '<option value="text">text</option>' + \
                            '<option value="textToOneRow">text do řádku</option>' + \
                            '<option value="xml">xml</option>' + \
                            '<option value="html">html</option>' + \
                            '<option value="htmlToOneRow">html do řádku</option>' + \
                            '<option value="json">json</option>' + \
                    '</select>'
        else:
            if param.disabled:
                disabledStr = ' disabled="disabled" '
            else:
                disabledStr = ''

            if param.name == "SuppressID":
                inputTypeStr = ' type="checkbox" '
            else:
                inputTypeStr = ""


            result += '<input name="' + formName + '_' + param.name + '" ' + valueStr.decode('utf8') + 'title="' + \
                  param.shortDesc + ', parametr ' + param.name + \
                  '" onchange="' + onChangeProcCode + '" ' + disabledStr + inputTypeStr + '/>'

        result += '</tr>'
        return result

    def getServicesHTMLPage(self, pathInfo, queryParams):
        result = PAGE_TEMPLATE.replace("#PAGETITLE#", u"Webové služby RÚIAN")
        result = result.replace("<#SERVICES_URL>", "http://" + SERVER_HTTP + getPortSpecification() + "/" + SERVICES_WEB_PATH )


        url = "http://" + SERVER_HTTP + getPortSpecification() + "/" + HTMLDATA_URL
        result = result.replace("#HTMLDATA_URL#", url)

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
            displayResultProcCode = "displayResult('" + formName + "_textArea', '" + service.pathName + "')"
            if service.pathName == pathInfo:
                tabIndex = i

            tabDivs += u'<span name="' + urlSpanName + '" id="' + urlSpanName + '" >' + "http://" + SERVER_HTTP + getPortSpecification() + "/" + SERVICES_WEB_PATH + service.pathName[1:] + "</span>\n" #service.getServicePath() + "</span>\n"
            if service.pathName == "/CompileAddress" or service.pathName == "/Geocode":
                tabDivs += u"""
                <br><br>
                <input type="radio" name= "radio""" + service.pathName + u"""" value="id">Identifikátor RÚIAN
                <input type="radio" name= "radio""" + service.pathName + u"""" value="adresa"  checked>Textový řetězec adresy
                <input type="radio" name= "radio""" + service.pathName + u"""" value="vstup">Jednotlivé prvky adresy
                """

            tabDivs += "<br><br>"
            tabDivs += "<table><tr valign=\"top\"><td>"
            tabDivs += '<form id="' + formName + '" name="' + formName + '" action="' + SERVICES_PATH + service.pathName + '" method="get">\n'

            # Parameters list
            tabDivs += '<table>\n'
            for param in service.restPathParams:
                tabDivs += self.tablePropertyRow(param, formName, u"REST", queryParams, onChangeProcCode)

            for param in service.queryParams:
                tabDivs += self.tablePropertyRow(param, formName, u"Query", queryParams, onChangeProcCode)

            tabDivs += '</table>\n'

            tabDivs += '<br><input type="button" value="' + service.sendButtonCaption + '" onclick="' + onChangeProcCode + '; ' + displayResultProcCode + '">\n'
            tabDivs += '</form>\n'
            tabDivs += "</td><td>"
            tabDivs += '<textarea id=' + formName + '_textArea rows ="12" cols="50"></textarea>'
            tabDivs += "</td></tr></table>"

            tabDivs += "<a href='http://www.vugtk.cz/euradin/testing" + service.pathName + ".html'>show tests</a>"
            #tabDivs += "<a href='" + SERVER_HTTP + "/euradin/testing" + service.pathName + ".html'>show tests</a>"

            url = "http://" + SERVER_HTTP + getPortSpecification() + "/" + HTMLDATA_URL + service.pathName + '.png'
            tabDivs += '<p>\n<img src="' + url + '"></p>\n'

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

def createServices():
    geocode.createServiceHandlers()
    fulltextsearch.createServiceHandlers()
    compileaddress.createServiceHandlers()
    validate.createServiceHandlers()
    nearbyaddresses.createServiceHandlers()
    validateaddressid.createServiceHandlers()
#    IDCheck.createServiceHandlers()
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