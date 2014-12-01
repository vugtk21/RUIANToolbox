#!C:/Python27/python.exe
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        addresswebservices
# Purpose:
#
# Author:      Radek Augustýn
# Copyright:   (c) VUGTK, v.v.i. 2014
# License:     CC BY-SA 4.0
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

import RUIANConnection

SERVICES_PATH = '' # 'services'

def getPageTemplate():
    f = codecs.open("..//HTML//RestPageTemplate.htm", "r", "utf-8")
    result = f.read()
    f.close()

    # convert windows line breaks to linux, so firebug places breakpoint properly
    result = result.replace("\r\n", "\n")
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
    if configmodule.config.issueShortDescription == "":
        return ""
    else:
        result =  u'<div class="ui-widget">' \
                u'<div class="ui-state-error ui-corner-all" style="padding: 0 .7em;">' \
                u'<p><span class="ui-icon ui-icon-alert" style="float: left; margin-right: .3em;"></span>' \
                u'<strong>Návrh řešení ' + configmodule.config.issueNumber + u'</strong>'
        result += configmodule.config.issueShortDescription
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

        if param.name == 'FillAddressButton':
            result += '<td></td><td align="right">'
        else:
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

        elif param.name == 'FillAddressButton':
            result += '<input type="button" value="Doplň adresu" id="' + formName + '_FillAddressButton' + \
                      '" title="' + param.shortDesc + '"  onclick="findAddress(\'' + formName + '\')">'
            result += '<br><input type="checkbox" id="%s_SmartAutocompleteCB" checked>Chytré našeptávače</input>' % (formName)
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
        servicesURL = "http://" + SERVER_HTTP + getPortSpecification() + "/" + SERVICES_WEB_PATH
        result = result.replace("<#SERVICES_URL>", servicesURL)

        result = result.replace("#HTMLDATA_URL#", configmodule.getHTMLDataURL())
        result = result.replace("#VERSIONNUMBER#", configmodule.config.issueNumber)
        result = result.replace("#SERVICES_URL_PATH#", configmodule.getServicesPath())
        if configmodule.config.ruianVersionDate == "":
            configmodule.config.ruianVersionDate = RUIANConnection.getRUIANVersionDate()

        result = result.replace("#RUIANVERSIONDATE#", '<a href="%s/downloaded/Import.html">%s</a>' % (servicesURL, configmodule.config.ruianVersionDate))

        queryParams = self.normalizeQueryParams(queryParams)

        tabCaptions = ""
        tabDivs = ""

        i = 1
        tabIndex = 0
        for service in services:
            tabCaptions += '<li><a href="#tabs-' + str(i) + '">' + service.caption + '</a></li>\n'
            tabDivs += '<div id="tabs-' + str(i) + '">   <h2>' + service.shortDesc + '</h2>\n'
            tabDivs += service.htmlDesc
            tabDivs += u'<p class = "enhancedGUI">Adresa služby:' + service.pathName + '</p>\n'
            formName = "form_" + str(i)
            urlSpanName = formName + "_urlSpan"
            onChangeProcCode = 'onChangeProc(' + formName + "," + urlSpanName + ", '" + service.pathName + "')"
            displayResultProcCode = "runOrHookDisplayResult('" + formName + "', '" + service.pathName + "')"
            if service.pathName == pathInfo:
                tabIndex = i

            restPyURL = "http://" + SERVER_HTTP + getPortSpecification() + "/" + SERVICES_WEB_PATH + "/"
            tabDivs += u'<span name="' + urlSpanName + '" class = "enhancedGUI" id="' + urlSpanName + '" >' + "http://" + SERVER_HTTP + getPortSpecification() + "/" + SERVICES_WEB_PATH + "/" + service.pathName[1:] + "</span>\n" #service.getServicePath() + "</span>\n"
            if service.pathName == "/CompileAddress" or service.pathName == "/Geocode":
                tabDivs += u"""
                <br><br>
                <input type="radio" name= "radio%s" value="adresa"   id="%s_AddressRB" checked>Adresa</input>
                <input type="radio" name= "radio%s" value="vstup" id="%s_AddressItemsRB">Prvky adresy</input>
                <input type="radio" name= "radio%s" value="id"  id="%s_RuianIdRB">Identifikátor RÚIAN</input>
                """ % (service.pathName, formName, service.pathName, formName, service.pathName, formName)

            tabDivs += "<br><br>"
            tabDivs += "<table><tr valign=\"top\"><td>"
            tabDivs += '<form id="' + formName + '" name="' + formName + '" action="' + SERVICES_PATH + service.pathName + '" method="get" SearchForAddress="false">\n'

            # Parameters list
            tabDivs += '<div class="warning">\n'
            tabDivs += '<table id="' + formName + '_ParamsTable">\n'
            for param in service.restPathParams:
                tabDivs += self.tablePropertyRow(param, formName, u"REST", queryParams, onChangeProcCode)

            for param in service.queryParams:
                tabDivs += self.tablePropertyRow(param, formName, u"Query", queryParams, onChangeProcCode)

            tabDivs += '</table>\n'
            tabDivs += '</div>\n'

            tabDivs += '<br>'
            tabDivs += '<input style="float: right;" type="button" value="Nové zadání" onclick="clearInputs(\'' + formName + '\')">\n'
            tabDivs += '<input style="float: right;" type="button" value="%s" onclick="%s;%s">\n' % (service.sendButtonCaption, onChangeProcCode, displayResultProcCode)
            tabDivs += '</form>\n'
            tabDivs += "</td>"
            tabDivs += '<td><textarea id=' + formName + '_textArea rows ="12" cols="50"></textarea></td>'
            tabDivs += '<td><div class="resizeAbleDiv">' \
                       '<table class="resultsTable" id=' + formName + '_resultsTable>' \
                       '<tr><td>The resize property specifies whether or not an element is resizable by the user.</td></tr>' \
                       '<tr class="altColor"><td>The resize property specifies whether or not an element is resizable by the user.</td></tr>' \
                       '<tr><td>The resize property specifies whether or not an element is resizable by the user.</td></tr>' \
                       '<tr class="altColor"><td>The resize property specifies whether or not an element is resizable by the user.</td></tr>' \
                       '</table>' \
                       '</td>'
            tabDivs += "</tr></table>"

            tabDivs += "<a class = 'enhancedGUI' href='" + restPyURL + "testing" + service.pathName + ".html'>Výsledky testů</a>"
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