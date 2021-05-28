use MeshliumDB;

CREATE TABLE CLIENTDETAILS
(
ID int PRIMARY KEY NOT NULL AUTO_INCREMENT,
ClientName VARCHAR(200) NOT NULL,
Latitude decimal(10,6) NOT NULL,
Longitude decimal(10,6) NOT NULL
);

Insert into CLIENTDETAILS (ClientName,Latitude,Longitude) values ('University of Turin (Agraria)', 45.066398, 7.592362);

CREATE TABLE `USER`
(
	ID int PRIMARY KEY NOT NULL AUTO_INCREMENT,
	PASSWORD VARCHAR(100) NOT NULL,
    EMAIL VARCHAR(100) NOT NULL,
    ROLES VARCHAR(200) NOT NULL,
    UNIQUE INDEX `EMAIL` (`EMAIL`)
);


CREATE TABLE CROPS
(
	`id` int PRIMARY KEY NOT NULL AUTO_INCREMENT,
    `Name` varchar(16) NOT NULL,
	`GrafanaURL` varchar(300) NOT NULL,
    `DateSeeded` datetime NOT NULL
);

Insert into CROPS (`Name`, GrafanaURL, DateSeeded) values ('Basil Crop', '','2021-04-13 00:00:00');

CREATE TABLE EVAPOTRANSPIRATIONDATA
(
	`id` int PRIMARY KEY NOT NULL AUTO_INCREMENT,
    `ET0_value` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci  DEFAULT NULL,
	`dateInserted` timestamp
);
