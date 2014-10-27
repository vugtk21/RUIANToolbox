# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        HTTPShared
# Purpose:
#
# Author:      Radek Augustýn
#
# Created:     13/11/2013
# Copyright:   (c) Radek Augustýn 2013
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import urllib

services = []

def getResultFormatParam():
    return RestParam("/Format", u"Formát", u"Formát výsledku služby (HTML, XML, Text, JSON)")

def getSearchTextParam():
    return URLParam("SearchText", u"Adresa", u"Textový řetězec adresy, jednotlivé položky oddělené čárkou", htmlTags = ' class="RUIAN_TEXTSEARCH_INPUT" ')

def getAddressPlaceIdParamRest():
    return RestParam("/AddressPlaceId", u"Identifikátor", u"Identifikátor adresního místa")

def getAddressPlaceIdParamURL():
    # gid = 19..72628626
    return URLParam("AddressPlaceId", u"Identifikátor", u"Identifikátor adresního místa, maximálně 8 číslic", "", True,
                    htmlTags = ' class="RUIAN_ID_INPUT" onkeypress="return isNumber(event, this, 8, 0)" ')#onpaste="return isNumber(event, this, 8, 0)"')

def getZIPCodeURL(disabled = True):
    # psc = 10000...79862
    return URLParam("ZIPCode",           u"PSČ", u"Poštovní směrovací číslo v rozsahu 100000 až 79862", "", disabled,
                    htmlTags = ' class="RUIAN_ZIP_INPUT" onkeypress="return isNumber(event, this, 5, 79862)" ')#onpaste="return isNumber(event, this, 5, 79862)"')

def getHouseNumberURL(disabled = True):
    # cislo_domovni (cislo popisne a cislo evidencni) = 1..9999
    return URLParam("HouseNumber",       u"Číslo popisné", "Číslo popisné v rozsahu 1 až 9999", "", disabled,
                    htmlTags = ' onkeypress="return isNumber(event, this, 4, 0)" ')#onpaste="return isNumber(event, this, 4, 0)"')

def getRecordNumberURL(disabled = True):
    # cislo_domovni (cislo popisne a cislo evidencni) = 1..9999
    return URLParam("RecordNumber",      u"Číslo evidenční", u"Číslo evidenční, pokud je přiděleno, v rozsahu 1 až 9999", "", disabled,
                    htmlTags = ' onkeypress="return isNumber(event, this, 4, 0)" ')#onpaste="return isNumber(event, this, 4, 0)"')

def getOrientationNumberURL(disabled = True):
    # cislo_orientacni = 1..999
    return URLParam("OrientationNumber", u"Číslo orientační", "Číslo orientační v rozsahu 1 až 999", "", disabled,
                    htmlTags = ' onkeypress="return isNumber(event, this, 3, 0)" ')#onpaste="return isNumber(event, this, 3, 0)"')

def getOrientationNumberCharacterURL(disabled = True):
    # Písmeno čísla orientačního a..z, A..Z
    return URLParam("OrientationNumberCharacter", u"Písmeno čísla<br>orientačního", "Písmeno čísla orientačního a..z, A..Z", "", disabled,
                    htmlTags = ' onkeypress="return isENLetter(event, this)" ')

def getDistrictNumberURL(disabled = True):
    # 1..10
    return URLParam("DistrictNumber", u"Číslo městského<br>obvodu v Praze", u"Číslo městského obvodu v Praze v rozsahu 1 až 10",
                    "", disabled, htmlTags = ' onkeypress="return isNumber(event, this, 2, 10)" ')#onpaste="return isNumber(event, this, 2, 10)"')

def getAddressPlaceIdParamURL_IdNotDisabled():
    return URLParam("AddressPlaceId", u"Identifikátor", u"Identifikátor adresního místa", "", False,  htmlTags = ' class="RUIAN_ID_INPUT" ')

class HTTPResponse():
    def __init__(self, handled, mimeFormat = "text/html", htmlData = ""):
        self.handled = handled
        self.mimeFormat = mimeFormat
        self.htmlData = htmlData

class URLParam:
    def __init__(self, name, caption, shortDesc, htmlDesc = "", disabled = False, htmlTags = ""):
        self.name  = name
        self.caption   = caption
        self.shortDesc = shortDesc
        self.htmlDesc  = htmlDesc
        self.disabled = disabled
        self.htmlTags = htmlTags

