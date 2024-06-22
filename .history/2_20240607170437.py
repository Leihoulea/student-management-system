from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, 
    QFormLayout, QLineEdit, QDialog, QMessageBox, QFileDialog, QLabel, QInputDialog, QGroupBox, 
    QHBoxLayout, QTabWidget
)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
import pymysql
import sys

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
    
    def view_students(self):
        sql = "SELECT * FROM Students"
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def delete_student(self, student_id):
        sql = "DELETE FROM Students WHERE student_id = %s"
        self.cursor.execute(sql, (student_id,))
        self.connection.commit()

    def add_major_change(self, student_id, old_major_id, new_major_id, change_date):
        # 检查学生当前专业
        sql = "SELECT major_id FROM Students WHERE student_id = %s"
        self.cursor.execute(sql, (student_id,))
        current_major_id = self.cursor.fetchone()
        
        if current_major_id is None:
            raise ValueError("Student ID does not exist")
        
        current_major_id = current_major_id[0]
        
        if current_major_id != old_major_id:
            raise ValueError("The old major ID does not match the current major ID of the student")
        
        if old_major_id == new_major_id:
            raise ValueError("The new major ID cannot be the same as the old major ID")
        
        # 添加专业变更记录
        sql = "INSERT INTO MajorChanges (student_id, old_major_id, new_major_id, change_date) VALUES (%s, %s, %s, %s)"
        self.cursor.execute(sql, (student_id, old_major_id, new_major_id, change_date))
        self.connection.commit()
        
        # 更新学生表中的专业ID
        sql = "UPDATE Students SET major_id = %s WHERE student_id = %s"
        self.cursor.execute(sql, (new_major_id, student_id))
        self.connection.commit()
    def get_student_info(self, student_id):
        # 获取学生个人信息
        sql = "SELECT * FROM Students WHERE student_id = %s"
        self.cursor.execute(sql, (student_id,))
        student_info = self.cursor.fetchone()

        # 获取学生所选课程
        sql = """
        SELECT Courses.course_id, Courses.course_name, Courses.credits, Courses.hours 
        FROM Enrollments 
        JOIN Courses ON Enrollments.course_id = Courses.course_id 
        WHERE Enrollments.student_id = %s
        """
        self.cursor.execute(sql, (student_id,))
        courses = self.cursor.fetchall()

        # 获取学生奖惩记录
        sql = "SELECT * FROM Awards WHERE student_id = %s"
        self.cursor.execute(sql, (student_id,))
        awards = self.cursor.fetchall()

        return student_info, courses, awards

    def get_course_info(self, course_id):
        # 获取课程信息
        sql = "SELECT * FROM Courses WHERE course_id = %s"
        self.cursor.execute(sql, (course_id,))
        course_info = self.cursor.fetchone()

        # 获取选择该课程的学生
        sql = """
        SELECT Students.student_id, Students.name, Students.gender, Students.birthdate, Students.major_id 
        FROM Enrollments 
        JOIN Students ON Enrollments.student_id = Students.student_id 
        WHERE Enrollments.course_id = %s
        """
        self.cursor.execute(sql, (course_id,))
        students = self.cursor.fetchall()

        return course_info, students
    
    def view_major_changes(self):
        sql = "SELECT * FROM MajorChanges"
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def add_award(self, student_id, award_type, award_name, award_date):
        # 检查学生ID是否存在
        sql = "SELECT * FROM Students WHERE student_id = %s"
        self.cursor.execute(sql, (student_id,))
        if not self.cursor.fetchone():
            raise ValueError("Student ID does not exist")
        
        # 检查奖惩是否重复
        sql = "SELECT * FROM Awards WHERE student_id = %s AND award_name = %s AND award_date = %s"
        self.cursor.execute(sql, (student_id, award_name, award_date))
        if self.cursor.fetchone():
            raise ValueError("Award already exists for the given student on the specified date")
        
        sql = "INSERT INTO Awards (student_id, award_type, award_name, award_date) VALUES (%s, %s, %s, %s)"
        self.cursor.execute(sql, (student_id, award_type, award_name, award_date))
        self.connection.commit()

    def view_awards(self):
        sql = "SELECT * FROM Awards"
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def add_course(self, course_id, course_name, credits, hours):
        # 检查课程编号是否重复
        sql = "SELECT * FROM Courses WHERE course_id = %s"
        self.cursor.execute(sql, (course_id,))
        if self.cursor.fetchone():
            raise ValueError("Course ID already exists")
        
        sql = "INSERT INTO Courses (course_id, course_name, credits, hours) VALUES (%s, %s, %s, %s)"
        self.cursor.execute(sql, (course_id, course_name, credits, hours))
        self.connection.commit()
    
    def update_course(self, course_id, course_name, credits, hours):
        # 检查课程编号是否存在
        sql = "SELECT * FROM Courses WHERE course_id = %s"
        self.cursor.execute(sql, (course_id,))
        if not self.cursor.fetchone():
            raise ValueError("Course ID does not exist")
        
        sql = "UPDATE Courses SET course_name = %s, credits = %s, hours = %s WHERE course_id = %s"
        self.cursor.execute(sql, (course_name, credits, hours, course_id))
        self.connection.commit()

    def view_courses(self):
        sql = "SELECT * FROM Courses"
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def add_course_grade(self, student_id, course_id, grade, grade_date):
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

    def view_course_grades(self):
        sql = "SELECT * FROM CourseGrades"
        self.cursor.execute(sql)
        return self.cursor.fetchall()
    
    def enroll_student_in_course(self, student_id, course_id, enrollment_date):
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
        
        # 检查是否已选过该课程
        sql = "SELECT * FROM Enrollments WHERE student_id = %s AND course_id = %s"
        self.cursor.execute(sql, (student_id, course_id))
        if self.cursor.fetchone():
            raise ValueError("Student is already enrolled in this course")
        
        sql = "INSERT INTO Enrollments (student_id, course_id, enrollment_date) VALUES (%s, %s, %s)"
        self.cursor.execute(sql, (student_id, course_id, enrollment_date))
        self.connection.commit()
    
    def view_enrollments(self):
        sql = "SELECT * FROM Enrollments"
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def get_student_average_grade(self, student_id):
        sql = "SELECT GetStudentAverageGrade(%s)"
        self.cursor.execute(sql, (student_id,))
        result = self.cursor.fetchone()
        return result[0] if result else 0.00  # 返回 0.00 如果没有结果

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
        db = Database()
        student_info = db.get_student_info(student_id)[0]  # 获取学生个人信息
        
        if student_info:
            self.show_update_form(student_info)
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

class AddMajorChangeDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Add Major Change')
        self.setGeometry(100, 100, 300, 200)
        self.layout = QFormLayout()
        
        self.student_id_input = QLineEdit(self)
        self.old_major_id_input = QLineEdit(self)
        self.new_major_id_input = QLineEdit(self)
        self.change_date_input = QLineEdit(self)
        
        self.layout.addRow('Student ID:', self.student_id_input)
        self.layout.addRow('Old Major ID:', self.old_major_id_input)
        self.layout.addRow('New Major ID:', self.new_major_id_input)
        self.layout.addRow('Change Date:', self.change_date_input)
        
        self.submit_button = QPushButton('Submit')
        self.submit_button.clicked.connect(self.submit)
        self.layout.addWidget(self.submit_button)
        
        self.setLayout(self.layout)
    
    def submit(self):
        student_id = self.student_id_input.text()
        old_major_id = self.old_major_id_input.text()
        new_major_id = self.new_major_id_input.text()
        change_date = self.change_date_input.text()
        
        db = Database()
        try:
            db.add_major_change(student_id, old_major_id, new_major_id, change_date)
            QMessageBox.information(self, 'Success', 'Major change added successfully')
            self.close()
        except ValueError as e:
            QMessageBox.critical(self, 'Error', str(e))


class AddAwardDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Add Award')
        self.setGeometry(100, 100, 300, 200)
        self.layout = QFormLayout()
        
        self.student_id_input = QLineEdit(self)
        self.award_type_input = QLineEdit(self)
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
        award_type = self.award_type_input.text()
        award_name = self.award_name_input.text()
        award_date = self.award_date_input.text()
        
        db = Database()
        db.add_award(student_id, award_type, award_name, award_date)
        QMessageBox.information(self, 'Success', 'Award added successfully')
        self.close()

class AddCourseDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Add Course')
        self.setGeometry(100, 100, 300, 200)
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
        
        db = Database()
        try:
            db.add_course_grade(student_id, course_id, grade, grade_date)
            QMessageBox.information(self, 'Success', 'Grade added successfully')
            self.close()
        except ValueError as e:
            QMessageBox.critical(self, 'Error', str(e))
            
class UpdateCourseDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Update Course')
        self.setGeometry(100, 100, 300, 200)
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

class EnrollStudentDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Enroll Student in Course')
        self.setGeometry(100, 100, 300, 200)
        self.layout = QFormLayout()
        
        self.student_id_input = QLineEdit(self)
        self.course_id_input = QLineEdit(self)
        self.enrollment_date_input = QLineEdit(self)
        
        self.layout.addRow('Student ID:', self.student_id_input)
        self.layout.addRow('Course ID:', self.course_id_input)
        self.layout.addRow('Enrollment Date:', self.enrollment_date_input)
        
        self.submit_button = QPushButton('Submit')
        self.submit_button.clicked.connect(self.submit)
        self.layout.addWidget(self.submit_button)
        
        self.setLayout(self.layout)
    
    def submit(self):
        student_id = self.student_id_input.text()
        course_id = self.course_id_input.text()
        enrollment_date = self.enrollment_date_input.text()
        
        db = Database()
        try:
            db.enroll_student_in_course(student_id, course_id, enrollment_date)
            QMessageBox.information(self, 'Success', 'Student enrolled in course successfully')
            self.close()
        except ValueError as e:
            QMessageBox.critical(self, 'Error', str(e))

class QueryStudentDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Query Student')
        self.setGeometry(100, 100, 300, 200)
        self.layout = QFormLayout()
        
        self.student_id_input = QLineEdit(self)
        
        self.layout.addRow('Student ID:', self.student_id_input)
        
        self.submit_button = QPushButton('Submit')
        self.submit_button.clicked.connect(self.submit)
        self.layout.addWidget(self.submit_button)
        
        self.setLayout(self.layout)
    
    def submit(self):
        student_id = self.student_id_input.text()
        
        db = Database()
        try:
            student_info, courses, awards = db.get_student_info(student_id)
            if student_info:
                info = f"Student Info:\nID: {student_info[0]}\nName: {student_info[1]}\nGender: {student_info[2]}\nBirthdate: {student_info[3]}\nMajor ID: {student_info[4]}\n"
                info += "\nCourses:\n"
                for course in courses:
                    info += f"ID: {course[0]}, Name: {course[1]}, Credits: {course[2]}, Hours: {course[3]}\n"
                info += "\nAwards:\n"
                for award in awards:
                    info += f"ID: {award[0]}, Type: {award[2]}, Name: {award[3]}, Date: {award[4]}\n"
                QMessageBox.information(self, 'Student Information', info)
            else:
                QMessageBox.information(self, 'Error', 'Student ID does not exist')
        except ValueError as e:
            QMessageBox.critical(self, 'Error', str(e))


class QueryCourseDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Query Course')
        self.setGeometry(100, 100, 300, 200)
        self.layout = QFormLayout()
        
        self.course_id_input = QLineEdit(self)
        
        self.layout.addRow('Course ID:', self.course_id_input)
        
        self.submit_button = QPushButton('Submit')
        self.submit_button.clicked.connect(self.submit)
        self.layout.addWidget(self.submit_button)
        
        self.setLayout(self.layout)
    
    def submit(self):
        course_id = self.course_id_input.text()
        
        db = Database()
        try:
            course_info, students = db.get_course_info(course_id)
            if course_info:
                info = f"Course Info:\nID: {course_info[0]}\nName: {course_info[1]}\nCredits: {course_info[2]}\nHours: {course_info[3]}\n"
                info += "\nStudents:\n"
                for student in students:
                    info += f"ID: {student[0]}, Name: {student[1]}, Gender: {student[2]}, Birthdate: {student[3]}, Major ID: {student[4]}\n"
                QMessageBox.information(self, 'Course Information', info)
            else:
                QMessageBox.information(self, 'Error', 'Course ID does not exist')
        except ValueError as e:
            QMessageBox.critical(self, 'Error', str(e))
