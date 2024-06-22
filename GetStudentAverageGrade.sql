DROP FUNCTION IF EXISTS GetStudentAverageGrade;

DELIMITER $$

CREATE FUNCTION GetStudentAverageGrade(p_student_id VARCHAR(20)) 
RETURNS DECIMAL(5,2)
DETERMINISTIC
BEGIN
    DECLARE avg_grade DECIMAL(5,2);

    SELECT AVG(grade) INTO avg_grade
    FROM CourseGrades
    WHERE student_id = p_student_id;

    RETURN IFNULL(avg_grade, 0.00);
END $$

DELIMITER ;
