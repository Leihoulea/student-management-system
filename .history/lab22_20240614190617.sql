CREATE DATABASE StudentManagement;

USE StudentManagement;

CREATE TABLE Students (
    student_id VARCHAR(20) PRIMARY KEY,
    name VARCHAR(50),
    gender CHAR(1),
    birthdate DATE,
    major_id VARCHAR(10)
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