class RestParam(URLParam):
    def __init__(self, pathName, caption, shortDesc, htmlDesc = "", htmlTags = ""):
        URLParam.__init__(self, pathName, caption, shortDesc, htmlDesc, False, htmlTags)

    def getPathName(self):
        return self.name

    pathName = property(getPathName, "REST path name")

def getMimeFormat(self, formatText):
    a = self[formatText].lower()
    if a in ["html", "htmltoonerow"]:
        return "text/" + self[formatText].lower()
    elif a in ["xml", "json"]:
        return "application/" + self[formatText].lower()
    else: # Default value text
        return "text/plain"

def noneToString(item):
    if item is None:
        return ""
    else:
        return str(item)

class MimeBuilder:
    def __init__(self, formatText = "text"):
        self.formatText = formatText.lower()

        if self.formatText in ["xml", "json"]:
            self.lineSeparator = "\n"
        elif self.formatText == "html":
            self.lineSeparator = "<br>"
        elif self.formatText in ["htmltoonerow", "texttoonerow"]:
            self.lineSeparator = ", "
        else: # default value text
            self.lineSeparator = "\n"

        pass

    def getMimeFormat(self):
        if self.formatText in ["xml", "json"]:
            return "application/" + self.formatText
        elif self.formatText in ["html", "htmltoonerow"]:
            return "text/html"
        else: # Default value text
            return "text/plain"

    def listToXML(self, listOfLines, lineSeparator = "\n", tag = "FormattedOutput"):
        result = '<?xml version="1.0" encoding="UTF-8"?>' + lineSeparator + "<xml>" + lineSeparator
        for line in listOfLines:
            result += "<" + tag + ">" + lineSeparator + line + "</" + tag + ">" + lineSeparator
        return result + "</xml>"

    def listToJSON(self, listOfLines, lineSeparator = "\n", tag = "FormattedOutput"):
        result = "{"
        index = 0
        for item in listOfLines:
            index += 1
            if index > 1:
                result += ','
            if item == "True" or item == "False":
                addition1 = '\t"valid" : '
                addition2 = "\n"
            else:
                addition1 = ""
                addition2 = ""
            result += lineSeparator + '"' + tag + str(index) + '" : {' + lineSeparator + addition1 + item + addition2 + "\t}"
        result += lineSeparator + "}"
        return result

    def listToText(self, listOfLines, lineSeparator = "\n"):
        result = ""
        for line in listOfLines:
            result += line + lineSeparator
        return result[:-len(lineSeparator)]

    def listToHTML(self, listOfLines, lineSeparator = "<br>"):
        result = ""
        for line in listOfLines:
            if result != "":
                result += lineSeparator
            result += line
        return result

    def listToResponseText(self, ListOfLines, ignoreOneRow=False):
        if self.formatText == "xml":
            return self.listToXML(ListOfLines)
        elif self.formatText == "html" or self.formatText == "htmltoonerow":
            return self.listToHTML(ListOfLines)
        elif self.formatText == "json":
            return self.listToJSON(ListOfLines)
        else: # default value text
            return self.listToText(ListOfLines)

    def dictionaryToText(self, dictionary, withID, withAddress):
        response = dictionary["JTSKY"] + ", " + dictionary["JTSKX"]
        if withID:
            response = dictionary["id"] + ", " + response
        if withAddress:
            response += ", " + compileAddressToOneRow(dictionary["street"],dictionary["houseNumber"],dictionary["recordNumber"], dictionary["orientationNumber"], dictionary["orientationNumberCharacter"], dictionary["zipCode"], dictionary["locality"], dictionary["localityPart"], dictionary["districtNumber"])
        return response

    def dictionaryToXML(self, dict, withID, withAddress):
        response = "<record>\n"
        if withID:
            response += "\t<id>" + dict["id"] + "</id>\n"
        response += "\t<JTSKY>" + dict["JTSKY"] + "</JTSKY>\n"
        response += "\t<JTSKX>" + dict["JTSKX"] + "</JTSKX>\n"
        if withAddress:
            response += compileAddressAsXML(dict["street"], dict["houseNumber"], dict["recordNumber"], dict["orientationNumber"], dict["orientationNumberCharacter"],dict["zipCode"], dict["locality"], dict["localityPart"], dict["districtNumber"])
        response += "</record>\n"
        return response

    def dictionaryToJSON(self, dict, withID, withAddress):
        response = "\n\t{\n"
        if withID:
            response += '\t"id":' + dict["id"] + ",\n"
        response += '\t"JTSKY":' + dict["JTSKY"] + ",\n"
        response += '\t"JTSKX":' + dict["JTSKX"]
        if withAddress:
            response += ",\n" + compileAddressAsJSON(dict["street"], dict["houseNumber"], dict["recordNumber"], dict["orientationNumber"], dict["orientationNumberCharacter"],dict["zipCode"], dict["locality"], dict["localityPart"], dict["districtNumber"])
        else:
            response += "\n"
        response += "\t}"
        return response

    def listOfDictionariesToResponseText(self, listOfDictionaries, withID, withAddress):
        response = ""
        if self.formatText == "xml":
            head = '<?xml version="1.0" encoding="UTF-8"?>\n<xml>\n'
            body = ""
            tail = "</xml>"
            for dict in listOfDictionaries:
                body += self.dictionaryToXML(dict, withID, withAddress)
            return head + body + tail
        elif self.formatText == "json":
            head = '{\n"records": ['
            body = ""
            tail = "\n]}"
            first = True
            for dict in listOfDictionaries:
                if first:
                    first = False
                else:
                    body += ","
                body += self.dictionaryToJSON(dict, withID, withAddress)
            return head + body + tail
        else:
            for dict in listOfDictionaries:
                response += self.dictionaryToText(dict, withID, withAddress) + self.lineSeparator
            response = response[:-len(self.lineSeparator)]
        return response

    def coordinatesToXML(self, listOfCoordinates, lineSeparator = "\n", tag = "Coordinates"):
        result = '<?xml version="1.0" encoding="UTF-8"?>' + lineSeparator + "<xml>" + lineSeparator
        index = 0
        for coordinates in listOfCoordinates:
            index = index + 1
            result += "<" + tag + str(index) + ">" + lineSeparator + "<Y>" + coordinates.JTSKY + "</Y>" + lineSeparator + "<X>" + coordinates.JTSKX + "</X>" + lineSeparator + "</" + tag + str(index) + ">" + lineSeparator
        result += "</xml>"
        return result

    def coordinatesToHTML(self, listOfCoordinates, lineSeparator = "<br>"):
        result = ""
        for line in listOfCoordinates:
            if result != "":
                result += lineSeparator
            result += line.JTSKY + ", " + line.JTSKX
        return result

    def coordinatesToJSON(self, listOfCoordinates, lineSeparator = "\n", tag = "Coordinates"):
        result = "{"
        index = 0
        for line in listOfCoordinates:
            index += 1
            if index > 1:
                result += ','
            result += lineSeparator + '"' + tag + str(index) + '" : {' + lineSeparator + ' \t"Y": "' + line.JTSKY + '",' + lineSeparator + '\t"X": "' + line.JTSKX + '"' + lineSeparator + "\t}"
        result += lineSeparator + "}"
        return result

    def coordinatesToText(self, listOfCoordinates, lineSeparator = "\n"):
        result = ""
        for line in listOfCoordinates:
            result += line.JTSKX + ", " + line.JTSKY + lineSeparator
        return result[:-1]

    def coordintesToResponseText(self, listOfCoordinates):
        if self.formatText == "xml":
            return self.coordinatesToXML(listOfCoordinates)
        elif self.formatText == "html":
            return self.coordinatesToHTML(listOfCoordinates)
        elif self.formatText == "htmltoonerow":
            return self.coordinatesToHTML(listOfCoordinates, "; ")
        elif self.formatText == "json":
            return self.coordinatesToJSON(listOfCoordinates)
        elif self.formatText == "texttoonerow":
            return self.coordinatesToText(listOfCoordinates, "; ")
        else: # default value text
            return self.coordinatesToText(listOfCoordinates)

    def addressesToXML(self, listOfAddresses, lineSeparator = "\n", tag = "Adresa"):
        result = '<?xml version="1.0" encoding="UTF-8"?>' + lineSeparator + "<xml>" + lineSeparator
        index = 0
        for line in listOfAddresses:
            orientationNumber = noneToString(line[6])
            sign = noneToString(line[4])
            if orientationNumber != "":
                houseNumbers = "\t<" + sign +">" + noneToString(line[5]) + "</" + sign +">" + lineSeparator + "\t<orientacni_cislo>" + orientationNumber + noneToString(line[7]) + "</orientacni_cislo>"
            else:
                houseNumbers = "\t<" + sign +">" + noneToString(line[5]) + "</" + sign +">"

            index = index + 1
            street = noneToString(line[3])

            if street != "":
                street = "\t<ulice>" + street + "</ulice>" + lineSeparator

            town = noneToString(line[1])
            district = noneToString(line[2])

            if town == district or district == "":
                townDistrict = "\t<obec>" + town + "</obec>"
            else:
                townDistrict = "\t<obec>" + town + "</obec>" + lineSeparator + "\t<cast_obce>" + district + "</cast_obce>"

            result += "<" + tag + str(index) + ">" + lineSeparator + "<ID>" + noneToString(line[0]) + "</ID>" + lineSeparator + townDistrict + lineSeparator + street + houseNumbers + lineSeparator + "\t<PSČ>" + noneToString(line[8]) + "</PSČ>" + lineSeparator + "</" + tag + str(index) + ">" + lineSeparator
        result += "</xml>"
        return result

    def addressesToJSON(self, listOfAddresses, lineSeparator = "\n", tag = "Adresa"):
        result = "{"
        index = 0
        for line in listOfAddresses:
            index += 1
            if index > 1:
                result += ','

            orientationNumber = noneToString(line[6])
            sign = noneToString(line[4])
            if orientationNumber != "":
                houseNumbers = '\t"' + sign +'": ' + noneToString(line[5]) + ',' + lineSeparator + '\t"orientační_číslo":' + orientationNumber + noneToString(line[7]) + ','
            else:
                houseNumbers ='\t"' + sign +'": ' + noneToString(line[5]) + ','

            street = noneToString(line[3])

            if street != "":
                street = '\t"ulice": ' + street + "," + lineSeparator

            town = noneToString(line[1])
            district = noneToString(line[2])

            if town == district or district == "":
                townDistrict = '\t"obec" : ' + town + ","
            else:
                townDistrict = '\t"obec" : ' + town + "," + lineSeparator + '\t"část_obce": ' + district + ","


            result += lineSeparator + '"' + tag + str(index) + '" : {' + lineSeparator + '\t"ID": ' + noneToString(line[0])+ lineSeparator + townDistrict + lineSeparator + street + houseNumbers + lineSeparator + '\t"PSČ" :' + noneToString(line[8]) + lineSeparator + "\t}"
        result += lineSeparator + "}"
        return result

    def addressesToText(self, listOfAddresses, lineSeparator = "\n"):
        result = ""
        for line in listOfAddresses:
            orientationNumber = noneToString(line[6])
            if orientationNumber != "":
                houseNumbers = noneToString(line[5]) + "/" + orientationNumber + noneToString(line[7])
            else:
                houseNumbers = noneToString(line[5])
            street = noneToString(line[3])
            if street != "":
                street += " "
            town = noneToString(line[1])
            district = noneToString(line[2])
            if town == district:
                townDistrict = town
            else:
                townDistrict = town + "-" + district
            result += noneToString(line[0]) + " " + street + noneToString(line[4]) + " " + houseNumbers + ", " + townDistrict + ", " + noneToString(line[8]) + lineSeparator
        return result

    def addressesToResponseText(self, listOfAddresses):
        if self.formatText == "xml":
            return self.addressesToXML(listOfAddresses)
        elif self.formatText == "html" or self.formatText == "htmltoonerow":
            return self.addressesToText(listOfAddresses, "<br>")
        elif self.formatText == "json":
            return self.addressesToJSON(listOfAddresses)
        else: # default value text
            return self.addressesToText(listOfAddresses)


