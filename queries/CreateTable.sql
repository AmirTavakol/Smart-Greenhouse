use MeshliumDB;

CREATE TABLE FILTEREDDATA
(
	`id` int PRIMARY KEY NOT NULL AUTO_INCREMENT,
    `sensor` varchar(16) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
	`value` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci  DEFAULT NULL,
	`timestamp` timestamp NOT NULL,
    `sensorParserId` int NOT NULL,
    `wasOutlier` bool NOT NULL,
    `dateInserted` timestamp NOT NULL,
    `dateModified` timestamp NOT NULL,
    FOREIGN KEY (sensorParserId) REFERENCES sensorParser(id)
);
