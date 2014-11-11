# -*- coding: utf-8 -*-
__author__ = 'Augustyn'

import sharedtools
import urllib2
import urllib
import codecs

def buildParamString(street, houseNumber, recordNumber, orientationNumber, orientationNumberCharacter, zipCode, locality, localityPart, districtNumber):
    url = u"/CompileAddress?"
    params = {
        "Street"            : street,
        "HouseNumber"       : houseNumber,
        "RecordNumber"      : recordNumber,
        "OrientationNumber" : orientationNumber,
        "OrientationNumberCharacter" : orientationNumberCharacter,
        "ZIPCode"           : zipCode,
        "Locality"          : locality,
        "LocalityPart"      : localityPart,
        "DistrictNumber"    : districtNumber
    }

    for key in params:
        url += key + "=" + urllib.quote(codecs.encode(params[key], "utf-8")) + "&"

    return url

def test(testerParam = None):
    if testerParam == None:
        tester = sharedtools.FormalTester("Ověření funkčnosti služby CompileAddress")
    else:
        tester = testerParam
    tester.newSection("Ověření funkčnosti služby CompileAddress",
                """
Tento test ověřuje sestavení zápisu adresy ve standardizovaném tvaru podle § 6 vyhlášky č. 359/2011 Sb.,
kterou se provádí zákon č. 111/2009 Sb., o základních registrech, ve znění zákona č. 100/2010 Sb.
Adresní místo lze zadat buď pomocí jeho identifikátoru RÚIAN, textového řetězce adresy nebo jednotlivých prvků adresy.
                """,
                "Compiling person", "Tester")

    def addTest(street, houseNumber, recordNumber, orientationNumber, orientationNumberCharacter, zipCode, locality, localityPart, districtNumber, expectedValue):
        params = buildParamString(street, houseNumber, recordNumber, orientationNumber, orientationNumberCharacter, zipCode, locality, localityPart, districtNumber)
        try:
            result = urllib2.urlopen(sharedtools.SERVER_URL + params).read()
            result = "\n".join(result.splitlines())
        except Exception as inst:
            result = str(inst)
        #result = "aaa" #result.decode("utf-8")
        #expectedValue = "ev"
        params = params.decode("utf-8")
        #expectedValue = expectedValue.decode("utf-8")
        tester.addTest(params, result, expectedValue, "")

    def addTestByID(path, expectedValue):
        try:
            result = urllib2.urlopen(sharedtools.SERVER_URL + path).read()
        except Exception as inst:
            result = str(inst)
        #result = result.strip()
        result = "\n".join(result.splitlines())
        #result = urllib.quote(codecs.encode(result, "utf-8"))
        tester.addTest(path, result, expectedValue, "")

    def addTestFullText(testerParam = None):
        if testerParam == None:
            tester = sharedtools.FormalTester("Ověření funkčnosti služby FullTextSearch")
        else:
            tester = testerParam

    
    tester.loadAndAddTest("/CompileAddress/text/?", "SearchText=Mramor,%20Tet%C3%ADn", "Mramorová 234\n26601 Tetín\nMramorová 243\n26601 Tetín\nMramorová 236\n26601 Tetín")
    tester.loadAndAddTest("/CompileAddress/text/?", "SearchText=12", "")
        
    addTestByID("/CompileAddress/text?AddressPlaceId=41326474", u"U Kamene 181\n26716 Vysoký Újezd")    
    addTestByID("/CompileAddress/text?AddressPlaceId=21907145", u"Na lánech 598/13\nMichle\n14100 Praha 4")
    addTestByID("/CompileAddress/text?AddressPlaceId=25021478", u"Lesní 345/5\n35301 Mariánské Lázně")
    addTestByID("/CompileAddress/text?AddressPlaceId=16512171", u"Pašinovice 8\n37401 Komařice")
    addTestByID("/CompileAddress/text?AddressPlaceId=165k", u"") #ošetření chyby - zadání omylem znaku do identifikátoru
    addTestByID("/CompileAddress/text?AddressPlaceId=12", u"") #ošetření chyby - zadání identifikátoru, který není v DB

    addTest(u"Arnošta Valenty", u"670", u"", u"31", u"", u"19800", u"Praha", u"Černý Most", u"9", u"Arnošta Valenty 670/31\nČerný Most\n19800 Praha 9")
    addTest(u"Arnošta Valenty", u"670", u"", u"", u"", u"198 00", u"Praha", u"Černý Most", u"9", u"Arnošta Valenty 670\nČerný Most\n19800 Praha 9")
    addTest(u"Medová", u"", u"30", u"", u"", u"10400", u"Praha", u"Křeslice",  u"10", u"Medová č.ev. 30\nKřeslice\n10400 Praha 10")
    addTest(u"", u"", u"42", u"", u"", u"10400", u"Praha", u"Křeslice", u"10", u"Křeslice č.ev. 42\n10400 Praha 10")
    addTest(u"Lhenická", u"1120", u"", u"1", u"", u"37005", u"České Budějovice", u"České Budějovice 2", u"", u"Lhenická 1120/1\nČeské Budějovice 2\n37005 České Budějovice")
    addTest(u"Holická", u"568", u"", u"31", u"y", u"779 00", u"Olomouc", u"Hodolany", u"", u"Holická 568/31y\nHodolany\n77900 Olomouc")
    addTest(u"Na Herinkách", u"85", u"", u"", u"", u"26601", u"Beroun", u"Beroun-Závodí", u"", u"Na Herinkách 85\nBeroun-Závodí\n26601 Beroun")
    addTest(u"Na Herinkách", u"", u"97", u"", u"", u"26601", u"Beroun", u"Beroun-Závodí", u"", u"Na Herinkách č.ev. 97\nBeroun-Závodí\n26601 Beroun")
    addTest(u"Žamberecká", u"339", u"", u"", u"", u"51601", u"Vamberk", u"Vamberk", u"", u"Žamberecká 339\n51601 Vamberk")
    addTest(u"Žamberecká", u"339", u"", u"1", u"", u"51601", u"Vamberk", u"Vamberk", u"", u"Žamberecká 339/1\n51601 Vamberk")
    addTest(u"Lidická", u"2858", u"", u"49", u"F", u"78701", u"Šumperk", u"Šumperk", u"", u"Lidická 2858/49F\n78701 Šumperk")
    addTest(u"Žamberecká", u"", u"21", u"", u"", u"51601", u"Vamberk", u"Vamberk", u"", u"Žamberecká č.ev. 21\n51601 Vamberk")
    addTest(u"", u"106", u"", u"", u"", u"53333", u"Pardubice", u"Dražkovice", u"", u"Dražkovice 106\n53333 Pardubice")
    addTest(u"", u"", u'32', u'', u"", u"53333", u"Pardubice", u"Dražkovice", u"", u"Dražkovice č.ev. 32\n53333 Pardubice")
    addTest(u"", u"111", u"", u"", u"", u"50333", u"Praskačka", u"Praskačka", u"", u"č.p. 111\n50333 Praskačka")
    addTest(u"", u"", u"86", u"", u"", u"53943", u"Krouna", u"Krouna", u"", u"č.ev. 86\n53943 Krouna")
    tester.closeSection()

    if testerParam == None:
        tester.saveToHTML("CompileAddress.html")


if __name__ == '__main__':
    sharedtools.setupUTF()
    test()
