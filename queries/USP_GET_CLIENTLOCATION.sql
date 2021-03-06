USE MeshliumDB;

DROP PROCEDURE IF EXISTS USP_GET_CLIENTLOCATION;
DELIMITER //
CREATE PROCEDURE USP_GET_CLIENTLOCATION(
OUT OUTPUT JSON
)
BEGIN

SELECT JSON_ARRAYAGG(JSON_OBJECT('latitude', `Latitude`, 'longitude', `Longitude`)) from `CLIENTDETAILS` limit 1 into OUTPUT;



END
//
DELIMITER ;