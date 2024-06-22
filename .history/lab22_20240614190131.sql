-- 使用 StudentManagement 数据库
USE StudentManagement;

-- 删除表以防止冲突
DROP TABLE IF EXISTS MajorChanges;
DROP TABLE IF EXISTS Awards;
DROP TABLE IF EXISTS CourseGrades;
DROP TABLE IF EXISTS Enrollments;
DROP TABLE IF EXISTS Students;
DROP TABLE IF EXISTS Majors;
DROP TABLE IF EXISTS Courses;

-- 创建 Students 表
CREATE TABLE Students (
    student_id VARCHAR(20) PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    gender CHAR(1) NOT NULL CHECK (gender IN ('M', 'F')),
    birthdate DATE NOT NULL,
    major_id VARCHAR(10) NOT NULL,
    photo LONGBLOB,  -- 用于存储学生照片
    FOREIGN KEY (major_id) REFERENCES Majors(major_id) ON DELETE RESTRICT ON UPDATE CASCADE
);

-- 创建 Majors 表
CREATE TABLE Majors (
    major_id VARCHAR(10) PRIMARY KEY,
    major_name VARCHAR(50) NOT NULL
);

-- 创建 MajorChanges 表
CREATE TABLE MajorChanges (
    change_id INT AUTO_INCREMENT PRIMARY KEY,
    student_id VARCHAR(20) NOT NULL,
    old_major_id VARCHAR(10) NOT NULL,
    new_major_id VARCHAR(10) NOT NULL,
    change_date DATE NOT NULL,
    FOREIGN KEY (student_id) REFERENCES Students(student_id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (old_major_id) REFERENCES Majors(major_id) ON DELETE RESTRICT ON UPDATE CASCADE,
    FOREIGN KEY (new_major_id) REFERENCES Majors(major_id) ON DELETE RESTRICT ON UPDATE CASCADE
);

-- 创建 Awards 表
CREATE TABLE Awards (
    award_id INT AUTO_INCREMENT PRIMARY KEY,
    student_id VARCHAR(20) NOT NULL,
    award_type ENUM('Reward', 'Punishment') NOT NULL,
    award_name VARCHAR(50) NOT NULL,
    award_date DATE NOT NULL,
    FOREIGN KEY (student_id) REFERENCES Students(student_id) ON DELETE CASCADE ON UPDATE CASCADE
);

-- 创建 Courses 表
CREATE TABLE Courses (
    course_id VARCHAR(10) PRIMARY KEY,
    course_name VARCHAR(50) NOT NULL,
    credits INT NOT NULL CHECK (credits > 0),
    hours INT NOT NULL CHECK (hours > 0)
);

-- 创建 CourseGrades 表
CREATE TABLE CourseGrades (
    grade_id INT AUTO_INCREMENT PRIMARY KEY,
    student_id VARCHAR(20) NOT NULL,
    course_id VARCHAR(10) NOT NULL,
    grade DECIMAL(3, 2) NOT NULL CHECK (grade >= 0.00 AND grade <= 10.00),
    grade_date DATE NOT NULL,
    FOREIGN KEY (student_id) REFERENCES Students(student_id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (course_id) REFERENCES Courses(course_id) ON DELETE CASCADE ON UPDATE CASCADE
);

-- 创建 Enrollments 表
CREATE TABLE Enrollments (
    enrollment_id INT AUTO_INCREMENT PRIMARY KEY,
    student_id VARCHAR(20) NOT NULL,
    course_id VARCHAR(10) NOT NULL,
    enrollment_date DATE NOT NULL,
    FOREIGN KEY (student_id) REFERENCES Students(student_id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (course_id) REFERENCES Courses(course_id) ON DELETE CASCADE ON UPDATE CASCADE
);
