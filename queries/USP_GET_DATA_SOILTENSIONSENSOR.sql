USE MeshliumDB;

DROP PROCEDURE IF EXISTS USP_GET_DATA_SOILTENSIONSENSOR;
DELIMITER //
CREATE PROCEDURE USP_GET_DATA_SOILTENSIONSENSOR(
IN DAYS int)
BEGIN
set @sensor = 'SOIL3';
set @samples  = 24*4*DAYS;

PREPARE STMT FROM 'Select value FROM sensorParser WHERE sensor = ? ORDER BY timestamp DESC LIMIT ?';
EXECUTE STMT USING @sensor,@samples ;


END
//
DELIMITER ;