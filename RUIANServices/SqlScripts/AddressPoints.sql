-- ##################################################
-- This script creates full text search tables
-- ##################################################

drop table if exists address_points;
CREATE TABLE address_points
AS SELECT adresnimista.kod gid, obce.kod kod_obce, obce.nazev nazev_obce, momc.nazev nazev_momc, mop.nazev nazev_mop, castiobci.kod kod_casti_obce, castiobci.nazev nazev_casti_obce, ulice.nazev nazev_ulice, typ_st_objektu.zkratka typ_so, adresnimista.cislodomovni cislo_domovni, adresnimista.cisloorientacni cislo_orientacni, adresnimista.cisloorientacnipismeno znak_cisla_orientacniho, adresnimista.psc psc, -ST_X(adresnibod) latitude, -ST_Y(adresnibod) longitude, adresnimista.platiod plati_od, adresnimista.adresnibod the_geom
FROM adresnimista
LEFT OUTER JOIN ulice on (adresnimista.ulicekod=ulice.kod)
LEFT OUTER JOIN stavebniobjekty on (adresnimista.stavebniobjektkod=stavebniobjekty.kod )
LEFT OUTER JOIN castiobci on (stavebniobjekty.castobcekod=castiobci.kod)
LEFT OUTER JOIN obce on (castiobci.obeckod=obce.kod)
LEFT OUTER JOIN typ_st_objektu on (stavebniobjekty.typstavebnihoobjektukod=typ_st_objektu.kod)
LEFT OUTER JOIN momc on (stavebniobjekty.momckod=momc.kod)
LEFT OUTER JOIN mop on (momc.mopkod=mop.kod);

ALTER TABLE address_points ADD PRIMARY KEY (gid);

select UpdateGeometrySRID('public', 'address_points', 'the_geom', 5514);
