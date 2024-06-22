DROP PROCEDURE IF EXISTS returnBook;
DELIMITER //

CREATE PROCEDURE returnBook(IN rid CHAR(4), IN bid CHAR(4))
BEGIN
    DECLARE s INT DEFAULT 0;
    DECLARE reserve_exists INT;
    DECLARE errMsg VARCHAR(1000);
    DECLARE CONTINUE HANDLER FOR SQLEXCEPTION
    BEGIN
        GET DIAGNOSTICS CONDITION 1 errMsg = MESSAGE_TEXT;
        SET s = 1;
    END;

    SET @old_safe_updates = @@SQL_SAFE_UPDATES, @new_safe_updates = 0;
    SET SQL_SAFE_UPDATES = @new_safe_updates;

    START TRANSACTION;
    
    -- 检查是否存在未还的借阅记录
    IF NOT EXISTS (SELECT 1 FROM Borrow WHERE reader_ID = rid AND book_ID = bid AND return_Date IS NULL) THEN
        SET s = 2; -- 没有借阅这本书
    ELSE
        -- 检查是否还有其他预约这本书
        SELECT COUNT(*) INTO reserve_exists FROM Reserve WHERE book_ID = bid;
        
        -- 修改Borrow表中的还书日期信息
        UPDATE Borrow SET return_Date = '2024-05-10' WHERE reader_ID = rid AND book_ID = bid AND return_Date IS NULL;
        
        -- 根据是否有其他预约修改Book表中的信息
        UPDATE Book SET bstatus = IF(reserve_exists > 0, 2, 0) WHERE bid = bid;
    END IF;
    
    -- 错误处理
    IF s = 0 THEN
        SELECT "还书成功" AS message;
        COMMIT;
    ELSEIF s = 1 THEN
        SELECT CONCAT("SQL错误: ", errMsg) AS message;
        ROLLBACK;
    ELSE
        SELECT "还书失败!没有借阅这本书" AS message;
        ROLLBACK;
    END IF;

    SET SQL_SAFE_UPDATES = @old_safe_updates;
END //
DELIMITER ;



CALL returnBook('R001','B008'); -- 未借阅，预期失败

CALL returnBook('R001','B001'); -- 借阅后归还，预期成功
SELECT 
    b.bid,
    b.bname,
    b.bstatus,
    br.borrow_date,
    br.return_date
FROM 
    Book b
LEFT JOIN 
    Borrow br ON b.bid = br.book_ID
WHERE 
    b.bid = 'B001';

