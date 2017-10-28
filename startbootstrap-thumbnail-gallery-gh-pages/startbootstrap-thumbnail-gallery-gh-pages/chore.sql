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