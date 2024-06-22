-- 创建图书表
-- 图书号 bid 为主键
-- 书名 bname 不能为空
-- 状态 bstatus 为 0 表示可借，1 表示书被借出，2 表示已被预约，默认值为 0
-- borrow_Times 表示图书有史以来的总借阅次数, reserve_Times 表示图书当前的预约人数，默认值都为 0
-- 规定一本书只能被一个人借阅，但可以被多个人预约 //
DROP DATABASE IF EXISTS library;
CREATE DATABASE library;
USE library;

CREATE TABLE Book (
	bid CHAR(8),
    bname VARCHAR(100) NOT NULL,
    author VARCHAR(50),
    price FLOAT,
    bstatus INT DEFAULT 0,
    borrow_Times INT DEFAULT 0,
    reserve_Times INT DEFAULT 0,
    CONSTRAINT PK_Book PRIMARY KEY(bid)
);

-- 创建读者表
-- 读者号rid为主键

CREATE TABLE Reader (
	rid CHAR(8),
    rname VARCHAR(20),
    age INT,
    address VARCHAR(100),
    CONSTRAINT PK_Reader PRIMARY KEY(rid)
);

-- 创建借阅表Borrow
-- 还期 return_Date 为 NULL 表示该书未还 //
-- 主键为（图书号book_ID，读者号reader_ID，借阅日期borrow_Date）
-- 图书号book_ID为外键, 引用图书表的图书号
-- 读者号reader_ID为外键, 引用读者表的读者号
-- 规定一本书只能被一个人借阅，但可以被多个人预约

CREATE TABLE Borrow (
	book_ID CHAR(8),
    reader_ID CHAR(8),
    borrow_Date DATE,
    return_Date DATE,
    CONSTRAINT PK_Borrow PRIMARY KEY(book_ID, reader_ID, borrow_Date),
    CONSTRAINT FK_Borrow1 FOREIGN KEY(book_ID) REFERENCES Book(bid),
    CONSTRAINT FK_Borrow2 FOREIGN KEY(reader_ID) REFERENCES Reader(rid)
);

-- 创建预约表reverse
-- 其中主键为(图书号book_ID，读者号reader_ID，预约日期reserve_Date)
-- reserve_Date 默认为当前日期
-- take_Date 为预约取书的日期且要求晚于 reserve_Date

CREATE TABLE Reserve (
	book_ID CHAR(8),
    reader_ID CHAR(8),
    reverse_Date DATE DEFAULT(CURDATE()),
    take_Date DATE,
    CONSTRAINT PK_Reverse PRIMARY KEY(book_ID, reader_ID, reverse_Date),
    CONSTRAINT CK_Reverse CHECK (take_Date > reverse_Date)
)