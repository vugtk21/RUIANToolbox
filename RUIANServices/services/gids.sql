-- --------------------------------------------------
-- Create table gids
-- --------------------------------------------------
drop table if exists gids;
create table gids
as
select gid from address_points
group by gid order by gid;
