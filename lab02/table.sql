USE student_management_system;

CREATE TABLE majors (
    major_id INT PRIMARY KEY,
    major_name VARCHAR(100) NOT NULL
);

CREATE TABLE students (
    student_id INT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    gender ENUM('M', 'F') NOT NULL,
    major_id INT,
    birthdate DATE NOT NULL,
    FOREIGN KEY (major_id) REFERENCES majors(major_id)
);

CREATE TABLE major_changes (
    change_id INT PRIMARY KEY,
    student_id INT NOT NULL,
    old_major_id INT NOT NULL,
    new_major_id INT NOT NULL,
    change_date DATE NOT NULL,
    FOREIGN KEY (student_id) REFERENCES students(student_id),
    FOREIGN KEY (old_major_id) REFERENCES majors(major_id),
    FOREIGN KEY (new_major_id) REFERENCES majors(major_id)
);

CREATE TABLE awards_and_sanctions (
    record_id INT PRIMARY KEY,
    student_id INT NOT NULL,
    type ENUM('award', 'sanction') NOT NULL,
    name VARCHAR(255) NOT NULL,
    date DATE NOT NULL,
    FOREIGN KEY (student_id) REFERENCES students(student_id)
);

CREATE TABLE courses (
    course_id INT PRIMARY KEY,
    course_name VARCHAR(100) NOT NULL,
    credits DECIMAL(3,1) NOT NULL,
    hours INT NOT NULL
);

CREATE TABLE grades (
    grade_id INT PRIMARY KEY,
    student_id INT NOT NULL,
    course_id INT NOT NULL,
    grade DECIMAL(5,2) NOT NULL,
    grade_date DATE NOT NULL,
    FOREIGN KEY (student_id) REFERENCES students(student_id),
    FOREIGN KEY (course_id) REFERENCES courses(course_id)
);
