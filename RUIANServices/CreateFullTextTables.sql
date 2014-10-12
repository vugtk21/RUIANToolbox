-- ##################################################
-- This script creates full text search tables
-- ##################################################

drop table if exists address_points;
CREATE TABLE address_points
AS SELECT adresnimista.kod gid, obce.kod kod_obce, obce.nazev nazev_obce, ui_momc.nazev nazev_momc, ui_mop.nazev nazev_mop, castiobci.kod kod_casti_obce, castiobci.nazev nazev_casti_obce, ulice.nazev nazev_ulice, typ_st_objektu.zkratka typ_so, adresnimista.cislodomovni cislo_domovni, adresnimista.cisloorientacni cislo_orientacni, adresnimista.cisloorientacnipismeno znak_cisla_orientacniho, adresnimista.psc psc, -ST_X(adresnibod) latitude, -ST_Y(adresnibod) longitude, adresnimista.platiod plati_od, adresnimista.adresnibod the_geom
FROM adresnimista
LEFT OUTER JOIN ulice on (adresnimista.ulicekod=ulice.kod)
LEFT OUTER JOIN stavebniobjekty on (adresnimista.stavebniobjektkod=stavebniobjekty.kod )
LEFT OUTER JOIN castiobci on (stavebniobjekty.castobcekod=castiobci.kod)
LEFT OUTER JOIN obce on (castiobci.obeckod=obce.kod)
LEFT OUTER JOIN typ_st_objektu on (stavebniobjekty.typstavebnihoobjektukod=typ_st_objektu.kod)
LEFT OUTER JOIN ui_momc on (stavebniobjekty.momckod=ui_momc.kod)
LEFT OUTER JOIN ui_mop on (ui_momc.mop_kod=ui_mop.kod);

ALTER TABLE address_points ADD PRIMARY KEY (gid);

select UpdateGeometrySRID('public', 'address_points', 'the_geom', 5514);

-- --------------------------------------------------
-- Create temporary table fulltext_a and fill it with partial data
-- --------------------------------------------------
drop table if exists fulltext_a;
create table fulltext_a
as
select gid, concat(nazev_obce, ',', nazev_casti_obce, ',', nazev_ulice) searchstr
from address_points
where nazev_obce <> nazev_casti_obce;

-- --------------------------------------------------
-- add rest of values
-- --------------------------------------------------
insert into fulltext_a 
select gid, concat(nazev_obce, ',', nazev_ulice) searchstr
from address_points
where nazev_obce = nazev_casti_obce;

-- --------------------------------------------------
-- Create table fulltext
-- --------------------------------------------------
DROP TABLE IF EXISTS fulltext;
create table fulltext
as
SELECT searchstr, array_agg(gid) gids
FROM fulltext_a
GROUP BY searchstr;

-- --------------------------------------------------
-- Drop temporary table fulltext_a
-- --------------------------------------------------
drop table fulltext_a;

-- --------------------------------------------------
-- Create search function explode_array
-- --------------------------------------------------
create or replace function explode_array(in_array anyarray) returns setof anyelement as
$$
    select ($1)[s] from generate_series(1,array_upper($1, 1)) as s;
$$
language sql immutable;

-- --------------------------------------------------
-- Create table gids
-- --------------------------------------------------
drop table if exists gids;
create table gids
as
select gid from address_points
group by gid order by gid