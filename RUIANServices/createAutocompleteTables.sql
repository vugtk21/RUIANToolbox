create table psc
as
select CAST(psc AS text), nazev_obce
from address_points
group by psc, nazev_obce;

create table obce
as
select nazev_obce, CAST(psc AS text)
from address_points
group by nazev_obce, psc
order by nazev_obce, psc

create table ulice
as
select nazev_ulice, nazev_obce, CAST(psc AS text) from address_points where nazev_ulice <> '' 
group by nazev_ulice, nazev_obce, psc order by nazev_ulice, nazev_obce, psc

create table gids
as
select gid from address_points
group by gid order by gid