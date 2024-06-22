DELIMITER //

CREATE PROCEDURE UpdateStudent(
    IN p_student_id INT,
    IN p_name VARCHAR(100),
    IN p_gender ENUM('M', 'F'),
    IN p_major_id INT,
    IN p_birthdate DATE
)
BEGIN
    UPDATE students
    SET name = p_name, gender = p_gender, major_id = p_major_id, birthdate = p_birthdate
    WHERE student_id = p_student_id;
END //

DELIMITER ;
