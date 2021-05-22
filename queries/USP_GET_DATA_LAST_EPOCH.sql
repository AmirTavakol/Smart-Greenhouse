USE MeshliumDB;

DROP PROCEDURE IF EXISTS USP_GET_DATA_LAST_EPOCH;
DELIMITER //
CREATE PROCEDURE USP_GET_DATA_LAST_EPOCH()
BEGIN

SELECT Distinct  sensor, value, timestamp, id
FROM sensorParser 
where  sensor in ('PAR',
			'PLV1',
			'PLV2',
			'PLV3',
			'ANE',
			'WV',
			'TC',
			'HUM',
			'PRES',
			'SOIL3',
			'SOILTC')
 ORDER BY timestamp DESC LIMIT 11;


END
//
DELIMITER ;