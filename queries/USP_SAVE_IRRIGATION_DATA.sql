USE MeshliumDB;

DROP PROCEDURE IF EXISTS USP_SAVE_IRRIGATION_DATA;
DELIMITER //
CREATE PROCEDURE USP_SAVE_IRRIGATION_DATA(
In CROPID int,
In DURATION int
)
BEGIN

INSERT INTO IRRIGATION (CROPID, IRIIGATIONTIME, DURATION) values (CROPID, UTC_TIMESTAMP(), DURATION);

END
//
DELIMITER ;