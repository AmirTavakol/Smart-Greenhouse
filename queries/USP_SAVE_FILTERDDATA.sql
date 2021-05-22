USE MeshliumDB;

DROP PROCEDURE IF EXISTS USP_SAVE_FILTERDDATA;
DELIMITER //
CREATE PROCEDURE USP_SAVE_FILTERDDATA(
IN INPUT JSON
)
BEGIN

UPDATE FILTEREDDATA
SET 
	FILTEREDDATA.value = NULL, 
	FILTEREDDATA.dateModified = UTC_TIMESTAMP(),
	FILTEREDDATA.wasOutlier = 1
WHERE
FILTEREDDATA.sensorParserId in (select data.ID from
JSON_TABLE(
         input,
         "$[*]"
         COLUMNS(
          ID INT PATH "$.ID",
          isOutlier bool PATH "$.isOutlier"
         )
       ) data
where data.isOutlier = 1);

Insert into FILTEREDDATA (sensor,value,timestamp,sensorParserId,wasOutlier,dateInserted,dateModified)
SELECT data.sensor, 
	case data.isOutlier
	when 1 then NULL
	else data.value
	end, data.timestamp,data.ID, data.isOutlier, UTC_TIMESTAMP(), UTC_TIMESTAMP()
     FROM
       JSON_TABLE(
         INPUT,
         "$[*]"
         COLUMNS(
          sensor Varchar(16) Path "$.sensor",
		  value varchar(50) PATH "$.value",
          `timestamp` timestamp PATH "$.timestamp",
          ID INT PATH "$.ID",
          isOutlier bool PATH "$.isOutlier"
         )
       ) data
	left join FILTEREDDATA on data.ID = FILTEREDDATA.sensorParserId
	where FILTEREDDATA.sensorParserId is NULL;

END
//
DELIMITER ;