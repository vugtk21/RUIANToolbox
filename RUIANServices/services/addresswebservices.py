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

from HTTPShared import *
import compileaddress
from config import SERVER_HTTP
from config import getPortSpecification
from config import SERVICES_WEB_PATH
import config as configmodule
from config import setupVariables

SERVICES_PATH = '' # 'services'

def getPageTemplate():
    f = codecs.open("..//HTML//RestPageTemplate.htm", "r", "utf-8")
    result = f.read()
    f.close()
    return result

class Console():
    consoleLines = ""
    infoLines = ""
    debugMode = False

    def addMsg(self, msg):
        msg = '<div class="ui-widget">' \
                '<div class="ui-state-error ui-corner-all" style="padding: 0 .7em;">' \
                '<p><span class="ui-icon ui-icon-alert" style="float: left; margin-right: .3em;"></span>' \
                '<strong>Chyba: </strong>' + msg + '</p></div></div>'
        self.consoleLines += msg + "\n"

    def addInfo(self, msg):
        if not self.debugMode: return

        msg = '<div class="ui-widget">' \
                '<div class="ui-state-error ui-corner-all" style="padding: 0 .7em;">' \
                '<p><span class="ui-icon ui-icon-alert" style="float: left; margin-right: .3em;"></span>' \
                '<strong>Info: </strong>' + msg + '</p></div></div>'
        self.infoLines += msg + "\n"

    def clear(self):
        self.consoleLines = ''
        self.infoLines = ""


console = Console()

