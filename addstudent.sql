USE StudentManagement;
DELIMITER //

CREATE PROCEDURE add_student(
    IN p_student_id VARCHAR(20),
    IN p_name VARCHAR(50),
    IN p_gender CHAR(1),
    IN p_birthdate DATE,
    IN p_major_id VARCHAR(10),
    IN p_photo LONGBLOB
)
BEGIN
    -- 检查学号是否重复
    IF EXISTS (SELECT 1 FROM Students WHERE student_id = p_student_id) THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Student ID already exists';
    ELSE
        -- 插入新的学生信息
        INSERT INTO Students (student_id, name, gender, birthdate, major_id, photo)
        VALUES (p_student_id, p_name, p_gender, p_birthdate, p_major_id, p_photo);
    END IF;
END //

DELIMITER ;

