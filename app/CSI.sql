-- drop database IF EXISTS csi;
-- create database csi;
-- use csi;

-- drop table IF EXISTS User;
-- drop table IF EXISTS Regular;
-- drop table IF EXISTS Organizer;
-- drop table IF EXISTS Sets;
-- drop table IF EXISTS Grouped;
-- drop table IF EXISTS joinSet;
-- drop table IF EXISTS Scores;
-- drop table IF EXISTS pin_user;
-- drop table IF EXISTS Administrator;
-- drop table IF EXISTS Dictionary;


-- create table User(
--     user_id int auto_increment not null,
--     type varchar(20) not null,
--     first_name varchar(30) not null,
--     last_name varchar(30) not null,
--     username varchar(30) not null unique,
--     email varchar(65) not null,
--     password varchar(255) not null,
--     primary key(user_id)
-- );

-- create table Regular (
--     user_id int not null,
--     sex varchar(10),
--     age varchar(10),
--     height varchar(50),
--     leadership varchar(35),
--     ethnicity varchar(35),
--     personality varchar(35),
--     education varchar(35),
--     hobby varchar(50),
--     occupation varchar(50),
--     pref_sex varchar(50),
--     pref_ethnicity varchar(50),
--     primary key(user_id), 
--     foreign key (user_id) references User(user_id) on delete cascade
-- );

-- create table Organizer (
--     user_id int auto_increment not null, 
--     position varchar (50),
--     primary key(user_id),
--     foreign key (user_id) references User(user_id) on delete cascade
-- );


-- create table Sets (
--     sid int auto_increment not null, 
--     set_name varchar (20) unique,
--     purpose varchar (30),
--     code varchar (10),
--     organizer int,
--     primary key(sid),
--     foreign key (organizer) references organizer(user_id) on delete cascade
-- );

-- create table joinSet(
--     user_id int not null,
--     sid int not null,
--     primary key (user_id, sid),
--     foreign key (user_id) references Regular(user_id) on delete cascade,
--     foreign key (sid) references Sets(sid) on delete cascade
-- );

-- create table SetUserGroup (
--     user_id int not null,
--     sid int not null,
--     group_num int not null,
--     primary key (user_id, sid, group_num),
--     foreign key (user_id) references Regular(user_id) on delete cascade,
--     foreign key (sid) references Sets(sid) on delete cascade
-- );

-- create table Scores(
--     user_id int not null,
--     match_id int not null,
--     score decimal (3, 2),
--     primary key (user_id, match_id),
--     foreign key (user_id) references Regular(user_id) on delete cascade on update cascade,
--     foreign key (match_id) references Regular(user_id) on delete cascade on update cascade
-- );

-- create table pin_user (
--     user_id int not null,
--     match_id int not null,
--     primary key(user_id, match_id),
--     foreign key (user_id) references User (user_id) on delete cascade on update cascade,
--     foreign key (match_id) references User (user_id) on delete cascade on update cascade
-- );

-- create table Administrator (
--     admin_id varchar(10) not null,
--     first_name varchar(30),
--     last_name varchar(30),
--     primary key (admin_id)
-- );

-- create table Dictionary (
--     dict_id varchar(10) not null,
--     admin_id varchar(10) not null,
--     personality_weight int,
--     leadership_weight int,
--     hobby_weight int,
--     democratic varchar(500),
--     autocratic varchar(500),
--     laissez_faire varchar(500),
--     ambivert varchar(500),
--     extrovert varchar(500),
--     introvert varchar(500),
--     sports varchar(500),
--     music varchar(500),
--     exercising varchar(500),
--     reading varchar(500),
--     shopping varchar(500),
--     writing varchar(500),
--     dancing varchar(500),
--     arts varchar(500),
--     watching_tv varchar(500),
--     primary key (dict_id),
--     foreign key (admin_id) references Administrator (admin_id) on delete cascade on update cascade
-- );


-- insert into Administrator values('A-01', 'Horfield', 'Brovers');

-- insert into Dictionary values('D-01', 'A-01', 5, 5, 5,'participative leadership or shared leadership,members of the group take a more participative role in the decision-making process', 'authoritarian leadership, individual control over all decisions and little input from group members.rarely accept advice from followers', 'delegative leadership,leaders are hands-off and allow group members to make the decisions. lowest productivity among group members', 'normal overall behavior is between introversion and extroversion', 'Their outgoing, vibrant nature draws people to them, and they have a hard time turning away the attention. They thrive off the interaction', 'Introverts tend to feel drained after socializing and regain their energy by spending time alone', 'activity needing physical effort and skill that is played according to rules, for enjoyment or as a job', 'an art of sound in time that expresses ideas and emotions in significant forms through the elements of rhythm, melody, harmony, and color', 'activity requiring physical effort, carried out to sustain or improve health and fitness', 'cognitive process of decoding symbols to derive meaning', 'Searching for or buying goods', 'using symbols to communicate thoughts and ideas in a readable form', "to move one's body, rhythmically in a pattern of steps", 'expression of human creative skill and imagination', 'keep under attentive view or observation or view attentively with interest to a broadcast on television');


-- insert into user values (11, 'Regular', 'Bradley', 'Pitt', 'Brad', 'bradpitt@gmail.com', PASSWORD('pass'));

-- insert into pin_user values (1, 5);
-- insert into pin_user values (5, 1);

-- insert into pin_user values (1, 6);
-- insert into pin_user values (6, 1);

-- insert into pin_user values (1, 7);
-- insert into pin_user values (7, 1);


-- insert into pin_user values (1, 8);
-- insert into pin_user values (8, 1);


-- insert into pin_user values (1, 9);
-- insert into pin_user values (9, 1);