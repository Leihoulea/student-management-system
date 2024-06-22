DELIMITER //

CREATE PROCEDURE AddStudent(
    IN p_student_id INT,
    IN p_name VARCHAR(100),
    IN p_gender ENUM('M', 'F'),
    IN p_major_id INT,
    IN p_birthdate DATE
)
BEGIN
    INSERT INTO students (student_id, name, gender, major_id, birthdate)
    VALUES (p_student_id, p_name, p_gender, p_major_id, p_birthdate);
END //

DELIMITER ;
