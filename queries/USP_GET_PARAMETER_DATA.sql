USE MeshliumDB;

DROP PROCEDURE IF EXISTS USP_GET_PARAMETER_DATA;
DELIMITER //
CREATE PROCEDURE USP_GET_PARAMETER_DATA(
OUT OUTPUT JSON
)
BEGIN

DECLARE RESUlT JSON;

DECLARE MIN_TC decimal(10,3);
DECLARE MAX_TC decimal(10,3);
DECLARE MIN_HUM decimal(10,3);
DECLARE MAX_HUM decimal(10,3);
DECLARE AVG_SOLAR decimal(10,3);

SELECT
  min(sensorParser.value),
  max(sensorParser.value)
FROM sensorParser
inner join FILTEREDDATA on sensorParser.ID = FILTEREDDATA.sensorParserID
WHERE
  sensorParser.timestamp BETWEEN DATE_SUB(UTC_TIMESTAMP(), INTERVAL 24 HOUR) AND UTC_TIMESTAMP()
  AND sensorParser.sensor = 'TC'
  AND FILTEREDDATA.wasOutlier <> 1
into MIN_TC, MAX_TC;

SELECT
   min(sensorParser.value),
   max(sensorParser.value)
FROM sensorParser
inner join FILTEREDDATA on sensorParser.ID = FILTEREDDATA.sensorParserID
WHERE
  sensorParser.timestamp BETWEEN DATE_SUB(UTC_TIMESTAMP(), INTERVAL 24 HOUR) AND UTC_TIMESTAMP()
  AND sensorParser.sensor = 'HUM'
  AND FILTEREDDATA.wasOutlier <> 1
into MIN_HUM, MAX_HUM;
  
SELECT
  truncate(avg(sensorParser.value),3)
FROM sensorParser
WHERE
  sensorParser.timestamp BETWEEN DATE_SUB(UTC_TIMESTAMP(), INTERVAL 24 HOUR) AND UTC_TIMESTAMP()
  AND sensorParser.sensor = 'PAR'
into AVG_SOLAR;

SELECT JSON_MERGE_PRESERVE(
       JSON_OBJECT('min_tc', MIN_TC),
       JSON_OBJECT('max_tc', MAX_TC),
       JSON_OBJECT('min_hum', MIN_HUM),
       JSON_OBJECT('max_hum', MAX_HUM),
       JSON_OBJECT('avg_solar', AVG_SOLAR)
    ) INTO OUTPUT;

END
//
DELIMITER ;