class WebService:
    """ Webova sluzba
    """
    def __init__(self, pathName, caption, shortDesc, htmlDesc = "", restPathParams = [], queryParams = [],
                 processHandler = None, sendButtonCaption = u"Odeslat", htmlInputTemplate = ""):
        ''' Webova sluzba '''
        self.pathName  = pathName
        self.caption   = caption
        self.shortDesc = shortDesc
        self.htmlDesc  = htmlDesc
        self.restPathParams = restPathParams
        self.queryParams = queryParams
        self.processHandler = processHandler
        self.sendButtonCaption = sendButtonCaption
        self.htmlInputTemplate = htmlInputTemplate # Šablona elementu HTML, implicitně INPUT
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
        result = "/REST" + self.pathName
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

def p(queryParams, name, defValue = ""):
    if queryParams.has_key(name):
        a = urllib.unquote(queryParams[name])
        return urllib.unquote(queryParams[name])
    else:
        return defValue

def numberCheck(possibleNumber):
    if possibleNumber != None and possibleNumber.isdigit():
        return possibleNumber
    else:
        return ""

def alphaCheck(possibleAlpha):
    if possibleAlpha != None and possibleAlpha.isalpha():
        return possibleAlpha
    else:
        return ""

def rightAddress(street, houseNumber, recordNumber, orientationNumber, orientationNumberCharacter, zipCode, locality, localityPart, districtNumber):
    psc = zipCode.replace(" ", "")
    if houseNumber != "" and not houseNumber.isdigit():
        return False
    if orientationNumber != "" and not orientationNumber.isdigit():
        return False
    if recordNumber != "" and not recordNumber.isdigit():
        return False
    if orientationNumberCharacter != "" and not orientationNumberCharacter.isalpha():
        return False
    if psc != "" and not psc.isdigit():
        return False
    if districtNumber != "" and not districtNumber.isdigit():
        return False
    if street == "" and houseNumber == "" and recordNumber == "" and orientationNumber == "" and orientationNumberCharacter == "" and psc == "" and locality == "" and localityPart == "" and districtNumber == "":
        return False
    return True

