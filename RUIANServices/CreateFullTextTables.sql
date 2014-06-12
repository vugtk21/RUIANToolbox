# Create full text tables

create table fulltext_a
as
select gid, concat(nazev_obce, ',', nazev_casti_obce, ',', nazev_ulice) fulltext
from address_points
where nazev_obce <> nazev_casti_obce;

insert into fulltext_a 
select gid, concat(nazev_obce, ',', nazev_ulice) fulltext
from address_points
where nazev_obce = nazev_casti_obce;

create table fulltext
as
SELECT fulltext, array_agg(gid) gids
FROM fulltext_a
GROUP BY fulltext;

drop table fulltext_a;