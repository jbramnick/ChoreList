DROP DATABASE IF EXISTS choretracker;
CREATE DATABASE choretracker;
\c choretracker

CREATE EXTENSION pgcrypto;

CREATE TABLE usernames (
    id SERIAL PRIMARY KEY, 
    username TEXT NOT NULL);
    
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
    name TEXT,
    group_id INT NOT NULL);
    
CREATE TABLE users (
    id INT PRIMARY KEY,
    name TEXT,
    points INT DEFAULT 0,
    group_id INT NOT NULL);
    
CREATE TABLE groups (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    admin_id INT NOT NULL);
    
    /*test data for databases*/
<<<<<<< HEAD
INSERT INTO usernames (username ) VALUES ('Brendon');
INSERT INTO admin (id,name,group_id) VALUES (1,'Brendon',1); 
=======
INSERT INTO usernames (username) VALUES ('Brendon');
>>>>>>> 1111ee2db517ff7c6b7c3242e4f2d7c32b7b3fea
INSERT INTO pass (id,password) VALUES (1,'abc1');
INSERT INTO usernames (username ) VALUES ('Jesse');
INSERT INTO admin (id,name,group_id) VALUES (2,'Jesse',1);
INSERT INTO pass (id,password) VALUES (2,'abc2');
INSERT INTO chore (name,description,rewardval, claimed,user_id,group_id) VALUES ('chore1','the first chore',5,false,1,1);
INSERT INTO groups (name,admin_id) VALUES ('group1',1);
INSERT INTO users (id,name,points,group_id) VALUES (1,'bob',0,1);
INSERT INTO reward (id,name,description,cost,stock,group_id) VALUES (1,'MONEY','Cash',5,1,1);

INSERT INTO usernames (username ) VALUES ('Alice');
INSERT INTO admin (id,name,group_id) VALUES (3,'Alice',2);
INSERT INTO pass (id,password) VALUES (3,'abc3');
INSERT INTO usernames (username ) VALUES ('Joe');
INSERT INTO admin (id,name,group_id) VALUES (4,'Joe',2);
INSERT INTO pass (id,password) VALUES (4,'abc4');
INSERT INTO chore (name,description,rewardval, claimed,user_id,group_id) VALUES ('Sweep','Sweep the living room clean',10,false,2,2);
INSERT INTO groups (name,admin_id) VALUES ('group2',2);
INSERT INTO users (id,name,points,group_id) VALUES (2,'Noami',13,2);
INSERT INTO reward (id,name,description,cost,stock,group_id) VALUES (2,'Cholate','A candy-bar of your choosing',5,10,2);
