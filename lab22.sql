USE StudentManagement;
DROP TABLE IF EXISTS MajorChanges;
DROP TABLE IF EXISTS Awards;
DROP TABLE IF EXISTS CourseGrades;
DROP TABLE IF EXISTS Enrollments;
DROP TABLE IF EXISTS Students;
DROP TABLE IF EXISTS Courses;
DROP TABLE IF EXISTS Majors;
DROP TABLE IF EXISTS Enrollments;


CREATE TABLE Students (
    student_id VARCHAR(20) PRIMARY KEY,
    name VARCHAR(50),
    gender CHAR(1),
    birthdate DATE,
    major_id VARCHAR(10),
    photo LONGBLOB,  -- 用于存储学生照片
    average_grade DECIMAL(5,2) DEFAULT 0.00  -- 用于存储平均成绩
);

CREATE TABLE Majors (
    major_id VARCHAR(10) PRIMARY KEY,
    major_name VARCHAR(50)
);

CREATE TABLE MajorChanges (
    change_id INT AUTO_INCREMENT PRIMARY KEY,
    student_id VARCHAR(20),
    old_major_id VARCHAR(10),
    new_major_id VARCHAR(10),
    change_date DATE,
    FOREIGN KEY (student_id) REFERENCES Students(student_id),
    FOREIGN KEY (old_major_id) REFERENCES Majors(major_id),
    FOREIGN KEY (new_major_id) REFERENCES Majors(major_id)
);

CREATE TABLE Awards (
    award_id INT AUTO_INCREMENT PRIMARY KEY,
    student_id VARCHAR(20),
    award_type VARCHAR(10),
    award_name VARCHAR(50),
    award_date DATE,
    FOREIGN KEY (student_id) REFERENCES Students(student_id)
);

CREATE TABLE Courses (
    course_id VARCHAR(10) PRIMARY KEY,
    course_name VARCHAR(50),
    credits INT,
    hours INT
);

CREATE TABLE CourseGrades (
    grade_id INT AUTO_INCREMENT PRIMARY KEY,
    student_id VARCHAR(20),
    course_id VARCHAR(10),
    grade DECIMAL(3, 2),
    grade_date DATE,
    FOREIGN KEY (student_id) REFERENCES Students(student_id),
    FOREIGN KEY (course_id) REFERENCES Courses(course_id)
);
CREATE TABLE Enrollments (
    enrollment_id INT AUTO_INCREMENT PRIMARY KEY,
    student_id VARCHAR(20),
    course_id VARCHAR(10),
    enrollment_date DATE,
    FOREIGN KEY (student_id) REFERENCES Students(student_id),
    FOREIGN KEY (course_id) REFERENCES Courses(course_id)
);