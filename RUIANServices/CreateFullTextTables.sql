# Create full text tables

create table fulltext_a
as
select gid, concat(nazev_obce, ',', nazev_casti_obce, ',', nazev_ulice) searchstr
from address_points
where nazev_obce <> nazev_casti_obce;

insert into fulltext_a 
select gid, concat(nazev_obce, ',', nazev_ulice) searchstr
from address_points
where nazev_obce = nazev_casti_obce;

create table fulltext
as
SELECT searchstr, array_agg(gid) gids
FROM fulltext_a
GROUP BY searchstr;

drop table fulltext_a;

create or replace function explode_array(in_array anyarray) returns setof anyelement as
$$
    select ($1)[s] from generate_series(1,array_upper($1, 1)) as s;
$$
language sql immutable;

create table gids
as
select gid from address_points
group by gid order by gid