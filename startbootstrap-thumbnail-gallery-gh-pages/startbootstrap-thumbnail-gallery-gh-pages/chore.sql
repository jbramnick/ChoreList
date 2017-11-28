DROP DATABASE IF EXISTS choretracker;
CREATE DATABASE choretracker;
\c choretracker

CREATE EXTENSION pgcrypto;

CREATE TABLE usernames (
    id SERIAL PRIMARY KEY, 
    username TEXT NOT NULL,
    name TEXT);
    
CREATE TABLE pass (
    id INT PRIMARY KEY, 
    password TEXT NOT NULL);

/* insert into pass values(id, crypt('pass', gen_salt('bf'))); */
/* select * from pass where password = crypt('password', password); */

CREATE TABLE chore (
    id SERIAL PRIMARY KEY, 
    name TEXT NOT NULL, 
    description TEXT NOT NULL,
    rewardVal INT NOT NULL,
    claimed BOOL NOT NULL, 
    user_id INT,
    group_id INT NOT NULL);
    
CREATE TABLE reward (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT NOT NULL,
    cost INT NOT NULL,
    stock INT,
    group_id INT NOT NULL);
    
CREATE TABLE admin (
    id INT PRIMARY KEY,
    group_id INT NOT NULL);
    
CREATE TABLE users (
    id INT PRIMARY KEY,
    points INT DEFAULT 0,
    group_id INT NOT NULL);
    
CREATE TABLE groups (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    admin_id INT NOT NULL);
 
    /*test data for databases*/
/*
INSERT INTO usernames (username, name) VALUES ('Slark','Brendon');
INSERT INTO pass (id,password) VALUES (1,crypt('abc1', gen_salt('bf')));
INSERT INTO usernames (username, name) VALUES ('Brexit','Jesse');
INSERT INTO admin (id,name,group_id) VALUES (2,'Jesse',1);
INSERT INTO pass (id,password) VALUES (2,crypt('abc2', gen_salt('bf')));
INSERT INTO chore (name,description,rewardval, claimed,user_id,group_id) VALUES ('chore1','the first chore',5,false,1,1);
INSERT INTO groups (name,admin_id) VALUES ('group1',1);
INSERT INTO users (id,name,points,group_id) VALUES (1,'bob',0,1);
INSERT INTO reward (id,name,description,cost,stock,group_id) VALUES (1,'MONEY','Cash',5,1,1);

INSERT INTO usernames (username, name) VALUES ('MarthaStewart','Alice');
INSERT INTO admin (id,name,group_id) VALUES (3,'Alice',2);
INSERT INTO pass (id,password) VALUES (3,crypt('abc3', gen_salt('bf')));
INSERT INTO usernames (username, name) VALUES ('ThisGuy','Joe');
INSERT INTO admin (id,name,group_id) VALUES (4,'Joe',2);
INSERT INTO pass (id,password) VALUES (4,crypt('abc4', gen_salt('bf')));
INSERT INTO chore (name,description,rewardval, claimed,user_id,group_id) VALUES ('Sweep','Sweep the living room clean',10,false,2,2);
INSERT INTO groups (name,admin_id) VALUES ('group2',2);
INSERT INTO users (id,name,points,group_id) VALUES (2,'Noami',13,2);
INSERT INTO reward (id,name,description,cost,stock,group_id) VALUES (2,'Cholate','A candy-bar of your choosing',5,10,2);*/


CREATE ROLE choreadmin WITH LOGIN;
\password choreadmin
/*Ag7Lb4$fS*/

GRANT SELECT,INSERT,DELETE,UPDATE ON usernames, pass, chore, reward, admin, users, groups TO choreadmin;
GRANT USAGE ON usernames_id_seq, chore_id_seq, reward_id_seq, groups_id_seq TO choreadmin;  
