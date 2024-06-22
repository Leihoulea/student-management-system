USE library;
DROP PROCEDURE IF EXISTS borrowBook;
DELIMITER //

CREATE PROCEDURE borrowBook(IN readerId CHAR(8), IN bookId CHAR(8), IN borrowDate DATE)
END_LABLE:
BEGIN
    -- 书是否被别人借了 
    SELECT COUNT(*) INTO @borrow FROM Borrow WHERE book_ID = bookId AND return_Date IS NULL AND reader_id != readerid;
    IF @borrow > 0 THEN
       SELECT "书已经被别人借了";
       LEAVE END_LABLE;
    END IF;
    
    -- 同一天不允许同一个读者重复借阅同一本读书；
    SELECT COUNT(*) INTO @count FROM Borrow
    WHERE book_ID = bookId
      AND reader_ID = readerId
      AND borrow_date = borrowDate;
    IF @count > 0 THEN
        SELECT "借阅失败！同一天已经借阅过";
        LEAVE END_LABLE;
    END IF;

    -- 一个读者最多只能借阅 3 本图书
    SELECT COUNT(*) INTO @count FROM Borrow WHERE reader_ID = readerId AND return_date IS NULL;
    IF @count >= 3 THEN
        SELECT "借阅失败！已借三本书未还";
        LEAVE END_LABLE;
    END IF;

    -- 如果该图书存在预约记录，而当前借阅者没有预约，则不允许借阅；
    SELECT COUNT(*) INTO @count_me FROM Reserve WHERE book_ID = bookId AND reader_ID = readerId;
    SELECT COUNT(*) INTO @count_others FROM Reserve WHERE book_ID = bookId AND reader_id != readerId;
    IF @count_me = 0 AND @count_others > 0 THEN  
		SELECT "借阅失败！未预约";
        LEAVE END_LABLE;
    END IF;

    -- 检查通过，可以借阅
    -- 插入borrow
    INSERT INTO Borrow(reader_ID, book_ID, borrow_Date) VALUES (readerId, bookId, borrowDate);
    -- 修改book中的time和bstatus
    UPDATE Book SET borrow_Times = Book.borrow_Times + 1, bstatus = 1 WHERE bid = bookId;
    -- 借阅成功删除预约记录
    DELETE FROM Reserve WHERE book_ID = bookId AND reader_ID = readerId;

    -- 输出成功信息
    SELECT "借阅成功";

END;
//
DELIMITER ;

SELECT * FROM borrow;
SELECT * FROM reserve;
-- 未预约，别人预约，借阅失败
CALL borrowBook('R001','B008','2024-05-9');

-- 预约成功的，展示预约记录被删除还有book表的变化
SELECT * FROM reserve;
SELECT * FROM book WHERE bid ='B001';
CALL borrowBook('R001','B001','2024-05-9');

-- 同一天，同一个人再次借阅同一本书
CALL borrowBook('R001','B001','2024-05-9');

-- 同一个人借三本书未还
CALL borrowBook('R005','B008','2024-05-9');
