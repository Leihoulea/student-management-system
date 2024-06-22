USE library;
DROP TRIGGER IF EXISTS reserve_book;
-- 设计一个触发器，实现：当一本书被预约时, 自动将 Book 表中相应图书的status 修改为2，并增加 reserve_Times；
-- 当某本预约的书被借出时或者读者取消预约时, 自动减少 reserve_Times。
DELIMITER //
-- 当一本书被预约时, 自动将 Book 表中相应图书的status 修改为2，并增加 reserve_Times；

CREATE TRIGGER reserve_book
    BEFORE INSERT
    ON Reserve
    FOR EACH ROW
BEGIN
    -- 不允许同一个人重复预约同一本书
    SELECT COUNT(*) INTO @reserve FROM Reserve WHERE book_ID = NEW.book_id AND reader_ID = NEW.reader_id;
    IF @reserve != 0 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'You have already reserved this book.';
    END IF;
    -- 如果这本书被借出，那么status=1
    SELECT COUNT(*) INTO @borrow FROM Borrow WHERE book_ID = NEW.book_id AND return_date IS NULL;
    IF @borrow != 0 THEN
        UPDATE Book SET bstatus = 1 WHERE bid = NEW.book_id;
    ELSE
        UPDATE Book SET bstatus = 2 WHERE bid = NEW.book_id;
    END IF;

    UPDATE Book SET reserve_Times = reserve_Times + 1 WHERE bid = NEW.book_id;
END;

-- 当读者取消预约时, 自动减少 reserve_Times。
DROP TRIGGER IF EXISTS cancel_reserve;
CREATE TRIGGER cancel_reserve
    AFTER DELETE
    ON Reserve
    FOR EACH ROW
BEGIN
    -- 如果这本书被借出，那么status=1
    SELECT COUNT(*) INTO @borrow FROM Borrow WHERE book_ID = OLD.book_ID;
    SELECT COUNT(*) INTO @reserve FROM Reserve WHERE book_ID = OLD.book_ID;
    UPDATE Book SET reserve_Times = reserve_Times - 1 WHERE bid = OLD.book_ID;
    UPDATE Book SET bstatus = 1 WHERE bid = OLD.book_ID;
    IF @borrow != 0 THEN
        UPDATE Book SET bstatus = 1 WHERE bid = OLD.book_ID;
        -- 如果这本书还有预约，那么status=2
    ELSEIF @reserve != 0 THEN
        UPDATE Book SET bstatus = 2 WHERE bid = OLD.book_ID;
        -- 如果这本书没有预约，那么status=0
    ELSE
        UPDATE Book SET bstatus = 0 WHERE bid = OLD.book_ID;
    END IF;
END;
//
DELIMITER ;



-- Check initial state of the book
SELECT bid, bstatus, reserve_Times FROM Book WHERE bid = 'B012';

-- R001 makes a reservation for B012
INSERT INTO Reserve (book_ID, reader_ID, take_Date) VALUES ('B012', 'R001', '2024-06-16');

-- Check the state after reservation
SELECT bid, bstatus, reserve_Times FROM Book WHERE bid = 'B012';

-- R001 cancels the reservation for B012
DELETE FROM Reserve WHERE book_ID = 'B012' AND reader_ID = 'R001';

-- Check the final state after cancellation
SELECT bid, bstatus, reserve_Times FROM Book WHERE bid = 'B012';
