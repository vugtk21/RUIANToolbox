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
