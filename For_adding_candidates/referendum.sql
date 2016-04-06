--####
--#maight be really dangerous is using drop table
--####
--drop table if exists candidate;
create table referendum (
  id integer primary key autoincrement,
  description_en text not null,
  description_ir text
);
--#drop table if exists party;
create table referendum_vote(
  referendum_id integer primary key references referendum(id),
  type integer not null
);
--#drop table if exists ballot;
create table voter_table (
    PPS_number  integer primary key,
    name text,
    surname text,
    address text
);