def formatZIPCode(code):
    if code == None:
        return ""
    else:
        code = code.replace(" ", "")
        if code.isdigit():
            return code
        else:
            return ""

def compileAddressAsJSON(street, houseNumber, recordNumber, orientationNumber, orientationNumberCharacter, zipCode, locality, localityPart, districtNumber):
    if houseNumber != "":
        sign = u"č.p."
        addressNumber = houseNumber
    else:
        sign = u"č.ev."
        addressNumber = recordNumber

    if orientationNumber != "":
        houseNumberStr = '\t"' + sign +'": ' + addressNumber + ',\n\t"orientační_číslo": ' + orientationNumber + orientationNumberCharacter + ','
    else:
        houseNumberStr ='\t"' + sign +'": ' + addressNumber + ','

    if street != "":
        street = '\t"ulice": ' + street + ",\n"

    if districtNumber != "":
        districtNumberStr = ',\n\t"číslo_městského_obvodu": ' + districtNumber
    else:
        districtNumberStr = ""

    if locality == localityPart or localityPart == "":
        townDistrict = '\t"obec": ' + locality + districtNumberStr
    else:
        townDistrict = '\t"obec": ' + locality + districtNumberStr + ',\n\t"část_obce": ' + localityPart

    result = street + houseNumberStr + '\n\t"PSČ" :' + zipCode + ",\n" + townDistrict + "\n"
    return result

