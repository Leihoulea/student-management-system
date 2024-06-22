DELIMITER //

CREATE PROCEDURE AddGrade(
    IN p_grade_id INT,
    IN p_student_id INT,
    IN p_course_id INT,
    IN p_grade DECIMAL(5,2),
    IN p_grade_date DATE
)
BEGIN
    INSERT INTO grades (grade_id, student_id, course_id, grade, grade_date)
    VALUES (p_grade_id, p_student_id, p_course_id, p_grade, p_grade_date);
END //

DELIMITER ;
