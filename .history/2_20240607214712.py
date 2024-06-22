from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, 
    QFormLayout, QLineEdit, QDialog, QMessageBox, QFileDialog, QLabel, QInputDialog, QGroupBox, 
    QHBoxLayout, QTabWidget, QComboBox
)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
import pymysql
import sys
import re
from datetime import datetime

class Database:
    def __init__(self):
        self.connection = pymysql.connect(
            host='localhost',
            user='root',
            password='258114',  # 请替换为你的MySQL密码
            db='StudentManagement'
        )
        self.cursor = self.connection.cursor()

    def add_student(self, student_id, name, gender, birthdate, major_id, photo_path=None):
        if not student_id or not name or not gender or not birthdate or not major_id:
            raise ValueError("All fields except photo are required")
        
        if gender not in ['M', 'F']:
            raise ValueError("Gender must be 'M' or 'F'")
        
        if not re.match(r'^S\d{3}$', student_id):
            raise ValueError("Student ID must be in the format 'SXXX', where X is a digit.")
        
        # 检查学号是否重复
        sql = "SELECT * FROM Students WHERE student_id = %s"
        self.cursor.execute(sql, (student_id,))
        if self.cursor.fetchone():
            raise ValueError("Student ID already exists")
        
        sql = "INSERT INTO Students (student_id, name, gender, birthdate, major_id, photo_path) VALUES (%s, %s, %s, %s, %s, %s)"
        self.cursor.execute(sql, (student_id, name, gender, birthdate, major_id, photo_path))
        self.connection.commit()

    def update_student(self, student_id, name, gender, birthdate, photo_path=None):
        if not student_id or not name or not gender or not birthdate:
            raise ValueError("All fields except photo are required")
        
        if gender not in ['M', 'F']:
            raise ValueError("Gender must be 'M' or 'F'")
        
        # 检查学号是否存在
        sql = "SELECT * FROM Students WHERE student_id = %s"
        self.cursor.execute(sql, (student_id,))
        if not self.cursor.fetchone():
            raise ValueError("Student ID does not exist")
        
        if photo_path:
            sql = "UPDATE Students SET name = %s, gender = %s, birthdate = %s, photo_path = %s WHERE student_id = %s"
            self.cursor.execute(sql, (name, gender, birthdate, photo_path, student_id))
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

        # 检查课程ID是否存在
        sql = "SELECT * FROM Courses WHERE course_id = %s"
        self.cursor.execute(sql, (course_id,))
        if self.cursor.fetchone():
            raise ValueError("Course ID already exists")
        
        # 插入新的课程
        sql = "INSERT INTO Courses (course_id, course_name, credits, hours) VALUES (%s, %s, %s, %s)"
        self.cursor.execute(sql, (course_id, course_name, credits, hours))
        
        # 提交事务
        self.connection.commit()

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
        sql = "SELECT student_id, name, gender, birthdate, major_id, photo_path FROM Students"
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
        SELECT S.student_id, S.name, S.gender, S.birthdate, S.major_id, S.photo_path, C.course_id, C.course_name, G.grade, A.award_type, A.award_name, A.award_date
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

class AddStudentDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Add Student')
        self.setGeometry(100, 100, 400, 300)
        self.layout = QFormLayout()
        
        self.student_id_input = QLineEdit(self)
        self.name_input = QLineEdit(self)
        self.gender_input = QLineEdit(self)
        self.birthdate_input = QLineEdit(self)
        self.major_id_input = QLineEdit(self)
        self.photo_path_input = QLineEdit(self)
        self.photo_button = QPushButton('Choose Photo')
        self.photo_button.clicked.connect(self.choose_photo)
        
        self.layout.addRow('Student ID:', self.student_id_input)
        self.layout.addRow('Name:', self.name_input)
        self.layout.addRow('Gender:', self.gender_input)
        self.layout.addRow('Birthdate:', self.birthdate_input)
        self.layout.addRow('Major ID:', self.major_id_input)
        self.layout.addRow('Photo Path:', self.photo_path_input)
        self.layout.addWidget(self.photo_button)
        
        self.submit_button = QPushButton('Submit')
        self.submit_button.clicked.connect(self.submit)
        self.layout.addWidget(self.submit_button)
        
        self.setLayout(self.layout)
    
    def choose_photo(self):
        file_dialog = QFileDialog(self)
        file_dialog.setNameFilters(["Images (*.png *.xpm *.jpg)"])
        if file_dialog.exec_():
            file_names = file_dialog.selectedFiles()
            if file_names:
                self.photo_path_input.setText(file_names[0])
    
    def submit(self):
        student_id = self.student_id_input.text()
        name = self.name_input.text()
        gender = self.gender_input.text()
        birthdate = self.birthdate_input.text()
        major_id = self.major_id_input.text()
        photo_path = self.photo_path_input.text()
        
        db = Database()
        try:
            db.add_student(student_id, name, gender, birthdate, major_id, photo_path)
            QMessageBox.information(self, 'Success', 'Student added successfully')
            self.close()
        except ValueError as e:
            QMessageBox.critical(self, 'Error', str(e))

class UpdateStudentDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Update Student')
        self.setGeometry(100, 100, 300, 150)
        self.layout = QFormLayout()
        
        self.student_id_input = QLineEdit(self)
        self.check_button = QPushButton('Check Student')
        self.check_button.clicked.connect(self.check_student)
        
        self.layout.addRow('Student ID:', self.student_id_input)
        self.layout.addWidget(self.check_button)
        
        self.setLayout(self.layout)
    
    def check_student(self):
        student_id = self.student_id_input.text()

        if not re.match(r'^S\d{3}$', student_id):
            QMessageBox.critical(self, 'Error', "Student ID must be in the format 'SXXX', where X is a digit.")
            return
        
        db = Database()
        student_info = db.get_student_info(student_id)  # 获取学生个人信息
        
        if student_info:
            self.show_update_form(student_info[0])
        else:
            QMessageBox.information(self, 'Error', 'Student ID does not exist')

    def show_update_form(self, student_info):
        self.setWindowTitle('Update Student Information')
        
        # 清除旧布局中的所有小部件
        for i in reversed(range(self.layout.count())): 
            widget_to_remove = self.layout.itemAt(i).widget()
            # 移除小部件
            if widget_to_remove:
                widget_to_remove.setParent(None)
        
        # 重新设置新的布局
        self.name_input = QLineEdit(self)
        self.name_input.setText(student_info[1])
        
        self.gender_input = QLineEdit(self)
        self.gender_input.setText(student_info[2])
        
        # 将 datetime.date 转换为字符串格式
        birthdate_str = student_info[3].strftime('%Y-%m-%d')
        self.birthdate_input = QLineEdit(self)
        self.birthdate_input.setText(birthdate_str)
        
        self.photo_path_input = QLineEdit(self)
        self.photo_path_input.setText(student_info[5] if student_info[5] else "")
        
        self.photo_button = QPushButton('Choose Photo')
        self.photo_button.clicked.connect(self.choose_photo)
        
        self.layout.addRow('Name:', self.name_input)
        self.layout.addRow('Gender:', self.gender_input)
        self.layout.addRow('Birthdate:', self.birthdate_input)
        self.layout.addRow('Photo Path:', self.photo_path_input)
        self.layout.addWidget(self.photo_button)
        
        self.submit_button = QPushButton('Submit')
        self.submit_button.clicked.connect(self.submit)
        self.layout.addWidget(self.submit_button)
        
        self.setLayout(self.layout)
        self.resize(400, 300)

    def choose_photo(self):
        file_dialog = QFileDialog(self)
        file_dialog.setNameFilters(["Images (*.png *.xpm *.jpg)"])
        if file_dialog.exec_():
            file_names = file_dialog.selectedFiles()
            if file_names:
                self.photo_path_input.setText(file_names[0])
    
    def submit(self):
        student_id = self.student_id_input.text()
        name = self.name_input.text()
        gender = self.gender_input.text()
        birthdate = self.birthdate_input.text()
        photo_path = self.photo_path_input.text()
        
        db = Database()
        try:
            db.update_student(student_id, name, gender, birthdate, photo_path)
            QMessageBox.information(self, 'Success', 'Student updated successfully')
            self.close()
        except ValueError as e:
            QMessageBox.critical(self, 'Error', str(e))

class DeleteStudentDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Delete Student')
        self.setGeometry(100, 100, 300, 150)
        self.layout = QFormLayout()

        self.student_id_input = QLineEdit(self)
        self.layout.addRow('Student ID:', self.student_id_input)

        self.submit_button = QPushButton('Delete')
        self.submit_button.clicked.connect(self.submit)
        self.layout.addWidget(self.submit_button)

        self.setLayout(self.layout)

    def submit(self):
        student_id = self.student_id_input.text()

        if not re.match(r'^S\d{3}$', student_id):
            QMessageBox.critical(self, 'Error', "Student ID must be in the format 'SXXX', where X is a digit.")
            return

        db = Database()
        try:
            db.delete_student(student_id)
            QMessageBox.information(self, 'Success', 'Student deleted successfully')
            self.close()
        except ValueError as e:
            QMessageBox.critical(self, 'Error', str(e))

class AddCourseDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Add Course')
        self.setGeometry(100, 100, 400, 300)
        self.layout = QFormLayout()
        
        self.course_id_input = QLineEdit(self)
        self.course_name_input = QLineEdit(self)
        self.credits_input = QLineEdit(self)
        self.hours_input = QLineEdit(self)
        
        self.layout.addRow('Course ID:', self.course_id_input)
        self.layout.addRow('Course Name:', self.course_name_input)
        self.layout.addRow('Credits:', self.credits_input)
        self.layout.addRow('Hours:', self.hours_input)
        
        self.submit_button = QPushButton('Submit')
        self.submit_button.clicked.connect(self.submit)
        self.layout.addWidget(self.submit_button)
        
        self.setLayout(self.layout)
    
    def submit(self):
        course_id = self.course_id_input.text()
        course_name = self.course_name_input.text()
        credits = self.credits_input.text()
        hours = self.hours_input.text()
        
        db = Database()
        try:
            db.add_course(course_id, course_name, credits, hours)
            QMessageBox.information(self, 'Success', 'Course added successfully')
            self.close()
        except ValueError as e:
            QMessageBox.critical(self, 'Error', str(e))

class UpdateCourseDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Update Course')
        self.setGeometry(100, 100, 400, 300)
        self.layout = QFormLayout()

        self.course_id_input = QLineEdit(self)
        self.course_name_input = QLineEdit(self)
        self.credits_input = QLineEdit(self)
        self.hours_input = QLineEdit(self)

        self.layout.addRow('Course ID:', self.course_id_input)
        self.layout.addRow('Course Name:', self.course_name_input)
        self.layout.addRow('Credits:', self.credits_input)
        self.layout.addRow('Hours:', self.hours_input)

        self.submit_button = QPushButton('Submit')
        self.submit_button.clicked.connect(self.submit)
        self.layout.addWidget(self.submit_button)

        self.setLayout(self.layout)

    def submit(self):
        course_id = self.course_id_input.text()
        course_name = self.course_name_input.text()
        credits = self.credits_input.text()
        hours = self.hours_input.text()

        db = Database()
        try:
            db.update_course(course_id, course_name, credits, hours)
            QMessageBox.information(self, 'Success', 'Course updated successfully')
            self.close()
        except ValueError as e:
            QMessageBox.critical(self, 'Error', str(e))

class AddCourseGradeDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Add Course Grade')
        self.setGeometry(100, 100, 400, 300)
        self.layout = QFormLayout()
        
        self.student_id_input = QLineEdit(self)
        self.course_id_input = QLineEdit(self)
        self.grade_input = QLineEdit(self)
        self.grade_date_input = QLineEdit(self)
        
        self.layout.addRow('Student ID:', self.student_id_input)
        self.layout.addRow('Course ID:', self.course_id_input)
        self.layout.addRow('Grade:', self.grade_input)
        self.layout.addRow('Grade Date:', self.grade_date_input)
        
        self.submit_button = QPushButton('Submit')
        self.submit_button.clicked.connect(self.submit)
        self.layout.addWidget(self.submit_button)
        
        self.setLayout(self.layout)
    
    def submit(self):
        student_id = self.student_id_input.text()
        course_id = self.course_id_input.text()
        grade = self.grade_input.text()
        grade_date = self.grade_date_input.text()
        
        # 输入合法性检查
        if not student_id or not course_id or not grade or not grade_date:
            QMessageBox.critical(self, 'Error', 'All fields are required')
            return
        
        try:
            grade = float(grade)
        except ValueError:
            QMessageBox.critical(self, 'Error', 'Grade must be a number')
            return
        
        try:
            datetime.strptime(grade_date, '%Y-%m-%d')
        except ValueError:
            QMessageBox.critical(self, 'Error', 'Grade Date must be in the format YYYY-MM-DD')
            return
        
        db = Database()
        try:
            db.add_course_grade(student_id, course_id, grade, grade_date)
            QMessageBox.information(self, 'Success', 'Grade added successfully')
            self.close()
        except ValueError as e:
            QMessageBox.critical(self, 'Error', str(e))

class UpdateCourseGradeDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Update Course Grade')
        self.setGeometry(100, 100, 400, 300)
        self.layout = QFormLayout()

        self.grade_id_input = QLineEdit(self)
        self.grade_input = QLineEdit(self)
        self.grade_date_input = QLineEdit(self)

        self.layout.addRow('Grade ID:', self.grade_id_input)
        self.layout.addRow('Grade:', self.grade_input)
        self.layout.addRow('Grade Date:', self.grade_date_input)

        self.submit_button = QPushButton('Submit')
        self.submit_button.clicked.connect(self.submit)
        self.layout.addWidget(self.submit_button)

        self.setLayout(self.layout)

    def submit(self):
        grade_id = self.grade_id_input.text()
        grade = self.grade_input.text()
        grade_date = self.grade_date_input.text()

        # 输入合法性检查
        if not grade_id or not grade or not grade_date:
            QMessageBox.critical(self, 'Error', 'All fields are required')
            return

        try:
            grade = float(grade)
        except ValueError:
            QMessageBox.critical(self, 'Error', 'Grade must be a number')
            return

        try:
            datetime.strptime(grade_date, '%Y-%m-%d')
        except ValueError:
            QMessageBox.critical(self, 'Error', 'Grade Date must be in the format YYYY-MM-DD')
            return

        db = Database()
        try:
            db.update_course_grade(grade_id, grade, grade_date)
            QMessageBox.information(self, 'Success', 'Grade updated successfully')
            self.close()
        except ValueError as e:
            QMessageBox.critical(self, 'Error', str(e))

class DeleteCourseGradeDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Delete Course Grade')
        self.setGeometry(100, 100, 300, 150)
        self.layout = QFormLayout()

        self.grade_id_input = QLineEdit(self)
        self.layout.addRow('Grade ID:', self.grade_id_input)

        self.submit_button = QPushButton('Delete')
        self.submit_button.clicked.connect(self.submit)
        self.layout.addWidget(self.submit_button)

        self.setLayout(self.layout)

    def submit(self):
        grade_id = self.grade_id_input.text()

        db = Database()
        try:
            db.delete_course_grade(grade_id)
            QMessageBox.information(self, 'Success', 'Grade deleted successfully')
            self.close()
        except ValueError as e:
            QMessageBox.critical(self, 'Error', str(e))

class EnrollStudentDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Enroll Student in Course')
        self.setGeometry(100, 100, 400, 200)
        self.layout = QFormLayout()
        
        self.student_id_input = QLineEdit(self)
        self.course_id_input = QLineEdit(self)
        
        self.layout.addRow('Student ID:', self.student_id_input)
        self.layout.addRow('Course ID:', self.course_id_input)
        
        self.submit_button = QPushButton('Submit')
        self.submit_button.clicked.connect(self.submit)
        self.layout.addWidget(self.submit_button)
        
        self.setLayout(self.layout)
    
    def submit(self):
        student_id = self.student_id_input.text()
        course_id = self.course_id_input.text()
        
        if not student_id or not course_id:
            QMessageBox.critical(self, 'Error', 'Both fields are required')
            return
        
        db = Database()
        try:
            db.enroll_student_in_course(student_id, course_id)
            QMessageBox.information(self, 'Success', 'Student enrolled successfully')
            self.close()
        except ValueError as e:
            QMessageBox.critical(self, 'Error', str(e))

class QueryStudentDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Query Student Information')
        self.setGeometry(100, 100, 600, 400)
        self.layout = QVBoxLayout()
        
        self.student_id_input = QLineEdit(self)
        self.query_button = QPushButton('Query')
        self.query_button.clicked.connect(self.query_student)
        
        self.layout.addWidget(QLabel('Student ID:'))
        self.layout.addWidget(self.student_id_input)
        self.layout.addWidget(self.query_button)
        
        self.result_table = QTableWidget()
        self.layout.addWidget(self.result_table)
        
        self.setLayout(self.layout)
    
    def query_student(self):
        student_id = self.student_id_input.text()
        
        # 检查输入的学号格式
        if not re.match(r'^S\d{3}$', student_id):
            QMessageBox.critical(self, 'Error', "Student ID must be in the format 'SXXX', where X is a digit.")
            return
        
        db = Database()
        # 检查学号是否存在
        student_info = db.get_student_info(student_id)
        if not student_info:
            QMessageBox.critical(self, 'Error', 'Student ID does not exist')
            return
        
        results = db.query_student_info(student_id)
        
        if not results:
            QMessageBox.information(self, 'No Results', 'No information found for the given Student ID')
            return
        
        self.result_table.setRowCount(0)
        self.result_table.setColumnCount(12)
        self.result_table.setHorizontalHeaderLabels([
            'Student ID', 'Name', 'Gender', 'Birthdate', 'Major ID', 'Photo', 'Course ID', 'Course Name', 
            'Grade', 'Award Type', 'Award Name', 'Award Date'
        ])
        
        for row_number, row_data in enumerate(results):
            self.result_table.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                if column_number == 5 and data:  # Display the photo
                    photo_label = QLabel()
                    pixmap = QPixmap(data)
                    pixmap = pixmap.scaled(50, 50, Qt.KeepAspectRatio)
                    photo_label.setPixmap(pixmap)
                    self.result_table.setCellWidget(row_number, column_number, photo_label)
                else:
                    self.result_table.setItem(row_number, column_number, QTableWidgetItem(str(data)))


class QueryCourseDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Query Course Information')
        self.setGeometry(100, 100, 600, 400)
        self.layout = QVBoxLayout()
        
        self.course_id_input = QLineEdit(self)
        self.query_button = QPushButton('Query')
        self.query_button.clicked.connect(self.query_course)
        
        self.layout.addWidget(QLabel('Course ID:'))
        self.layout.addWidget(self.course_id_input)
        self.layout.addWidget(self.query_button)
        
        self.result_table = QTableWidget()
        self.layout.addWidget(self.result_table)
        
        self.setLayout(self.layout)
    
    def query_course(self):
        course_id = self.course_id_input.text()
        
        if not course_id:
            QMessageBox.critical(self, 'Error', 'Course ID is required')
            return
        
        db = Database()
        results = db.query_course_info(course_id)
        
        if not results:
            QMessageBox.information(self, 'No Results', 'No information found for the given Course ID')
            return
        
        self.result_table.setRowCount(0)
        self.result_table.setColumnCount(6)
        self.result_table.setHorizontalHeaderLabels([
            'Course ID', 'Course Name', 'Credits', 'Hours', 'Student ID', 'Student Name'
        ])
        
        for row_number, row_data in enumerate(results):
            self.result_table.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.result_table.setItem(row_number, column_number, QTableWidgetItem(str(data)))

class AddAwardDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Add Award')
        self.setGeometry(100, 100, 400, 300)
        self.layout = QFormLayout()
        
        self.student_id_input = QLineEdit(self)
        self.award_type_input = QComboBox(self)
        self.award_type_input.addItems(["Reward", "Punishment"])
        self.award_name_input = QLineEdit(self)
        self.award_date_input = QLineEdit(self)
        
        self.layout.addRow('Student ID:', self.student_id_input)
        self.layout.addRow('Award Type:', self.award_type_input)
        self.layout.addRow('Award Name:', self.award_name_input)
        self.layout.addRow('Award Date:', self.award_date_input)
        
        self.submit_button = QPushButton('Submit')
        self.submit_button.clicked.connect(self.submit)
        self.layout.addWidget(self.submit_button)
        
        self.setLayout(self.layout)
    
    def submit(self):
        student_id = self.student_id_input.text()
        award_type = self.award_type_input.currentText()
        award_name = self.award_name_input.text()
        award_date = self.award_date_input.text()
        
        db = Database()
        try:
            db.add_award(student_id, award_type, award_name, award_date)
            QMessageBox.information(self, 'Success', 'Award added successfully')
            self.close()
        except ValueError as e:
            QMessageBox.critical(self, 'Error', str(e))

class ViewAwardsDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('View Awards')
        self.setGeometry(100, 100, 600, 400)
        self.layout = QVBoxLayout()
        
        self.result_table = QTableWidget()
        self.layout.addWidget(self.result_table)
        
        self.setLayout(self.layout)
        self.load_awards()
    
    def load_awards(self):
        db = Database()
        awards = db.view_awards()
        
        self.result_table.setRowCount(0)
        self.result_table.setColumnCount(5)
        self.result_table.setHorizontalHeaderLabels([
            'Award ID', 'Student ID', 'Award Type', 'Award Name', 'Award Date'
        ])
        
        for row_number, row_data in enumerate(awards):
            self.result_table.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.result_table.setItem(row_number, column_number, QTableWidgetItem(str(data)))

class StudentManagementSystem(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Student Management System')
        self.setGeometry(100, 100, 800, 600)
        
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.tabs = QTabWidget()
        self.layout.addWidget(self.tabs)
        
        self.student_tab = QWidget()
        self.course_tab = QWidget()
        self.grade_tab = QWidget()
        self.enrollment_tab = QWidget()
        self.award_tab = QWidget()
        
        self.tabs.addTab(self.student_tab, "Students")
        self.tabs.addTab(self.course_tab, "Courses")
        self.tabs.addTab(self.grade_tab, "Grades")
        self.tabs.addTab(self.enrollment_tab, "Enrollments")
        self.tabs.addTab(self.award_tab, "Awards")

        self.init_student_tab()
        self.init_course_tab()
        self.init_grade_tab()
        self.init_enrollment_tab()
        self.init_award_tab()

    def init_student_tab(self):
        student_layout = QVBoxLayout()

        student_buttons = QGroupBox("Student Management")
        student_buttons_layout = QVBoxLayout()
        
        self.add_student_button = QPushButton('Add Student')
        self.update_student_button = QPushButton('Update Student')
        self.view_student_button = QPushButton('View Students')
        self.delete_student_button = QPushButton('Delete Student')
        self.get_student_avg_grade_button = QPushButton('Get Student Average Grade')
        self.query_student_button = QPushButton('Query Student')
        
        student_buttons_layout.addWidget(self.add_student_button)
        student_buttons_layout.addWidget(self.update_student_button)
        student_buttons_layout.addWidget(self.view_student_button)
        student_buttons_layout.addWidget(self.delete_student_button)
        student_buttons_layout.addWidget(self.get_student_avg_grade_button)
        student_buttons_layout.addWidget(self.query_student_button)
        
        student_buttons.setLayout(student_buttons_layout)
        student_layout.addWidget(student_buttons)
        
        self.student_table = QTableWidget()
        student_layout.addWidget(self.student_table)
        
        self.add_student_button.clicked.connect(self.add_student)
        self.update_student_button.clicked.connect(self.update_student)
        self.view_student_button.clicked.connect(self.view_students)
        self.delete_student_button.clicked.connect(self.delete_student)
        self.get_student_avg_grade_button.clicked.connect(self.get_student_avg_grade)
        self.query_student_button.clicked.connect(self.query_student)
        
        self.student_tab.setLayout(student_layout)

    def init_course_tab(self):
        course_layout = QVBoxLayout()

        course_buttons = QGroupBox("Course Management")
        course_buttons_layout = QVBoxLayout()
        
        self.add_course_button = QPushButton('Add Course')
        self.update_course_button = QPushButton('Update Course')
        self.view_courses_button = QPushButton('View Courses')
        self.query_course_button = QPushButton('Query Course')
        
        course_buttons_layout.addWidget(self.add_course_button)
        course_buttons_layout.addWidget(self.update_course_button)
        course_buttons_layout.addWidget(self.view_courses_button)
        course_buttons_layout.addWidget(self.query_course_button)
        
        course_buttons.setLayout(course_buttons_layout)
        course_layout.addWidget(course_buttons)
        
        self.course_table = QTableWidget()
        course_layout.addWidget(self.course_table)
        
        self.add_course_button.clicked.connect(self.add_course)
        self.update_course_button.clicked.connect(self.update_course)
        self.view_courses_button.clicked.connect(self.view_courses)
        self.query_course_button.clicked.connect(self.query_course)
        
        self.course_tab.setLayout(course_layout)

    def init_grade_tab(self):
        grade_layout = QVBoxLayout()

        grade_buttons = QGroupBox("Grade Management")
        grade_buttons_layout = QVBoxLayout()
        
        self.add_course_grade_button = QPushButton('Add Course Grade')
        self.update_course_grade_button = QPushButton('Update Course Grade')
        self.delete_course_grade_button = QPushButton('Delete Course Grade')
        self.view_course_grades_button = QPushButton('View Course Grades')
        
        grade_buttons_layout.addWidget(self.add_course_grade_button)
        grade_buttons_layout.addWidget(self.update_course_grade_button)
        grade_buttons_layout.addWidget(self.delete_course_grade_button)
        grade_buttons_layout.addWidget(self.view_course_grades_button)
        
        grade_buttons.setLayout(grade_buttons_layout)
        grade_layout.addWidget(grade_buttons)
        
        self.grade_table = QTableWidget()
        grade_layout.addWidget(self.grade_table)
        
        self.add_course_grade_button.clicked.connect(self.add_course_grade)
        self.update_course_grade_button.clicked.connect(self.update_course_grade)
        self.delete_course_grade_button.clicked.connect(self.delete_course_grade)
        self.view_course_grades_button.clicked.connect(self.view_course_grades)
        
        self.grade_tab.setLayout(grade_layout)

    def init_enrollment_tab(self):
        enrollment_layout = QVBoxLayout()

        enrollment_buttons = QGroupBox("Enrollment Management")
        enrollment_buttons_layout = QVBoxLayout()
        
        self.enroll_student_button = QPushButton('Enroll Student in Course')
        self.view_enrollments_button = QPushButton('View Enrollments')
        
        enrollment_buttons_layout.addWidget(self.enroll_student_button)
        enrollment_buttons_layout.addWidget(self.view_enrollments_button)
        
        enrollment_buttons.setLayout(enrollment_buttons_layout)
        enrollment_layout.addWidget(enrollment_buttons)
        
        self.enrollment_table = QTableWidget()
        enrollment_layout.addWidget(self.enrollment_table)
        
        self.enroll_student_button.clicked.connect(self.enroll_student)
        self.view_enrollments_button.clicked.connect(self.view_enrollments)
        
        self.enrollment_tab.setLayout(enrollment_layout)

    def init_award_tab(self):
        award_layout = QVBoxLayout()

        award_buttons = QGroupBox("Award Management")
        award_buttons_layout = QVBoxLayout()
        
        self.add_award_button = QPushButton('Add Award')
        self.view_awards_button = QPushButton('View Awards')
        
        award_buttons_layout.addWidget(self.add_award_button)
        award_buttons_layout.addWidget(self.view_awards_button)
        
        award_buttons.setLayout(award_buttons_layout)
        award_layout.addWidget(award_buttons)
        
        self.award_table = QTableWidget()
        award_layout.addWidget(self.award_table)
        
        self.add_award_button.clicked.connect(self.add_award)
        self.view_awards_button.clicked.connect(self.view_awards)
        
        self.award_tab.setLayout(award_layout)

    def add_student(self):
        self.add_student_dialog = AddStudentDialog()
        self.add_student_dialog.exec_()

    def update_student(self):
        self.update_student_dialog = UpdateStudentDialog()
        self.update_student_dialog.exec_()

    def delete_student(self):
        self.delete_student_dialog = DeleteStudentDialog()
        self.delete_student_dialog.exec_()

    def view_students(self):
        db = Database()
        students = db.view_students()
        
        self.student_table.setRowCount(0)
        self.student_table.setColumnCount(6)
        self.student_table.setHorizontalHeaderLabels(['Student ID', 'Name', 'Gender', 'Birthdate', 'Major ID', 'Photo'])
        
        for row_number, row_data in enumerate(students):
            self.student_table.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                if column_number == 5 and data:  # Display the photo
                    photo_label = QLabel()
                    pixmap = QPixmap(data)
                    pixmap = pixmap.scaled(50, 50, Qt.KeepAspectRatio)
                    photo_label.setPixmap(pixmap)
                    self.student_table.setCellWidget(row_number, column_number, photo_label)
                else:
                    self.student_table.setItem(row_number, column_number, QTableWidgetItem(str(data)))

    def add_course(self):
        self.add_course_dialog = AddCourseDialog()
        self.add_course_dialog.exec_()

    def update_course(self):
        self.update_course_dialog = UpdateCourseDialog()
        self.update_course_dialog.exec_()

    def view_courses(self):
        db = Database()
        courses = db.view_courses()
        
        self.course_table.setRowCount(0)
        self.course_table.setColumnCount(4)
        self.course_table.setHorizontalHeaderLabels(['Course ID', 'Course Name', 'Credits', 'Hours'])
        
        for row_number, row_data in enumerate(courses):
            self.course_table.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.course_table.setItem(row_number, column_number, QTableWidgetItem(str(data)))

    def add_course_grade(self):
        self.add_course_grade_dialog = AddCourseGradeDialog()
        self.add_course_grade_dialog.exec_()

    def update_course_grade(self):
        self.update_course_grade_dialog = UpdateCourseGradeDialog()
        self.update_course_grade_dialog.exec_()

    def delete_course_grade(self):
        self.delete_course_grade_dialog = DeleteCourseGradeDialog()
        self.delete_course_grade_dialog.exec_()

    def view_course_grades(self):
        db = Database()
        course_grades = db.view_course_grades()
        
        self.grade_table.setRowCount(0)
        self.grade_table.setColumnCount(5)
        self.grade_table.setHorizontalHeaderLabels(['Grade ID', 'Student ID', 'Course ID', 'Grade', 'Grade Date'])
        
        for row_number, row_data in enumerate(course_grades):
            self.grade_table.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.grade_table.setItem(row_number, column_number, QTableWidgetItem(str(data)))

    def enroll_student(self):
        self.enroll_student_dialog = EnrollStudentDialog()
        self.enroll_student_dialog.exec_()

    def view_enrollments(self):
        db = Database()
        enrollments = db.view_enrollments()
        
        self.enrollment_table.setRowCount(0)
        self.enrollment_table.setColumnCount(4)
        self.enrollment_table.setHorizontalHeaderLabels(['Enrollment ID', 'Student ID', 'Course ID', 'Enrollment Date'])
        
        for row_number, row_data in enumerate(enrollments):
            self.enrollment_table.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.enrollment_table.setItem(row_number, column_number, QTableWidgetItem(str(data)))

    def add_award(self):
        self.add_award_dialog = AddAwardDialog()
        self.add_award_dialog.exec_()

    def view_awards(self):
        self.view_awards_dialog = ViewAwardsDialog()
        self.view_awards_dialog.exec_()

    def query_student(self):
        self.query_student_dialog = QueryStudentDialog()
        self.query_student_dialog.exec_()

    def query_course(self):
        self.query_course_dialog = QueryCourseDialog()
        self.query_course_dialog.exec_()

    def get_student_avg_grade(self):
        student_id, ok = QInputDialog.getText(self, 'Get Average Grade', 'Enter Student ID:')
        if ok:
            db = Database()
            avg_grade = db.get_student_average_grade(student_id)
            print(f"Debug: Average grade for student {student_id} is {avg_grade}")
            if avg_grade is not None:
                QMessageBox.information(self, 'Average Grade', f'The average grade for student {student_id} is {avg_grade:.2f}')
            else:
                QMessageBox.critical(self, 'Error', 'Could not retrieve average grade')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = StudentManagementSystem()
    ex.show()
    sys.exit(app.exec_())
