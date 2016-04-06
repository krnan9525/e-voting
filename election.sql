####
#maight be really dangerous is using drop table
####
#drop table if exists candidate;
create table candidate (
  id integer primary key autoincrement,
  name text not null,
  surname text not null,
  party_id integer references party(party_id),
  job text not null,
  age integer not null,
  address text not null
);
#drop table if exists party;
create table party (
  party_id integer primary key autoincrement,
  party_name text not null
);
#drop table if exists ballot;
create table ballot (
  ballot_id integer primary key autoincrement,
  candidate_id integer references candidate(id),
  preference_number integer null null
);
