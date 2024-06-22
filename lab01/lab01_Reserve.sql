USE library;
DELIMITER //
CREATE TRIGGER reserve1 AFTER INSERT ON Reserve FOR EACH ROW
BEGIN
	UPDATE Book B SET B.bstatus = 2 WHERE B.bid = NEW.book_ID;
    UPDATE Book B SET B.reserve_Times = reserve_Times + 1 WHERE B.bid = NEW.book_ID;
END //
DELIMITER ;
DROP TRIGGER IF EXISTS reserve1;
DELIMITER //
CREATE TRIGGER reserve2 AFTER DELETE ON Reserve FOR EACH ROW
BEGIN 
	DECLARE borrow_count INT;
    SELECT COUNT(*) FROM Borrow B 
		WHERE B.book_ID = old.book_ID AND B.return_Date IS NULL INTO borrow_count;
    UPDATE Book B SET B.reserve_Times = B.reserve_Times - 1 WHERE B.bid = old.book_ID;
    IF borrow_count = 0 THEN
		UPDATE Book B SET B.bstatus = 0 WHERE B.bid = old.book_ID;
	END IF;
END //
DELIMITER ;
DROP TRIGGER IF EXISTS reserve2;
INSERT INTO Reserve (book_ID, reader_ID, take_Date) VALUES ('B012','R001','2024-6-16');
DELETE FROM Reserve R WHERE R.book_ID = 'B012' AND R.reader_ID = 'R001' AND R.take_Date = '2024-6-16';
SELECT * FROM Book;
SELECT * FROM Reserve;