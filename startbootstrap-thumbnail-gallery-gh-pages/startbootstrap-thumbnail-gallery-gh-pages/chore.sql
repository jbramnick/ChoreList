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
    id INT NOT NULL,
    group_id INT NOT NULL);
    
CREATE TABLE users (
    id INT,
    points INT DEFAULT 0,
    group_id INT NOT NULL);
    
CREATE TABLE groups (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    admin_id INT NOT NULL);

CREATE ROLE choreadmin WITH LOGIN;
\password choreadmin
/*Ag7Lb4$fS*/

GRANT SELECT,INSERT,DELETE,UPDATE ON usernames, pass, chore, reward, admin, users, groups TO choreadmin;
GRANT USAGE ON usernames_id_seq, chore_id_seq, reward_id_seq, groups_id_seq TO choreadmin;  
