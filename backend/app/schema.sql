DROP TABLE IF EXISTS data;
DROP TABLE IF EXISTS user;

CREATE TABLE data (
    id integer primary key autoincrement,
    sensorid integer not null,
    reading real not null,
    timestamp text not null,
    sensortype text not null
);

CREATE TABLE user (
    id integer primary key autoincrement,
    username text unique not null,
    password text not null
)