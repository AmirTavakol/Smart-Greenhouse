USE MeshliumDB;

DROP PROCEDURE IF EXISTS USP_SAVE_USER;
DELIMITER //
CREATE PROCEDURE USP_SAVE_USER(
 IN PASSWORD varchar(100),
 IN EMAIL varchar(100),
 ROLES varchar(200),
 OUT OUTPUT JSON
)
BEGIN


INSERT INTO `USER`( PASSWORD, EMAIL, ROLES) values (PASSWORD, EMAIL, ROLES);

SELECT JSON_MERGE_PRESERVE(
       JSON_OBJECT('email', EMAIL),
       JSON_OBJECT('roles', ROLES)
    ) INTO OUTPUT;

END
//
DELIMITER ;