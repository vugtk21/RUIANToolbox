# -*- coding: utf-8 -*-

import addressbuilder

class TestParams:
    def __init__(self, address, returnValue, errMsg):
        self.address = address
        self.returnValue = returnValue
        self.errMsg = errMsg

dictionary = {
    "Patern1":TestParams(
        addressbuilder.Address(
            street=u"Arnošta Valenty",
            descNumber = u"670",
            recordNumber = u"",
            orientationNumber = u"31",
            ZIPCode = u"198 00",
            town = u"Praha",
            district = u"Černý most",
            districtNumber = u"9"
        ),
        u"Arnošta Valenty 670/31<br>Černý Most<br>19800 Praha 9",
        u"1.Adresní místo v Praze s ulicí, číslem popisným a orientačním"),
    "Patern2":TestParams(
        addressbuilder.Address(
            street=u"Arnošta Valenty",
            descNumber = u"670",
            recordNumber = u"",
            orientationNumber = u"",
            ZIPCode = u"198 00",
            town = u"praha",
            district = u"Černý most",
            districtNumber = u"9"
        ),
        u"Arnošta Valenty 670<br>Černý Most<br>19800 Praha 9",
        u"2.Adresní místo v Praze s ulicí a číslem popisným"),
    "Patern3":TestParams(
        addressbuilder.Address(
            street = u"Medová",
            descNumber = u"",
            recordNumber = u"30",
            orientationNumber = u"",
            ZIPCode = u"104 00",
            town = u"Praha",
            district = u"Křeslice",
            districtNumber = u"10"
        ),
        u"Medová č.ev. 30<br>Křeslice<br>10400 Praha 10",
        u"3.Adresní místo v Praze s ulicí a číslem evidenčním"),
    "Patern4":TestParams(
        addressbuilder.Address(
            street = u"",
            descNumber = u"",
            recordNumber = u"42",
            orientationNumber = u"",
            ZIPCode = u"104 00",
            town = u"Praha",
            district = u"Křeslice",
            districtNumber = u"10"
        ),
        u"Křeslice č.ev. 42<br>10400 Praha 10",
        u"4.Adresní místo v Praze s číslem evidenčním"),
    "Patern5":TestParams(
        addressbuilder.Address(
            street = u"Lhenická",
            descNumber = u"1120",
            recordNumber = u"",
            orientationNumber = u"1",
            ZIPCode = u"370 05",
            town = u"České Budějovice",
            district = u"České Budějovice 2",
            districtNumber = u""
        ),
        u"Lhenická 1120/1<br>České Budějovice 2<br>37005 České Budějovice",
        u"5. Adresní místo mimo Prahu s ulicí, číslem popisným a orientačním, název obce a její části nejsou shodné"),
    "Patern6":TestParams(
        addressbuilder.Address(
            street = u"Lhenická",
            descNumber = u"1120",
            recordNumber = u"",
            orientationNumber = u"",
            ZIPCode = u"370 05",
            town = u"České Budějovice",
            district = u"České Budějovice 2",
            districtNumber = u""
        ),
        u"Lhenická 1120<br>České Budějovice 2<br>37005 České Budějovice",
        u"6. Adresní místo mimo Prahu s ulicí, číslem popisným, název obce a její části nejsou shodné"),
    "Patern7":TestParams(
        addressbuilder.Address(
            street = u"Lhenická",
            descNumber = u"",
            recordNumber = u"12",
            orientationNumber = u"",
            ZIPCode = u"370 05",
            town = u"České Budějovice",
            district = u"České Budějovice 2",
            districtNumber = u""
        ),
        u"Lhenická č.ev. 12<br>České Budějovice 2<br>37005 České Budějovice",
        u"7. Adresní místo mimo Prahu s ulicí a číslem evidenčním, název obce a její části nejsou shodné"),
    "Patern8":TestParams(
        addressbuilder.Address(
            street = u"Žamberecká",
            descNumber = u"339",
            recordNumber = u"",
            orientationNumber = u"",
            ZIPCode = u"516 01",
            town = u"Vamberk",
            district = u"Vamberk",
            districtNumber = u""
        ),
        u"Žamberecká 339<br>51601 Vamberk",
        u"8. Adresní místo mimo Prahu s ulicí a číslem popisným, název obce a její části jsou shodné"),
    "Patern9":TestParams(
        addressbuilder.Address(
            street = u"Žamberecká",
            descNumber = u"339",
            recordNumber = u"",
            orientationNumber = u"1",
            ZIPCode = u"516 01",
            town = u"Vamberk",
            district = u"Vamberk",
            districtNumber = u""
        ),
        u"Žamberecká 339/1<br>51601 Vamberk",
        u"9. Adresní místo mimo Prahu s ulicí, číslem popisným a orientačním, název obce a její části jsou shodné"),
    "Patern10":TestParams(
        addressbuilder.Address(
            street = u"Žamberecká",
            descNumber = u"",
            recordNumber = u"21",
            orientationNumber = u"",
            ZIPCode = u"516 01",
            town = u"Vamberk",
            district = u"Vamberk",
            districtNumber = u""
        ),
        u"Žamberecká č.ev. 21<br>51601 Vamberk",
        u"10. Adresní místo mimo Prahu s ulicí a číslem evidenčním, název obce a její části jsou shodné"),
    "Patern11":TestParams(
        addressbuilder.Address(
            street = u"",
            descNumber = u"106",
            recordNumber = u"",
            orientationNumber = u"",
            ZIPCode = u"533 33",
            town = u"Pardubice",
            district = u"Dražkovice",
            districtNumber = u""
        ),
        u"Dražkovice 106<br>53333 Pardubice",
        u"11. Adresní místo mimo Prahu s číslem popisným, název obce a její části nejsou shodné"),
    "Patern12":TestParams(
        addressbuilder.Address(
            street = u"",
            descNumber = u"106",
            recordNumber = u"",
            orientationNumber = u"12",
            ZIPCode = u"533 33",
            town = u"Pardubice",
            district = u"Dražkovice",
            districtNumber = u""
        ),
        u"Dražkovice 106/12<br>53333 Pardubice",
        u"12. Adresní místo mimo Prahu s číslem popisným a orinetačním, název obce a její části nejsou shodné"),
    "Patern13":TestParams(
        addressbuilder.Address(
            street = u"",
            descNumber = u"",
            recordNumber = u"32",
            orientationNumber = u"",
            ZIPCode = u"533 33",
            town = u"Pardubice",
            district = u"Dražkovice",
            districtNumber = u""
        ),
        u"Dražkovice č.ev. 32<br>53333 Pardubice",
        u"13. Adresní místo mimo Prahu s číslem evidenčním, název obce a její části nejsou shodné"),
    "Patern14":TestParams(
        addressbuilder.Address(
            street = u"",
            descNumber = u"111",
            recordNumber = u"",
            orientationNumber = u"",
            ZIPCode = u"503 33",
            town = u"Praskačka",
            district = u"Praskačka",
            districtNumber = u""
        ),
        u"č.p. 111<br>50333 Praskačka",
        u"14. Adresní místo mimo Prahu s číslem popisným, název obce a její části jsou shodné"),
    "Patern15":TestParams(
        addressbuilder.Address(
            street = u"",
            descNumber = u"111",
            recordNumber = u"",
            orientationNumber = u"1",
            ZIPCode = u"503 33",
            town = u"Praskačka",
            district = u"Praskačka",
            districtNumber = u""
        ),
        u"č.p. 111/1<br>50333 Praskačka",
        u"15. Adresní místo mimo Prahu s číslem popisným a orientačním, název obce a její části jsou shodné"),
    "Patern16":TestParams(
        addressbuilder.Address(
            street = u"",
            descNumber = u"",
            recordNumber = u"32",
            orientationNumber = u"",
            ZIPCode = u"503 33",
            town = u"Praskačka",
            district = u"Praskačka",
            districtNumber = u""
        ),
        u"č.ev. 32<br>50333 Praskačka",
        u"16. Adresní místo mimo Prahu s číslem evidenčním, název obce a její části jsou shodné")
    }