drop database IF EXISTS csi;
create database csi;
use csi;

drop table IF EXISTS User;
drop table IF EXISTS Regular;
drop table IF EXISTS Organizer;
drop table IF EXISTS Sets;
drop table IF EXISTS Grouped;
drop table IF EXISTS joinSet;
drop table IF EXISTS Scores;
drop table IF EXISTS pin_user;
drop table IF EXISTS Administrator;
drop table IF EXISTS Dictionary;


create table User(
    user_id int auto_increment not null,
    type varchar(20) not null,
    first_name varchar(30) not null,
    last_name varchar(30) not null,
    username varchar(30) not null unique,
    email varchar(65) not null,
    password varchar(255) not null,
    primary key(user_id)
);

create table Regular (
    user_id int not null,
    gender varchar(10),
    age varchar(10),
    height varchar(50),
    leadership varchar(35),
    ethnicity varchar(35),
    personality varchar(35),
    education varchar(35),
    hobby varchar(50),
    faculty varchar(50),
    occupation varchar(50),
    primary key(user_id), 
    foreign key (user_id) references User(user_id) on delete cascade
);

create table Organizer (
    user_id varchar (5), 
    position varchar (50),
    primary key(user_id),
    foreign key (user_id) references User(user_id) on delete cascade
);


create table Sets (
    sid int auto_increment not null, 
    set_name varchar (20) unique,
    purpose varchar (30),
    code varchar (10),
    organizer int,
    primary key(sid),
    foreign key (organizer) references organizer(user_id) on delete cascade
);

create table joinSet(
    user_id int not null,
    sid int not null,
    primary key (user_id, sid),
    foreign key (user_id) references Regular(user_id) on delete cascade,
    foreign key (sid) references Sets(sid) on delete cascade
);

create table SetUserGroup (
    user_id int not null,
    sid int not null,
    group_num int not null,
    primary key (user_id, sid, group_num),
    foreign key (user_id) references Regular(user_id) on delete cascade,
    foreign key (sid) references Sets(sid) on delete cascade
);


create table Administrator (
    admin_id int auto_increment not null,
    first_name varchar(30),
    last_name varchar(30),
    primary key (admin_id)
);

create table Dictionary (
    admin_id int auto_increment not null,
    dict_id int auto_increment not null,
    music varchar(250),
    sports varchar(250),
    shopping varchar(250),
    dancing varchar(250),
    watching_tv varchar(250),
    reading_writing varchar(250),
    arts varchar(250),
    laissez_faire varchar(250),
    democratic varchar(250),
    autocratic varchar(250),
    introvert varchar(250),
    extrovert varchar(250),
    ambivert varchar(250),
    education varchar(250),
    height_weight int,
    faculty_weight int,
    personality_weight int,
    primary key (admin_id, dict_id),
    foreign key (admin_id) references Administrator (admin_id) on delete cascade on update cascade
);


