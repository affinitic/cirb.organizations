create database if not exists gscetterbeek;
use gscetterbeek;

create table if not exists organization (
    organizationId integer unsigned not null auto_increment primary key,
    organizationName char(255) not null,

    )engine=sqlite;
