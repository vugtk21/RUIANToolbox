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
import os.path

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

USE_DATA_LISTS = True
SERVICES_PATH = '' # 'services'

def getAddressTabName(itemName):
    ADDRESSTABNAMES = {
        "vstup" : ["FillAddressButton", "Locality", "LocalityPart", "DistrictNumber", "Street", "HouseNumber", "RecordNumber", "OrientationNumber", "OrientationNumberCharacter", "ZIPCode"],
        "id" : ["AddressPlaceId"],
        "adresa" : ["SearchText"]
    }
    for key in ADDRESSTABNAMES:
        if itemName in ADDRESSTABNAMES[key]:
            return key
    return ""

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

def getNoAddressAvailableHTML(formName):
    result =  u"""
<div class="ui-widget NOADDRESSHINTDIV" id="#FORMNAME#_NoAddressHintDiv" isvisible="false" tabname="vstup">
    <div class="ui-state-error ui-corner-all" style="padding: 0 .7em;">
        <p>
            <span class="ui-icon ui-icon-alert" style="float: left; margin-right: .3em;"></span>
            Adresa v této kombinaci prvků nebyla nenalezena
        </p>
    </div>
</div>"""
    result = result.replace("#FORMNAME#", formName)
    return result

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
    def __init__(self):
        self.dataListHTML = ""

    def normalizeQueryParams(self, queryParams):
        """ Parametry odesílané v URL requestu do query z HTML fomulářů musí být použity bez jména formuláře,
        tj. 'form_2_/AddressPlaceId' se spráně jmenuje 'AddressPlaceId'.
        """
        result = {}
        for key in queryParams:
            result[key[key.find("/") + 1:]] = queryParams[key]
        return result

    def tablePropertyRow(self, param, formName, paramTypeStr, queryParams, onChangeProcCode, hasAddressTabs):
        keyName = param.name[1:]
        if queryParams.has_key(keyName):
            valueStr = 'value = "' + queryParams[keyName] + '"'
        else:
            valueStr = ""

        if param.disabled:
            visibilityStr = ' style="display:none" '
        else:
            visibilityStr = ''

        if hasAddressTabs:
            tagsStr = ' isvisible="true" '
            tabName = getAddressTabName(param.name)
            if tabName:
                tagsStr += ' tabname="%s" ' % (tabName)
        else:
            tagsStr = ''

        result = '<tr id="%s_row_%s"%s%s>' % (formName, param.name, visibilityStr, tagsStr)

        if param.name == 'FillAddressButton':
            result += '<td align="right" colspan = "2">'
        else:
            result += '<td align="right">' + param.caption + ' </td><td>'

        if param.name == '/Format':
            buildRotatingCircle = False
            selectHTML = '<select input name="' + formName + '_' + param.name + '" title="' + param.shortDesc + '" onchange="updateServiceSpan(\'%s\')' % formName + '">' + \
                            '<option value="text">text</option>' + \
                            '<option value="textToOneRow">text do řádku</option>' + \
                            '<option value="xml">xml</option>' + \
                            '<option value="html">html</option>' + \
                            '<option value="htmlToOneRow">html do řádku</option>' + \
                            '<option value="json">json</option>' + \
                    '</select>'
            if buildRotatingCircle:
                result += '<span>%s</span><span id="%s_WaitCursorSpan" class="WAITCURSORSPAN" style="width:100%%;text-align:right;"><img src="http://jqueryui.com/resources/demos/autocomplete/images/ui-anim_basic_16x16.gif" /></span>' % (selectHTML, formName)
            else:
                result += selectHTML
        elif param.name == "DistrictNumber":
            idValue = "%s_%s" % (formName, param.name)
            result += '<select id="%s" name="%s" title="%s" onchange="districtNumberChanged(\'%s\')">' % (idValue, idValue, param.shortDesc, formName)+ \
                            '<option value=""></option>' + \
                            '<option value="1">Praha 1</option>' + \
                            '<option value="2">Praha 2</option>' + \
                            '<option value="3">Praha 3</option>' + \
                            '<option value="4">Praha 4</option>' + \
                            '<option value="5">Praha 5</option>' + \
                            '<option value="6">Praha 6</option>' + \
                            '<option value="7">Praha 7</option>' + \
                            '<option value="8">Praha 8</option>' + \
                            '<option value="9">Praha 9</option>' + \
                            '<option value="10">Praha 10</option>' + \
                    '</select>'
        elif param.name == 'ExtraInformation':
            if formName == "form_1":
                addressOption = '<option value="address">přidat adresu</option>'
            elif formName == "form_5":
                addressOption = '<option value="distance">přidat vzdálenost</option>'
            else:
                addressOption = ""

            result += '<select name="%s_%s" title="%s" onchange="updateServiceSpan(\'%s\')" >' % (formName, param.name, param.shortDesc, formName) + \
                            '<option value="standard">žádné</option>' + \
                            '<option value="id">přidat ID</option>' + addressOption + \
                    '</select>'

        elif param.name == 'FillAddressButton':
            result += '<span class="SMARTAUTOCOMPLETECB"><input type="checkbox" id="%s_SmartAutocompleteCB" checked onchange="setupInputs(\'%s\')" title="Našeptávače budou reagovat na již vložené hodnoty">Chytré našeptávače</span>' % (formName, formName)
            result += '&nbsp;&nbsp;<input type="button" value="Doplň adresu" id="' + formName + '_FillAddressButton' + \
                      '" title="' + param.shortDesc + '"  onclick="findAddress(\'' + formName + '\')">'
        else:
            if False: #param.disabled:
                disabledStr = ' disabled="disabled" '
            else:
                disabledStr = ''

            elemID = formName + '_' + param.name

            if param.name == 'LocalityPart':
                onChangeProcCode = onChangeProcCode.replace("onChangeProc(", "localityPartChanged(")

            dataListRef = ""
            if USE_DATA_LISTS and param.name in ["HouseNumber", "OrientationNumber", "RecordNumber", "OrientationNumberCharacter", "LocalityPart"]:
                dataListID = "%s_%s_DataList" % (formName, param.name)
                if param.name == 'LocalityPart':
                    dataListChangeProcCode = ' onchange="%s"' % onChangeProcCode
                    dataListChangeProcCode = ' onchange="alert(\'ahoj\')"'
                else:
                    dataListChangeProcCode = ""

                self.dataListHTML += '<datalist id="%s" class="DATALIST_CLASS" %s>\n</datalist>\n' % (dataListID, dataListChangeProcCode)
                dataListRef = ' list="%s"' % dataListID


            result += '<input name="' + elemID + '" ' + valueStr.decode('utf8') + 'title="' + \
                  param.shortDesc + '" onchange="' + onChangeProcCode + '" ' + disabledStr + param.htmlTags + \
                      ' id="' + elemID + '"' + dataListRef + ' />'

        result += '</tr>\n'

        return result

    def getServicesHTMLPage(self, scriptName, pathInfo, queryParams):
        scriptName = os.path.basename(scriptName)
        self.dataListHTML = ""
        result = getPageTemplate().replace("#PAGETITLE#", u"Webové služby RÚIAN")
        servicesURL = "http://" + SERVER_HTTP + getPortSpecification() + "/" + SERVICES_WEB_PATH
        result = result.replace("<#SERVICES_URL>", servicesURL)

        result = result.replace("#HTMLDATA_URL#", configmodule.getHTMLDataURL())
        result = result.replace("#VERSIONNUMBER#", configmodule.config.issueNumber)
        result = result.replace("#SERVICES_URL_PATH#", configmodule.getServicesPath())

        if configmodule.config.ruianVersionDate == "":
            versionDate = RUIANConnection.getRUIANVersionDate()
            configmodule.config.databaseIsOK = not versionDate.upper().startswith("ERROR:")
            if versionDate.upper().startswith("ERROR:"):
                versionDate = u"Nepřipojeno"
                ruianVersionCode = u"<b>!!! Data RÚIAN nejsou připojena !!!</b>"
                console.addMsg(u"Data RÚIAN nejsou připojena, obraťte se na správce webového serveru.")
            else:
                ruianVersionCode = '<a href="%s/downloaded/Import.html">%s</a>' % (servicesURL, versionDate)

            configmodule.config.ruianVersionDate = versionDate
            configmodule.config.ruianVersionCode = ruianVersionCode

        result = result.replace("#RUIANVERSIONDATE#", configmodule.config.ruianVersionCode)

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
            onChangeProcCode = 'onChangeProc(' + formName + ', true)'
            displayResultProcCode = "runOrHookDisplayResult('" + formName + "', '" + service.pathName + "')"
            if service.pathName == pathInfo:
                tabIndex = i

            restPyURL = "http://" + SERVER_HTTP + getPortSpecification() + "/" + SERVICES_WEB_PATH + "/"
            tabDivs += u'<span name="' + urlSpanName + '" class = "enhancedGUI" id="' + urlSpanName + '" >' + "http://" + SERVER_HTTP + getPortSpecification() + "/" + SERVICES_WEB_PATH + "/" + service.pathName[1:] + "</span>\n" #service.getServicePath() + "</span>\n"
            hasAddressTabs = service.pathName == "/CompileAddress" or service.pathName == "/Geocode"
            if hasAddressTabs:
                updateServiceSpanCode = ' onclick="updateServiceSpan(\'%s\')"' % formName
                tabDivs += u"""
                <br><br>
                <input type="radio" name= "radio%s" value="adresa"   id="%s_AddressRB" checked %s>Adresa
                <input type="radio" name= "radio%s" value="vstup" id="%s_AddressItemsRB" %s>Prvky adresy
                <input type="radio" name= "radio%s" value="id"  id="%s_RuianIdRB" %s>Identifikátor RÚIAN
                """ % (service.pathName, formName, updateServiceSpanCode, service.pathName, formName, updateServiceSpanCode, service.pathName, formName, updateServiceSpanCode)

            tabDivs += "<br><br>"
            tabDivs += "<table><tr valign=\"top\"><td>"
            tabDivs += '<form id="' + formName + '" name="' + formName + '" action="' + SERVICES_PATH + service.pathName + '" method="get" SearchForAddress="false">\n'

            # Parameters list
            tabDivs += '<div class="warning">\n'
            tabDivs += '<table id="' + formName + '_ParamsTable">\n'
            for param in service.restPathParams:
                tabDivs += self.tablePropertyRow(param, formName, u"REST", queryParams, onChangeProcCode, hasAddressTabs)

            for param in service.queryParams:
                tabDivs += self.tablePropertyRow(param, formName, u"Query", queryParams, onChangeProcCode, hasAddressTabs)

            tabDivs += '</table>\n'
            tabDivs += '</div>\n'

            tabDivs += '<br>'
            tabDivs += '<input style="float: right;" type="button" value="Nové zadání" onclick="clearInputs(\'%s\')">\n' % formName
            tabDivs += '<input style="float: right;" type="button" value="%s" onclick="%s">\n' % (service.sendButtonCaption, displayResultProcCode)
            tabDivs += '</form>\n'
            tabDivs += "</td>"
            tabDivs += '<td>'
            tabDivs += '<div id="%s_addressesDiv" class="AddressesDiv" title="Vyber adresu" isvisible="false" tabname="vstup"></div>' % formName

            tabDivs += getNoAddressAvailableHTML(formName)
            tabDivs += '<div id="%s_addressDiv" class="AddressDiv" isvisible="false" tabname="vstup"></div>' % formName
            tabDivs += '<textarea id=' + formName + '_textArea rows ="12" cols="50" class="RESULTTEXTAREA"></textarea></td>'
            tabDivs += "</tr></table>"

            tabDivs += "<a class = 'enhancedGUI' href='" + restPyURL + "testing" + service.pathName + ".html'>Výsledky testů</a>"
            url = configmodule.getHTMLDataURL() + service.pathName[1:] + ".png"
            tabDivs += '<p>\n<center><img width="80%" class="enhancedGUI" src="' + url + '"></center></p>\n'

            tabDivs += '</div>\n'
            i = i + 1

        if configmodule.config.databaseIsOK:
            separateStr = ""
            inStr = ""
        else:
            separateStr = "{ disabled: [1, 2, 3, 4, 5, 6] }"
            inStr = ", disabled: [1, 2, 3, 4, 5, 6]"

        if tabIndex == 0:
            newStr = separateStr
        else:
            newStr = '{ active: %s %s }' % (str(tabIndex), inStr)

        result = result.replace("#TABSOPTIONS#", newStr)

        result = result.replace("#CONSOLELINES#", console.consoleLines + "\n" + console.infoLines)
        result = result.replace("#ISSUELINES#", getIssueHTML() + "\n")
        result = result.replace("<#TABCAPTIONS#/>", tabCaptions)
        result = result.replace("<#TABCAPTIONS#/>", tabCaptions)
        result = result.replace("<#TABDIVS#/>", tabDivs)
        result = result.replace("#USE_DATA_LISTS#", str(USE_DATA_LISTS).lower())
        result = result.replace("#SCRIPT_NAME#", scriptName)
        result = result.replace("#DISABLEGUISWITCH#", str(configmodule.config.disableGUISwitch).lower())


        result = result.replace("</body>", self.dataListHTML + "</body>")

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
    pageContent = pageBuilder.getServicesHTMLPage(__file__, "", {})

    # Write result into file
    file = codecs.open("..//html//WebServices.html", "w", "utf-8")
    file.write(pageContent)
    file.close()

    pass

if __name__ == '__main__':
    main()