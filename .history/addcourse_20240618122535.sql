USE StudentManagement;

-- 删除已存在的 add_course 存储过程
DROP PROCEDURE IF EXISTS add_course;

DELIMITER //

CREATE PROCEDURE add_course(
    IN p_course_id VARCHAR(10),
    IN p_course_name VARCHAR(50),
    IN p_credits INT,
    IN p_hours INT
)
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        -- 如果出现异常，回滚事务
        ROLLBACK;
        -- 抛出错误信号
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'An error occurred while adding the course';
    END;

    -- 开始事务
    START TRANSACTION;
    
    -- 检查课程ID是否重复
    IF EXISTS (SELECT 1 FROM Courses WHERE course_id = p_course_id) THEN
        -- 如果课程ID已存在，抛出错误信号并回滚事务
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Course ID already exists';
    ELSE
        -- 插入新的课程信息
        INSERT INTO Courses (course_id, course_name, credits, hours)
        VALUES (p_course_id, p_course_name, p_credits, p_hours);
    END IF;
    
    -- 如果没有错误，提交事务
    COMMIT;
END //

DELIMITER ;
