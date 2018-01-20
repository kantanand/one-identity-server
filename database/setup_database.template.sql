drop database if exists my_db;
create database my_db CHARACTER SET utf8 COLLATE utf8_general_ci;
grant all on my_db.* to 'myadmin'@'localhost' identified by 'mypass';
-- Remote Login uncomment to Enable
-- grant all on my_db.* to 'myadmin'@'%' identified by 'mypass';
use my_db;