def getIssueHTML():
    if configmodule.config.issueNumber == "":
        return ""
    else:
        result =  u'<div class="ui-widget">' \
                u'<div class="ui-state-error ui-corner-all" style="padding: 0 .7em;">' \
                u'<p><span class="ui-icon ui-icon-alert" style="float: left; margin-right: .3em;"></span>' \
                u'<strong>Návrh řešení požadavku č. ' + configmodule.config.issueNumber + u'</strong>'
        result += configmodule.config.issueShortDescription
        result += u'<p><a href="https://github.com/vugtk21/RUIANToolbox/issues/' + configmodule.config.issueNumber + '">Podrobnosti na GitHub</a></p>'
        result += u'</div></div>'

        return result

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

        if param.disabled:
            visibilityStr = ' style="display:none" '
        else:
            visibilityStr = ''

        result = '<tr id="' + formName + '_row_' + param.name + '"' + visibilityStr + '>'
        result += '<td align="right">' + param.caption + ' </td><td>'
        if param.name == '/Format':
            result += '<select input name="' + formName + '_' + param.name + '" title="' + param.shortDesc + '" onchange="' + onChangeProcCode + '">' + \
                            '<option value="text">text</option>' + \
                            '<option value="textToOneRow">text do řádku</option>' + \
                            '<option value="xml">xml</option>' + \
                            '<option value="html">html</option>' + \
                            '<option value="htmlToOneRow">html do řádku</option>' + \
                            '<option value="json">json</option>' + \
                    '</select>'
        elif param.name == 'ExtraInformation':
            if formName == "form_1":
                addressOption = '<option value="address">přidat adresu</option>'
            else:
                addressOption = ""

            result += '<select name="' + formName + '_' + param.name + '" title="' + param.shortDesc + '" onchange="' + onChangeProcCode + '" >' + \
                            '<option value="standard">žádné</option>' + \
                            '<option value="id">přidat ID</option>' + addressOption + \
                    '</select>'
        else:
            if False: #param.disabled:
                disabledStr = ' disabled="disabled" '
            else:
                disabledStr = ''

            elemID = formName + '_' + param.name
            result += '<input name="' + elemID + '" ' + valueStr.decode('utf8') + 'title="' + \
                  param.shortDesc + '" onchange="' + onChangeProcCode + '" ' + disabledStr + param.htmlTags + \
                      ' id="' + elemID + '"' + ' />'

        result += '</tr>\n'
        return result

    def getServicesHTMLPage(self, pathInfo, queryParams):
        result = getPageTemplate().replace("#PAGETITLE#", u"Webové služby RÚIAN")
        result = result.replace("<#SERVICES_URL>", "http://" + SERVER_HTTP + getPortSpecification() + "/" + SERVICES_WEB_PATH )

        result = result.replace("#HTMLDATA_URL#", configmodule.getHTMLDataURL())

        queryParams = self.normalizeQueryParams(queryParams)

        tabCaptions = ""
        tabDivs = ""

        i = 1
        tabIndex = 0
        for service in services:
            tabCaptions += '<li><a href="#tabs-' + str(i) + '">' + service.caption + '</a></li>\n'
            tabDivs += '<div id="tabs-' + str(i) + '">   <h2>' + service.shortDesc + '</h2>\n'
            tabDivs += service.htmlDesc
            tabDivs += u'<br><p class = "enhancedGUI">Adresa služby:' + service.pathName + '</p>\n'
            formName = "form_" + str(i)
            urlSpanName = formName + "_urlSpan"
            onChangeProcCode = 'onChangeProc(' + formName + "," + urlSpanName + ", '" + service.pathName + "')"
            displayResultProcCode = "displayResult('" + formName + "_textArea', '" + service.pathName + "')"
            if service.pathName == pathInfo:
                tabIndex = i

            tabDivs += u'<span name="' + urlSpanName + '" class = "enhancedGUI" id="' + urlSpanName + '" >' + "http://" + SERVER_HTTP + getPortSpecification() + "/" + SERVICES_WEB_PATH + "/" + service.pathName[1:] + "</span>\n" #service.getServicePath() + "</span>\n"
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
            #tabDivs += '<div class="ui-widget" style="margin: 0px 20px 20px 0px; padding: 10px 10px 15px 10px; border: solid grey 1px;">\n'
            tabDivs += '<div class="warning">\n'
            tabDivs += '<table id="' + formName + '_ParamsTable">\n'
            for param in service.restPathParams:
                tabDivs += self.tablePropertyRow(param, formName, u"REST", queryParams, onChangeProcCode)

            for param in service.queryParams:
                tabDivs += self.tablePropertyRow(param, formName, u"Query", queryParams, onChangeProcCode)

            tabDivs += '</table>\n'
            tabDivs += '</div>\n'

            tabDivs += '<br><input type="button" value="' + service.sendButtonCaption + '" onclick="' + onChangeProcCode + '; ' + displayResultProcCode + '">\n'
            tabDivs += '<input type="button" value="Nové zadání" onclick="clearInputs(\'' + formName + '\')">\n'
            tabDivs += '</form>\n'
            tabDivs += "</td><td>"
            tabDivs += '<textarea id=' + formName + '_textArea rows ="12" cols="50"></textarea>'
            tabDivs += "</td></tr></table>"

            tabDivs += "<a class = 'enhancedGUI' href='http://www.vugtk.cz/euradin/testing" + service.pathName + ".html'>Výsledky testů</a>"
            #tabDivs += "<a href='" + SERVER_HTTP + "/euradin/testing" + service.pathName + ".html'>show tests</a>"

            #url = "http://" + SERVER_HTTP + getPortSpecification() + "/" + configmodule.HTMLDATA_URL + service.pathName + '.png'
            url = configmodule.getHTMLDataURL() + service.pathName[1:] + ".png"
            tabDivs += '<p>\n<img class = "enhancedGUI" src="' + url + '"></p>\n'

            tabDivs += '</div>\n'
            i = i + 1

        if tabIndex == 0:
            newStr = ""
        else:
            newStr = '{ active: ' + str(tabIndex) + ' }'
        result = result.replace("#TABSOPTIONS#", newStr)

        result = result.replace("#CONSOLELINES#", console.consoleLines + "\n" + console.infoLines)
        result = result.replace("#ISSUELINES#", getIssueHTML() + "\n")
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
    import sys
    reload(sys)
    sys.setdefaultencoding('utf-8')
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