def compileAddressAsXML(street, houseNumber, recordNumber, orientationNumber, orientationNumberCharacter, zipCode, locality, localityPart, districtNumber):
    if houseNumber != "":
        sign = "c.p."
        addressNumber = houseNumber
    else:
        sign = "c.ev."
        addressNumber = recordNumber

    if orientationNumber != "":
        houseNumberStr = '\t<' + sign +'>' + addressNumber + '</' + sign +'>\n\t<orientacni_cislo>' + orientationNumber + orientationNumberCharacter + '</orientacni_cislo>'
    else:
        houseNumberStr ='\t<' + sign +'>' + addressNumber + '</' + sign +'>'

    if street != "":
        street = '\t<ulice>' + street + "</ulice>\n"

    if districtNumber != "":
        districtNumberStr = '\n\t<cislo_mestskeho_obvodu>' + districtNumber + '</cislo_mestskeho_obvodu>'
    else:
        districtNumberStr = ""

    if locality == localityPart or localityPart == "":
        townDistrict = '\t<obec>' + locality + "</obec>" + districtNumberStr
    else:
        townDistrict = '\t<obec>' + locality + '</obec>' + districtNumberStr + '\n\t<cast_obce>' + localityPart + '</cast_obce>'

    result = street + houseNumberStr + '\n\t<PSC>' + zipCode + "</PSC>\n" + townDistrict + "\n"
    return result

