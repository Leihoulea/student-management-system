USE library;
DROP PROCEDURE IF EXISTS updateReaderID;
DELIMITER $$
CREATE PROCEDURE updateReaderID(IN oldID CHAR(4), IN newID CHAR(4))
BEGIN
    DECLARE count INT;

    -- 检查新 ID 是否已在表中
    SELECT COUNT(*) INTO count FROM Reader WHERE rid = newID;
    IF count > 0 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'The new ID is already in the table';
    END IF;

    -- 检查旧 ID 是否在表中
    SELECT COUNT(*) INTO count FROM Reader WHERE rid = oldID;
    IF count = 0 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'The old ID is not in the table';
    END IF;

    -- 确保更新前没有未解决的外键依赖
    SET FOREIGN_KEY_CHECKS=0;

    START TRANSACTION;
        UPDATE Borrow SET reader_ID = newID WHERE reader_ID = oldID;
        UPDATE Reserve SET reader_ID = newID WHERE reader_ID = oldID;
        UPDATE Reader SET rid = newID WHERE rid = oldID;
    COMMIT;

    SET FOREIGN_KEY_CHECKS=1;
END$$
DELIMITER ;

SET SQL_SAFE_UPDATES = 0;
CALL updateReaderID('R006', 'R999');
SET SQL_SAFE_UPDATES = 1;
SELECT * FROM Reader WHERE rid = 'R999';
SELECT * FROM Borrow WHERE Reader_ID = 'R999';
SELECT * FROM Reserve WHERE Reader_ID = 'R999';
