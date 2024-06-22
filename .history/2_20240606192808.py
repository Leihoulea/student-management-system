import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QTableWidget, 
                             QTableWidgetItem, QLineEdit, QLabel, QFormLayout, QDialog, QMessageBox, 
                             QInputDialog, QComboBox)
import pymysql

class Database:
    def __init__(self):
        self.connection = pymysql.connect(
            host='localhost',
            user='root',
            password='258114',  # 请替换为你的MySQL密码
            db='StudentManagement'
        )
        self.cursor = self.connection.cursor()
    
    def add_student(self, student_id, name, gender, birthdate, major_id):
        sql = "INSERT INTO Students (student_id, name, gender, birthdate, major_id) VALUES (%s, %s, %s, %s, %s)"
        self.cursor.execute(sql, (student_id, name, gender, birthdate, major_id))
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
        
        sql = "INSERT INTO Awards (student_id, award_type, award_name, award_date) VALUES (%s, %s, %s, %s)"
        self.cursor.execute(sql, (student_id, award_type, award_name, award_date))
        self.connection.commit()

    def view_awards(self):
        sql = "SELECT * FROM Awards"
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def add_course(self, course_id, course_name, credits, hours):
        sql = "INSERT INTO Courses (course_id, course_name, credits, hours) VALUES (%s, %s, %s, %s)"
        self.cursor.execute(sql, (course_id, course_name, credits, hours))
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
        
        sql = "INSERT INTO CourseGrades (student_id, course_id, grade, grade_date) VALUES (%s, %s, %s, %s)"
        self.cursor.execute(sql, (student_id, course_id, grade, grade_date))
        self.connection.commit()

    def view_course_grades(self):
        sql = "SELECT * FROM CourseGrades"
        self.cursor.execute(sql)
        return self.cursor.fetchall()


class AddStudentDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Add Student')
        self.setGeometry(100, 100, 300, 200)
        self.layout = QFormLayout()
        
        self.student_id_input = QLineEdit(self)
        self.name_input = QLineEdit(self)
        self.gender_input = QLineEdit(self)
        self.birthdate_input = QLineEdit(self)
        self.major_id_input = QLineEdit(self)
        
        self.layout.addRow('Student ID:', self.student_id_input)
        self.layout.addRow('Name:', self.name_input)
        self.layout.addRow('Gender:', self.gender_input)
        self.layout.addRow('Birthdate:', self.birthdate_input)
        self.layout.addRow('Major ID:', self.major_id_input)
        
        self.submit_button = QPushButton('Submit')
        self.submit_button.clicked.connect(self.submit)
        self.layout.addWidget(self.submit_button)
        
        self.setLayout(self.layout)
    
    def submit(self):
        student_id = self.student_id_input.text()
        name = self.name_input.text()
        gender = self.gender_input.text()
        birthdate = self.birthdate_input.text()
        major_id = self.major_id_input.text()
        
        db = Database()
        db.add_student(student_id, name, gender, birthdate, major_id)
        QMessageBox.information(self, 'Success', 'Student added successfully')
        self.close()

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
        db.add_course(course_id, course_name, credits, hours)
        QMessageBox.information(self, 'Success', 'Course added successfully')
        self.close()

class AddCourseGradeDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Add Course Grade')
        self.setGeometry(100, 100, 300, 200)
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
        
        db = Database()
        db.add_course_grade(student_id, course_id, grade, grade_date)
        QMessageBox.information(self, 'Success', 'Course grade added successfully')
        self.close()

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
        
        self.add_student_button = QPushButton('Add Student')
        self.view_student_button = QPushButton('View Students')
        self.delete_student_button = QPushButton('Delete Student')
        self.add_major_change_button = QPushButton('Add Major Change')
        self.view_major_changes_button = QPushButton('View Major Changes')
        self.add_award_button = QPushButton('Add Award')
        self.view_awards_button = QPushButton('View Awards')
        self.add_course_button = QPushButton('Add Course')
        self.view_courses_button = QPushButton('View Courses')
        self.add_course_grade_button = QPushButton('Add Course Grade')
        self.view_course_grades_button = QPushButton('View Course Grades')
        
        self.layout.addWidget(self.add_student_button)
        self.layout.addWidget(self.view_student_button)
        self.layout.addWidget(self.delete_student_button)
        self.layout.addWidget(self.add_major_change_button)
        self.layout.addWidget(self.view_major_changes_button)
        self.layout.addWidget(self.add_award_button)
        self.layout.addWidget(self.view_awards_button)
        self.layout.addWidget(self.add_course_button)
        self.layout.addWidget(self.view_courses_button)
        self.layout.addWidget(self.add_course_grade_button)
        self.layout.addWidget(self.view_course_grades_button)
        
        self.student_table = QTableWidget()
        self.layout.addWidget(self.student_table)
        
        self.add_student_button.clicked.connect(self.add_student)
        self.view_student_button.clicked.connect(self.view_students)
        self.delete_student_button.clicked.connect(self.delete_student)
        self.add_major_change_button.clicked.connect(self.add_major_change)
        self.view_major_changes_button.clicked.connect(self.view_major_changes)
        self.add_award_button.clicked.connect(self.add_award)
        self.view_awards_button.clicked.connect(self.view_awards)
        self.add_course_button.clicked.connect(self.add_course)
        self.view_courses_button.clicked.connect(self.view_courses)
        self.add_course_grade_button.clicked.connect(self.add_course_grade)
        self.view_course_grades_button.clicked.connect(self.view_course_grades)
        
        self.show()

    def add_student(self):
        self.add_student_dialog = AddStudentDialog()
        self.add_student_dialog.exec_()

    def view_students(self):
        db = Database()
        students = db.view_students()
        
        self.student_table.setRowCount(0)
        self.student_table.setColumnCount(5)
        self.student_table.setHorizontalHeaderLabels(['Student ID', 'Name', 'Gender', 'Birthdate', 'Major ID'])
        
        for row_number, row_data in enumerate(students):
            self.student_table.insertRow(row_number)
            for column_number, data in enumerate(row_data):
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

    def add_major_change(self):
        self.add_major_change_dialog = AddMajorChangeDialog()
        self.add_major_change_dialog.exec_()

    def view_major_changes(self):
        db = Database()
        major_changes = db.view_major_changes()
        
        self.student_table.setRowCount(0)
        self.student_table.setColumnCount(5)
        self.student_table.setHorizontalHeaderLabels(['Change ID', 'Student ID', 'Old Major ID', 'New Major ID', 'Change Date'])
        
        for row_number, row_data in enumerate(major_changes):
            self.student_table.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.student_table.setItem(row_number, column_number, QTableWidgetItem(str(data)))

    def add_award(self):
        self.add_award_dialog = AddAwardDialog()
        self.add_award_dialog.exec_()

    def view_awards(self):
        db = Database()
        awards = db.view_awards()
        
        self.student_table.setRowCount(0)
        self.student_table.setColumnCount(5)
        self.student_table.setHorizontalHeaderLabels(['Award ID', 'Student ID', 'Award Type', 'Award Name', 'Award Date'])
        
        for row_number, row_data in enumerate(awards):
            self.student_table.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.student_table.setItem(row_number, column_number, QTableWidgetItem(str(data)))

    def add_course(self):
        self.add_course_dialog = AddCourseDialog()
        self.add_course_dialog.exec_()

    def view_courses(self):
        db = Database()
        courses = db.view_courses()
        
        self.student_table.setRowCount(0)
        self.student_table.setColumnCount(4)
        self.student_table.setHorizontalHeaderLabels(['Course ID', 'Course Name', 'Credits', 'Hours'])
        
        for row_number, row_data in enumerate(courses):
            self.student_table.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.student_table.setItem(row_number, column_number, QTableWidgetItem(str(data)))

    def add_course_grade(self):
        self.add_course_grade_dialog = AddCourseGradeDialog()
        self.add_course_grade_dialog.exec_()

    def view_course_grades(self):
        db = Database()
        course_grades = db.view_course_grades()
        
        self.student_table.setRowCount(0)
        self.student_table.setColumnCount(5)
        self.student_table.setHorizontalHeaderLabels(['Grade ID', 'Student ID', 'Course ID', 'Grade', 'Grade Date'])
        
        for row_number, row_data in enumerate(course_grades):
            self.student_table.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.student_table.setItem(row_number, column_number, QTableWidgetItem(str(data)))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = StudentManagementSystem()
    sys.exit(app.exec_())
