USE MeshliumDB;

DROP PROCEDURE IF EXISTS USP_GET_CROPS;
DELIMITER //
CREATE PROCEDURE USP_GET_CROPS(
OUT OUTPUT JSON
)
BEGIN

SELECT JSON_ARRAYAGG(JSON_OBJECT('id', ID, 'name', `Name`, 'grafanaUrl', GrafanaURL, 'dateseeded', DateSeeded)) from CROPS into OUTPUT;


END
//
DELIMITER ;