import pymysql
from datetime import datetime
import re

class Database:
    def __init__(self):
        self.connection = pymysql.connect(
            host='localhost',
            user='root',
            password='258114',
            db='StudentManagement'
        )
        self.cursor = self.connection.cursor()

    def add_student(self, student_id, name, gender, birthdate, major_id, photo_file_path=None):
        if not student_id or not name or not gender or not birthdate or not major_id:
            raise ValueError("All fields except photo are required")
        
        if gender not in ['M', 'F']:
            raise ValueError("Gender must be 'M' or 'F'")
        
        if not re.match(r'^S\d{3}$', student_id):
            raise ValueError("Student ID must be in the format 'SXXX', where X is a digit.")
        
        # 读取照片数据
        photo_blob = None
        if photo_file_path:
            with open(photo_file_path, 'rb') as file:
                photo_blob = file.read()
        
        try:
            # 调用存储过程
            self.cursor.callproc('add_student', (student_id, name, gender, birthdate, major_id, photo_blob))
            self.connection.commit()
        except pymysql.MySQLError as e:
            # 捕捉并处理错误
            self.connection.rollback()
            raise ValueError(f"Error adding student: {e}")

    def update_student(self, student_id, name, gender, birthdate, photo_file_path=None):
        if not student_id or not name or not gender or not birthdate:
            raise ValueError("All fields except photo are required")
        
        if gender not in ['M', 'F']:
            raise ValueError("Gender must be 'M' or 'F'")
        
        # 检查学号是否存在
        sql = "SELECT * FROM Students WHERE student_id = %s"
        self.cursor.execute(sql, (student_id,))
        if not self.cursor.fetchone():
            raise ValueError("Student ID does not exist")
        
        photo_blob = None
        if photo_file_path:
            with open(photo_file_path, 'rb') as file:
                photo_blob = file.read()
        
        if photo_blob:
            sql = "UPDATE Students SET name = %s, gender = %s, birthdate = %s, photo = %s WHERE student_id = %s"
            self.cursor.execute(sql, (name, gender, birthdate, photo_blob, student_id))
        else:
            sql = "UPDATE Students SET name = %s, gender = %s, birthdate = %s WHERE student_id = %s"
            self.cursor.execute(sql, (name, gender, birthdate, student_id))
        
        self.connection.commit()
    
    def delete_student(self, student_id):
        if not re.match(r'^S\d{3}$', student_id):
            raise ValueError("Student ID must be in the format 'SXXX', where X is a digit.")
        
        # 检查学号是否存在
        sql = "SELECT * FROM Students WHERE student_id = %s"
        self.cursor.execute(sql, (student_id,))
        if not self.cursor.fetchone():
            raise ValueError("Student ID does not exist")
        # 删除相关的选课记录
        sql = "DELETE FROM Enrollments WHERE student_id = %s"
        self.cursor.execute(sql, (student_id,))

        # 删除相关的成绩记录
        sql = "DELETE FROM CourseGrades WHERE student_id = %s"
        self.cursor.execute(sql, (student_id,))

        # 删除相关的奖惩记录
        sql = "DELETE FROM Awards WHERE student_id = %s"
        self.cursor.execute(sql, (student_id,))

        # 删除相关的专业变更记录
        sql = "DELETE FROM MajorChanges WHERE student_id = %s"
        self.cursor.execute(sql, (student_id,))

        # 删除学生记录
        sql = "DELETE FROM Students WHERE student_id = %s"
        self.cursor.execute(sql, (student_id,))
        
        self.connection.commit()

    def get_student_info(self, student_id):
        sql = "SELECT * FROM Students WHERE student_id = %s"
        self.cursor.execute(sql, (student_id,))
        return self.cursor.fetchall()

    def get_student_average_grade(self, student_id):
        sql = "SELECT GetStudentAverageGrade(%s)"
        self.cursor.execute(sql, (student_id,))
        result = self.cursor.fetchone()
        return result[0] if result and result[0] is not None else 0.00  # 返回 0.00 如果没有结果

    def add_course_grade(self, student_id, course_id, grade, grade_date):
        if not re.match(r'^S\d{3}$', student_id):
            raise ValueError("Student ID must be in the format 'SXXX', where X is a digit.")
        
        try:
            grade = float(grade)
        except ValueError:
            raise ValueError("Grade must be a number")

        try:
            datetime.strptime(grade_date, '%Y-%m-%d')
        except ValueError:
            raise ValueError("Grade Date must be in the format 'YYYY-MM-DD'")
        
        # 检查学生ID是否存在
        sql = "SELECT * FROM Students WHERE student_id = %s"
        self.cursor.execute(sql, (student_id,))
        if not self.cursor.fetchone():
            raise ValueError("Student ID does not exist")
        
        # 检查课程ID是否存在
        sql = "SELECT * FROM Courses WHERE course_id = %s"
        self.cursor.execute(sql, (course_id,))
        if not self.cursor.fetchone():
            raise ValueError("Course ID does not exist")
        
        # 检查成绩是否重复
        sql = "SELECT * FROM CourseGrades WHERE student_id = %s AND course_id = %s AND grade_date = %s"
        self.cursor.execute(sql, (student_id, course_id, grade_date))
        if self.cursor.fetchone():
            raise ValueError("Grade already exists for the given student and course on the specified date")
        
        # 插入新的成绩
        sql = "INSERT INTO CourseGrades (student_id, course_id, grade, grade_date) VALUES (%s, %s, %s, %s)"
        self.cursor.execute(sql, (student_id, course_id, grade, grade_date))
        
        # 提交事务
        self.connection.commit()

    def update_course_grade(self, grade_id, grade, grade_date):
        try:
            grade = float(grade)
        except ValueError:
            raise ValueError("Grade must be a number")

        try:
            datetime.strptime(grade_date, '%Y-%m-%d')
        except ValueError:
            raise ValueError("Grade Date must be in the format 'YYYY-MM-DD'")
        
        # 更新成绩
        sql = "UPDATE CourseGrades SET grade = %s, grade_date = %s WHERE grade_id = %s"
        self.cursor.execute(sql, (grade, grade_date, grade_id))
        
        # 提交事务
        self.connection.commit()

    def delete_course_grade(self, grade_id):
        sql = "DELETE FROM CourseGrades WHERE grade_id = %s"
        self.cursor.execute(sql, (grade_id,))
        self.connection.commit()

    def add_course(self, course_id, course_name, credits, hours):
        if not course_id or not course_name or not credits or not hours:
            raise ValueError("All fields are required")
        
        if not re.match(r'^C\d{3}$', course_id):
            raise ValueError("Course ID must be in the format 'CXXX', where X is a digit.")
        
        try:
            credits = int(credits)
            hours = int(hours)
        except ValueError:
            raise ValueError("Credits and Hours must be integers")

        try:
            # 开始事务
            self.connection.begin()
            # 调用存储过程
            self.cursor.callproc('add_course', (course_id, course_name, credits, hours))
            # 提交事务
            self.connection.commit()
        except pymysql.MySQLError as e:
            # 捕捉并处理错误，回滚事务
            self.connection.rollback()
            raise ValueError(f"Error adding course: {e}")
        
    def update_course(self, course_id, course_name, credits, hours):
        if not course_id or not course_name or not credits or not hours:
            raise ValueError("All fields are required")
        
        if not re.match(r'^C\d{3}$', course_id):
            raise ValueError("Course ID must be in the format 'CXXX', where X is a digit.")
        
        try:
            credits = int(credits)
            hours = int(hours)
        except ValueError:
            raise ValueError("Credits and Hours must be integers")

        # 检查课程ID是否存在
        sql = "SELECT * FROM Courses WHERE course_id = %s"
        self.cursor.execute(sql, (course_id,))
        if not self.cursor.fetchone():
            raise ValueError("Course ID does not exist")
        
        # 更新课程信息
        sql = "UPDATE Courses SET course_name = %s, credits = %s, hours = %s WHERE course_id = %s"
        self.cursor.execute(sql, (course_name, credits, hours, course_id))
        
        # 提交事务
        self.connection.commit()

    def enroll_student_in_course(self, student_id, course_id):
        # 检查学生ID是否存在
        sql = "SELECT * FROM Students WHERE student_id = %s"
        self.cursor.execute(sql, (student_id,))
        if not self.cursor.fetchone():
            raise ValueError("Student ID does not exist")
        
        # 检查课程ID是否存在
        sql = "SELECT * FROM Courses WHERE course_id = %s"
        self.cursor.execute(sql, (course_id,))
        if not self.cursor.fetchone():
            raise ValueError("Course ID does not exist")
        
        # 检查学生是否已选此课程
        sql = "SELECT * FROM Enrollments WHERE student_id = %s AND course_id = %s"
        self.cursor.execute(sql, (student_id, course_id))
        if self.cursor.fetchone():
            raise ValueError("Student already enrolled in this course")
        
        # 插入新的选课记录
        sql = "INSERT INTO Enrollments (student_id, course_id, enrollment_date) VALUES (%s, %s, NOW())"
        self.cursor.execute(sql, (student_id, course_id))
        
        # 提交事务
        self.connection.commit()

    def add_award(self, student_id, award_type, award_name, award_date):
        if not re.match(r'^S\d{3}$', student_id):
            raise ValueError("Student ID must be in the format 'SXXX', where X is a digit.")
        
        if award_type not in ['Reward', 'Punishment']:
            raise ValueError("Award Type must be 'Reward' or 'Punishment'")

        try:
            datetime.strptime(award_date, '%Y-%m-%d')
        except ValueError:
            raise ValueError("Award Date must be in the format 'YYYY-MM-DD'")
        
        # 检查学生ID是否存在
        sql = "SELECT * FROM Students WHERE student_id = %s"
        self.cursor.execute(sql, (student_id,))
        if not self.cursor.fetchone():
            raise ValueError("Student ID does not exist")

        # 检查奖惩记录是否重复
        sql = "SELECT * FROM Awards WHERE student_id = %s AND award_name = %s AND award_date = %s"
        self.cursor.execute(sql, (student_id, award_name, award_date))
        if self.cursor.fetchone():
            raise ValueError("Award already exists for the given student on the specified date")

        # 插入新的奖惩记录
        sql = "INSERT INTO Awards (student_id, award_type, award_name, award_date) VALUES (%s, %s, %s, %s)"
        self.cursor.execute(sql, (student_id, award_type, award_name, award_date))
        
        # 提交事务
        self.connection.commit()

    def view_students(self):
        sql = "SELECT student_id, name, gender, birthdate, major_id, photo FROM Students"
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def view_courses(self):
        sql = "SELECT course_id, course_name, credits, hours FROM Courses"
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def view_course_grades(self):
        sql = "SELECT grade_id, student_id, course_id, grade, grade_date FROM CourseGrades"
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def view_enrollments(self):
        sql = "SELECT enrollment_id, student_id, course_id, enrollment_date FROM Enrollments"
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def view_awards(self):
        sql = "SELECT award_id, student_id, award_type, award_name, award_date FROM Awards"
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def query_student_info(self, student_id):
        sql = """
        SELECT S.student_id, S.name, S.gender, S.birthdate, S.major_id, S.photo, C.course_id, C.course_name, G.grade, A.award_type, A.award_name, A.award_date
        FROM Students S
        LEFT JOIN Enrollments E ON S.student_id = E.student_id
        LEFT JOIN Courses C ON E.course_id = C.course_id
        LEFT JOIN CourseGrades G ON S.student_id = G.student_id AND C.course_id = G.course_id
        LEFT JOIN Awards A ON S.student_id = A.student_id
        WHERE S.student_id = %s
        """
        self.cursor.execute(sql, (student_id,))
        return self.cursor.fetchall()

    def query_course_info(self, course_id):
        sql = """
        SELECT C.course_id, C.course_name, C.credits, C.hours, S.student_id, S.name
        FROM Courses C
        LEFT JOIN Enrollments E ON C.course_id = E.course_id
        LEFT JOIN Students S ON E.student_id = S.student_id
        WHERE C.course_id = %s
        """
        self.cursor.execute(sql, (course_id,))
        return self.cursor.fetchall()

    def add_major_change(self, student_id, old_major_id, new_major_id, change_date):
        # 检查学生ID是否存在
        sql = "SELECT * FROM Students WHERE student_id = %s"
        self.cursor.execute(sql, (student_id,))
        student = self.cursor.fetchone()
        if not student:
            raise ValueError("Student ID does not exist")

        # 检查旧专业ID是否存在
        sql = "SELECT * FROM Majors WHERE major_id = %s"
        self.cursor.execute(sql, (old_major_id,))
        if not self.cursor.fetchone():
            raise ValueError("Old Major ID does not exist")
        
        # 检查新专业ID是否存在
        sql = "SELECT * FROM Majors WHERE major_id = %s"
        self.cursor.execute(sql, (new_major_id,))
        if not self.cursor.fetchone():
            raise ValueError("New Major ID does not exist")

        # 检查学生的当前专业是否与输入的旧专业一致
        current_major_id = student[4]  # 假设major_id在Students表中的第5列（从0开始计数）
        if current_major_id != old_major_id:
            raise ValueError("The student's current major does not match the old major provided")

        # 插入新的专业变更记录
        sql = "INSERT INTO MajorChanges (student_id, old_major_id, new_major_id, change_date) VALUES (%s, %s, %s, %s)"
        self.cursor.execute(sql, (student_id, old_major_id, new_major_id, change_date))
        
        # 更新学生的专业
        sql = "UPDATE Students SET major_id = %s WHERE student_id = %s"
        self.cursor.execute(sql, (new_major_id, student_id))

        # 提交事务
        self.connection.commit()

    def view_major_changes(self):
        sql = """
        SELECT change_id, student_id, old_major_id, new_major_id, change_date 
        FROM MajorChanges
        """
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def view_majors(self):
        sql = "SELECT major_id, major_name FROM Majors"
        self.cursor.execute(sql)
        return self.cursor.fetchall()
