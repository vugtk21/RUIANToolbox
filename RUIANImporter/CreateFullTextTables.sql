# ##################################################
# This script creates full text search tables
# ##################################################

# --------------------------------------------------
# Create temporary table fulltext_a and fill it with partial data
# --------------------------------------------------
drop table if exists fulltext_a;
create table fulltext_a
as
select gid, concat(nazev_obce, ',', nazev_casti_obce, ',', nazev_ulice) searchstr
from address_points
where nazev_obce <> nazev_casti_obce;

# --------------------------------------------------
# add rest of values
# --------------------------------------------------
insert into fulltext_a 
select gid, concat(nazev_obce, ',', nazev_ulice) searchstr
from address_points
where nazev_obce = nazev_casti_obce;

# --------------------------------------------------
# Create table fulltext
# --------------------------------------------------
DROP TABLE IF EXISTS fulltext;
create table fulltext
as
SELECT searchstr, array_agg(gid) gids
FROM fulltext_a
GROUP BY searchstr;

# --------------------------------------------------
# Drop temporary table fulltext_a
# --------------------------------------------------
drop table fulltext_a;

# --------------------------------------------------
# Create search function explode_array
# --------------------------------------------------
create or replace function explode_array(in_array anyarray) returns setof anyelement as
$$
    select ($1)[s] from generate_series(1,array_upper($1, 1)) as s;
$$
language sql immutable;

# --------------------------------------------------
# Create table gids
# --------------------------------------------------
drop table if exists gids
create table gids
as
select gid from address_points
group by gid order by gid