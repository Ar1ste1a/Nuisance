CREATE DATABASE IF NOT EXISTS nuisance;

USE nuisance;

DROP TABLE IF EXISTS user;

CREATE TABLE IF NOT EXISTS user
(
        id int AUTO_INCREMENT,
        username varchar(255),
        password varchar(255),
        token varchar(800),
        PRIMARY KEY(id)
);

DROP TABLE IF EXISTS services;

CREATE TABLE IF NOT EXISTS services
(
        id int AUTO_INCREMENT,
        name varchar(255),
        price varchar(255),
        PRIMARY KEY(id)
);

DROP TABLE IF EXISTS cart;

CREATE TABLE IF NOT EXISTS cart
(
        id int AUTO_INCREMENT,
        serviceid int,
        userid int,
        PRIMARY KEY(id)
);

INSERT INTO services(name,price) VALUES
        ('rat control','2500'),
        ('exotic animals','10000'),
        ('lice infestation','500'),
        ('ants','1000000');

