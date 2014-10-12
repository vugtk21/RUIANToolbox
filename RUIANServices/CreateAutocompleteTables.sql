-- ##################################################
-- This script creates Auto complete search tables
-- ##################################################

-- --------------------------------------------------
-- Create table psc
-- --------------------------------------------------
drop table if exists psc;
create table psc
as
select CAST(psc AS text), nazev_obce
from address_points
group by psc, nazev_obce;

-- --------------------------------------------------
-- Create table address_points
-- --------------------------------------------------
drop table if exists address_points;
create table obce
as
select nazev_obce, CAST(psc AS text)
from address_points
group by nazev_obce, psc
order by nazev_obce, psc;

-- --------------------------------------------------
-- Create table ulice
-- --------------------------------------------------
drop table if exists ulice;
create table ulice
as
select nazev_ulice, nazev_obce, CAST(psc AS text) from address_points where nazev_ulice <> '' 
group by nazev_ulice, nazev_obce, psc order by nazev_ulice, nazev_obce, psc;

-- --------------------------------------------------
-- Create table gids
-- --------------------------------------------------
drop table if exists gids;
create table gids
as
select gid from address_points
group by gid order by gid;

-- --------------------------------------------------
-- Create table casti_obce
-- --------------------------------------------------
drop table if exists casti_obce;
create table casti_obce as
select nazev_casti_obce, nazev_obce
from address_points
group by nazev_casti_obce, nazev_obce
order by nazev_casti_obce, nazev_obce;