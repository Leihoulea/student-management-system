-- 查询读者 Rose 借过的书（包括已还和未还）的图书号、书名和借期
USE library;
SELECT Book.bid, Book.bname, Borrow.borrow_Date
FROM Book, Reader, Borrow
WHERE Book.bid = Borrow.book_ID AND Reader.rid = Borrow.reader_ID AND Reader.rname = 'Rose';

-- 查询从没有借过图书也从没有预约过图书的读者号和读者姓名
SELECT Reader.rid, Reader.rname 
FROM Reader
WHERE NOT EXISTS (
    SELECT 1 
    FROM Borrow 
    WHERE Borrow.reader_ID = Reader.rid
) 
AND NOT EXISTS (
    SELECT 1 
    FROM Reserve 
    WHERE Reserve.reader_ID = Reader.rid
);


-- 查询被借阅次数最多的作者（注意一个作者可能写了多本书）；
-- 方法A：使用借阅表 borrow 中的借书记录
SELECT Book.author
FROM Book, Borrow
WHERE Book.bid = Borrow.book_ID
GROUP BY Book.author
ORDER BY COUNT(*) DESC
LIMIT 1;
-- 方法B：使用图书表 book 中的 borrow_times
-- 这种方法更好不需要连接
SELECT Book.author
FROM Book
GROUP BY Book.author
ORDER BY SUM(borrow_times) DESC
LIMIT 1;

--  查询目前借阅未还的书名中包含“MySQL”的图书号和书名
SELECT Book.bid, Book.bname
FROM Book, Borrow
WHERE Book.bid = Borrow.book_ID AND return_Date IS NULL AND Book.bname LIKE "%MySQL%";

-- 查询借阅图书数目（多次借同一本书需重复计入）超过 3 本的读者姓名
SELECT Reader.rname
FROM Reader, Borrow
WHERE Reader.rid = Borrow.reader_ID
GROUP BY Reader.rname
HAVING COUNT(*) > 3;

-- 查询没有借阅过任何一本 J.K. Rowling 所著的图书的读者号和姓名

SELECT DISTINCT(Reader.rid), Reader.rname
FROM Book, Reader, Borrow
WHERE Book.bid = Borrow.book_ID AND reader.rid = Borrow.reader_ID AND Book.author <> "J.K. Rowling";

-- 查询 2024 年借阅图书数目排名前 3 名的读者号、姓名以及借阅图书数
SELECT Reader.rid, Reader.rname, COUNT(*) AS borrow_count
FROM Reader, Borrow
WHERE Reader.rid = Borrow.reader_ID AND borrow_Date LIKE "2024%"
GROUP BY Borrow.reader_ID
ORDER BY COUNT(*) DESC
LIMIT 3;

-- 创建一个读者借书信息的视图，该视图包含读者号、姓名、所借图书号、
-- 图书名和借期（对于没有借过图书的读者，是否包含在该视图中均可）；
-- 并使用该视图查询2024年所有读者的读者号以及所借阅的不同图书数
DROP VIEW IF EXISTS b_view;

CREATE VIEW b_view(rid, rname, bid, bname, borrow_date)
AS SELECT Reader.rid, Reader.rname, Book.bid, Book.bname, Borrow.borrow_Date
FROM Book, Reader, Borrow
WHERE Book.bid = Borrow.book_ID AND Reader.rid = Borrow.reader_ID;

SELECT b_view.rid, COUNT(DISTINCT(b_view.bid)) AS book_count
FROM b_view
WHERE b_view.borrow_date LIKE "2024%"
GROUP BY b_view.rid;