def compileAddressToOneRow(street, houseNumber, recordNumber, orientationNumber, orientationNumberCharacter, zipCode, locality, localityPart, districtNumber):
    addressStr = ""
    zipCode = formatZIPCode(zipCode)
    houseNumber = numberCheck(houseNumber)
    orientationNumber = numberCheck(orientationNumber)
    districtNumber = numberCheck(districtNumber)
    orientationNumberCharacter = alphaCheck(orientationNumberCharacter)

    townInfo = zipCode + " " + locality#unicode(locality, "utf-8")
    if districtNumber != "":
        townInfo += " " + districtNumber

    if houseNumber != "":
        houseNumberStr = " " + houseNumber
        if orientationNumber != "":
            houseNumberStr += u"/" + orientationNumber + orientationNumberCharacter
    elif recordNumber != "":
        houseNumberStr = u" č.ev. " + recordNumber
    else:
        houseNumberStr = ""

    if locality.upper() == "PRAHA":
        if strIsNotEmpty(street):
            addressStr += street + houseNumberStr + ", " + localityPart + ", " + townInfo
        else:
            addressStr += localityPart + houseNumberStr + ", " + townInfo
    else:
        if strIsNotEmpty(street):
            addressStr += street + houseNumberStr + ", "
            if localityPart != locality:
                addressStr += localityPart + ", "
            addressStr += townInfo
        else:
            if localityPart != locality:
                addressStr += localityPart + houseNumberStr + ", "
            else:
                if houseNumber != "":
                    addressStr += u"č.p."+houseNumberStr + ", "
                else:
                    addressStr += houseNumberStr[1:] + ", "
            addressStr += townInfo
    return addressStr

def strIsNotEmpty(v):
    return v != None and v != ""

def compileAddressAsText(street, houseNumber, recordNumber, orientationNumber, orientationNumberCharacter, zipCode, locality, localityPart, districtNumber):
    lines = []
    zipCode = formatZIPCode(zipCode)
    houseNumber = numberCheck(houseNumber)
    orientationNumber = numberCheck(orientationNumber)
    districtNumber = numberCheck(districtNumber)
    orientationNumberCharacter = alphaCheck(orientationNumberCharacter)

    townInfo = zipCode + " " + locality#unicode(locality, "utf-8")
    if districtNumber != "":
        townInfo += " " + districtNumber

    if houseNumber != "":
        houseNumberStr = " " + houseNumber
        if orientationNumber != "":
            houseNumberStr += u"/" + orientationNumber + orientationNumberCharacter
    elif recordNumber != "":
        houseNumberStr = u" č.ev. " + recordNumber
    else:
        houseNumberStr = ""

    if locality.upper() == "PRAHA":
        if street != "":
            lines.append(street + houseNumberStr)#(unicode(street, "utf-8") + houseNumberStr)
            lines.append(localityPart)#(unicode(localityPart, "utf-8"))
            lines.append(townInfo)
        else:
            lines.append(localityPart + houseNumberStr)#(unicode(localityPart, "utf-8") + houseNumberStr)
            lines.append(townInfo)
    else:
        if street != "":
            lines.append(street + houseNumberStr)#(unicode(street, "utf-8") + houseNumberStr)
            if localityPart != locality:
                lines.append(localityPart)#(unicode(localityPart, "utf-8"))
            lines.append(townInfo)
        else:
            if localityPart != locality:
                lines.append(localityPart + houseNumberStr)#(unicode(localityPart, "utf-8") + houseNumberStr)
            else:
                if houseNumber != "":
                    lines.append(u"č.p."+houseNumberStr)
                else:
                    lines.append(houseNumberStr[1:])
            lines.append(townInfo)
    return lines

def numberToString(number):
    if number is None:
        return ""
    else:
        return str(number)

def extractDictrictNumber(nazev_mop):
    # Praha 10 -> 10
    if (nazev_mop != "") and (nazev_mop != None) and (nazev_mop.find(" ") >= 0):
        return nazev_mop.split(" ")[1]
    else:
        return ""

def analyseRow(typ_so, cislo_domovni):
    if typ_so[-3:] == ".p.":
        houseNumber = numberToString(cislo_domovni)
        recordNumber = ""
    elif typ_so[-3:] == "ev.":
        houseNumber = ""
        recordNumber = numberToString(cislo_domovni)
    else:
        pass

    return houseNumber, recordNumber

def itemToStr(item):
    if item == None:
        return ""
    else:
        return str(item)