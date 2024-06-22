DELIMITER //

CREATE PROCEDURE AddAwardSanction(
    IN p_record_id INT,
    IN p_student_id INT,
    IN p_type ENUM('award', 'sanction'),
    IN p_name VARCHAR(255),
    IN p_date DATE
)
BEGIN
    INSERT INTO awards_and_sanctions (record_id, student_id, type, name, date)
    VALUES (p_record_id, p_student_id, p_type, p_name, p_date);
END //

DELIMITER ;
