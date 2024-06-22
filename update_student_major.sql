USE StudentManagement;
DROP TRIGGER IF EXISTS update_student_major;
DELIMITER $$

CREATE TRIGGER update_student_major AFTER INSERT ON MajorChanges
FOR EACH ROW
BEGIN
    UPDATE Students
    SET major_id = NEW.new_major_id
    WHERE student_id = NEW.student_id;
END;

DELIMITER ;