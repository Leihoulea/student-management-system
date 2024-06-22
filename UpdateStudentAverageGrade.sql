USE StudentManagement;
DELIMITER $$

DROP TRIGGER IF EXISTS UpdateStudentAverageGrade $$

CREATE TRIGGER UpdateStudentAverageGrade
AFTER INSERT ON CourseGrades
FOR EACH ROW
BEGIN
    DECLARE avg_grade DECIMAL(5,2);

    -- 使用我们定义的函数 GetStudentAverageGrade 计算新的平均成绩
    SET avg_grade = GetStudentAverageGrade(NEW.student_id);

    -- 更新 Students 表中的 average_grade 字段
    UPDATE Students
    SET average_grade = avg_grade
    WHERE student_id = NEW.student_id;
END $$

DELIMITER ;

