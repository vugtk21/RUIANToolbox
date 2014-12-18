
-- ##################################################
-- This script creates Auto complete search tables
-- ##################################################

-- --------------------------------------------------
-- Create table psc
-- --------------------------------------------------
drop table if exists ac_psc;
create table ac_psc
as
select CAST(psc AS text), nazev_obce, nazev_casti_obce, nazev_ulice
from address_points
group by psc, nazev_obce, nazev_casti_obce, nazev_ulice;

-- --------------------------------------------------
-- Create table address_points
-- --------------------------------------------------
drop table if exists ac_obce;
create table ac_obce
as
select nazev_obce
from address_points
group by nazev_obce
order by nazev_obce;

-- --------------------------------------------------
-- Create table ac_ulice
-- --------------------------------------------------
drop table if exists ac_ulice;
create table ac_ulice
as
select nazev_ulice, nazev_obce, nazev_casti_obce, CAST(psc AS text) from address_points where nazev_ulice <> ''
group by nazev_ulice, nazev_obce, nazev_casti_obce, psc order by nazev_ulice, nazev_obce, nazev_casti_obce, psc;

-- --------------------------------------------------
-- Create table ac_casti_obce
-- --------------------------------------------------
drop table if exists ac_casti_obce;
create table ac_casti_obce as
select nazev_casti_obce, nazev_obce
from address_points
group by nazev_casti_obce, nazev_obce
order by nazev_casti_obce, nazev_obce;