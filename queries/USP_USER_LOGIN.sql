USE MeshliumDB;

DROP PROCEDURE IF EXISTS USP_USER_LOGIN;
DELIMITER //
CREATE PROCEDURE USP_USER_LOGIN(
 IN PASSWORD varchar(100),
 IN EMAIL varchar(100),
 OUT OUTPUT JSON
)
BEGIN
DECLARE VALIDUSER BOOL;
DECLARE USERID int;

SET VALIDUSER = 0;


SELECT  1, `USER`.ID FROM `USER` WHERE `USER`.EMAIL = EMAIL AND  `USER`.PASSWORD = PASSWORD INTO VALIDUSER,USERID;

IF VALIDUSER = 1 AND USERID IS NOT NULL THEN
      SELECT JSON_MERGE_PRESERVE(
       JSON_OBJECT('id', `USER`.ID),
       JSON_OBJECT('email', EMAIL),
       JSON_OBJECT('roles', ROLES)
    ) FROM `USER`
    WHERE `USER`.ID = USERID INTO OUTPUT;
ELSE
      SIGNAL SQLSTATE '45000'
			SET MESSAGE_TEXT = 'Incorrect password/email';
END IF;

END
//
DELIMITER ;