USE MeshliumDB;

DROP PROCEDURE IF EXISTS USP_GET_SENSOR_DATA;
DELIMITER //
CREATE PROCEDURE USP_GET_SENSOR_DATA(
IN DURATION int
)
BEGIN

SELECT
  sensor,
  value,
  timestamp,
  id
FROM sensorParser
WHERE
  timestamp BETWEEN DATE_SUB(UTC_TIMESTAMP(), INTERVAL DURATION HOUR) AND UTC_TIMESTAMP() AND
  sensor in ('PAR',
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
ORDER BY timestamp desc;



END
//
DELIMITER ;