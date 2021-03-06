USE MeshliumDB;

DROP PROCEDURE IF EXISTS USP_GET_IRRIGATION_DATA_LAST_EPOCH;
DELIMITER //
CREATE PROCEDURE USP_GET_IRRIGATION_DATA_LAST_EPOCH(
In CROPID int
)
BEGIN

SELECT IRRIGATIONTIME
FROM IRRIGATION 
where  IRRIGATION.CROPID = CROPID
ORDER BY IRRIGATION.IRIIGATIONTIME DESC LIMIT 1;


END
//
DELIMITER ;