class StudentManagementSystem(QMainWindow):
    def __init__(self):
        super().__init__()
        try:
            self.initUI()
        except Exception as e:
            print(f"Error initializing UI: {e}")

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
        
        self.tabs.addTab(self.student_tab, "Students")
        self.tabs.addTab(self.course_tab, "Courses")
        self.tabs.addTab(self.grade_tab, "Grades")

        self.init_student_tab()
        self.init_course_tab()
        self.init_grade_tab()

    def init_student_tab(self):
        student_layout = QVBoxLayout()

        student_buttons = QGroupBox("Student Management")
        student_buttons_layout = QVBoxLayout()
        
        self.add_student_button = QPushButton('Add Student')
        self.update_student_button = QPushButton('Update Student')
        self.view_student_button = QPushButton('View Students')
        self.delete_student_button = QPushButton('Delete Student')
        self.get_student_avg_grade_button = QPushButton('Get Student Average Grade')
        
        student_buttons_layout.addWidget(self.add_student_button)
        student_buttons_layout.addWidget(self.update_student_button)
        student_buttons_layout.addWidget(self.view_student_button)
        student_buttons_layout.addWidget(self.delete_student_button)
        student_buttons_layout.addWidget(self.get_student_avg_grade_button)
        
        student_buttons.setLayout(student_buttons_layout)
        student_layout.addWidget(student_buttons)
        
        self.student_table = QTableWidget()
        student_layout.addWidget(self.student_table)
        
        self.add_student_button.clicked.connect(self.add_student)
        self.update_student_button.clicked.connect(self.update_student)
        self.view_student_button.clicked.connect(self.view_students)
        self.delete_student_button.clicked.connect(self.delete_student)
        self.get_student_avg_grade_button.clicked.connect(self.get_student_avg_grade)
        
        self.student_tab.setLayout(student_layout)

    def init_course_tab(self):
        course_layout = QVBoxLayout()

        course_buttons = QGroupBox("Course Management")
        course_buttons_layout = QVBoxLayout()
        
        self.add_course_button = QPushButton('Add Course')
        self.update_course_button = QPushButton('Update Course')
        self.view_courses_button = QPushButton('View Courses')
        
        course_buttons_layout.addWidget(self.add_course_button)
        course_buttons_layout.addWidget(self.update_course_button)
        course_buttons_layout.addWidget(self.view_courses_button)
        
        course_buttons.setLayout(course_buttons_layout)
        course_layout.addWidget(course_buttons)
        
        self.course_table = QTableWidget()
        course_layout.addWidget(self.course_table)
        
        self.add_course_button.clicked.connect(self.add_course)
        self.update_course_button.clicked.connect(self.update_course)
        self.view_courses_button.clicked.connect(self.view_courses)
        
        self.course_tab.setLayout(course_layout)

    def init_grade_tab(self):
        grade_layout = QVBoxLayout()

        grade_buttons = QGroupBox("Grade Management")
        grade_buttons_layout = QVBoxLayout()
        
        self.add_course_grade_button = QPushButton('Add Course Grade')
        self.view_course_grades_button = QPushButton('View Course Grades')
        
        grade_buttons_layout.addWidget(self.add_course_grade_button)
        grade_buttons_layout.addWidget(self.view_course_grades_button)
        
        grade_buttons.setLayout(grade_buttons_layout)
        grade_layout.addWidget(grade_buttons)
        
        self.grade_table = QTableWidget()
        grade_layout.addWidget(self.grade_table)
        
        self.add_course_grade_button.clicked.connect(self.add_course_grade)
        self.view_course_grades_button.clicked.connect(self.view_course_grades)
        
        self.grade_tab.setLayout(grade_layout)

    def add_student(self):
        self.add_student_dialog = AddStudentDialog()
        self.add_student_dialog.exec_()

    def update_student(self):
        self.update_student_dialog = UpdateStudentDialog()
        self.update_student_dialog.exec_()

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

    def delete_student(self):
        student_id, ok = QInputDialog.getText(self, 'Delete Student', 'Enter Student ID:')
        if ok:
            db = Database()
            try:
                db.delete_student(student_id)
                QMessageBox.information(self, 'Success', 'Student deleted successfully')
            except ValueError as e:
                QMessageBox.critical(self, 'Error', str(e))

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
    ex.show()  # 确保主窗口被显示
    sys.exit(app.exec_())