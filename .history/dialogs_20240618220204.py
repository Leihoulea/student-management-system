# dialogs.py

from PyQt5.QtWidgets import (
    QDialog, QFormLayout, QLineEdit, QPushButton, QFileDialog, QMessageBox, QComboBox, QLabel, QTableWidget, QTableWidgetItem, QVBoxLayout, QInputDialog
)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt  # 添加这个导入
import re
from datetime import datetime
from database import Database


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
    
        # 显示照片
        self.photo_label = QLabel(self)
        pixmap = QPixmap()
    
        if student_info[5]:  # 检查是否有照片数据
            pixmap.loadFromData(student_info[5])  # 从 BLOB 数据加载图片
            pixmap = pixmap.scaled(100, 100, Qt.KeepAspectRatio)  # 调整图片大小
        self.photo_label.setPixmap(pixmap)
    
        self.layout.addRow('Name:', self.name_input)
        self.layout.addRow('Gender:', self.gender_input)
        self.layout.addRow('Birthdate:', self.birthdate_input)
        self.layout.addRow('Photo:', self.photo_label)  # 添加照片标签到布局
    
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
        
        # 获取学生详细信息并显示
        choice, ok = QInputDialog.getItem(
            self, "Select Information", "Select the information to view:",
            ["Personal Information", "Enrolled Courses", "Course Grades", "Awards", "Major Changes"], 0, False
        )
        if ok and choice:
            if choice == "Personal Information":
                self.display_student_info(student_info)
            elif choice == "Enrolled Courses":
                self.display_student_courses(student_id)
            elif choice == "Course Grades":
                self.display_student_grades(student_id)
            elif choice == "Awards":
                self.display_student_awards(student_id)
            elif choice == "Major Changes":
                self.display_student_major_changes(student_id)
    
    def display_student_info(self, student_info):
        self.result_table.setRowCount(1)
        self.result_table.setColumnCount(6)
        self.result_table.setHorizontalHeaderLabels(['Student ID', 'Name', 'Gender', 'Birthdate', 'Major ID', 'Photo'])
        
        row_data = student_info[0]
        for column_number, data in enumerate(row_data):
            if column_number == 5 and data:  # Display the photo
                photo_label = QLabel()
                pixmap = QPixmap(data)
                pixmap = pixmap.scaled(50, 50, Qt.KeepAspectRatio)
                photo_label.setPixmap(pixmap)
                self.result_table.setCellWidget(0, column_number, photo_label)
            else:
                self.result_table.setItem(0, column_number, QTableWidgetItem(str(data)))
    
    def display_student_courses(self, student_id):
        db = Database()
        sql = """
        SELECT C.course_id, C.course_name, C.credits, C.hours
        FROM Enrollments E
        JOIN Courses C ON E.course_id = C.course_id
        WHERE E.student_id = %s
        """
        db.cursor.execute(sql, (student_id,))
        results = db.cursor.fetchall()
        
        self.result_table.setRowCount(0)
        self.result_table.setColumnCount(4)
        self.result_table.setHorizontalHeaderLabels(['Course ID', 'Course Name', 'Credits', 'Hours'])
        
        for row_number, row_data in enumerate(results):
            self.result_table.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.result_table.setItem(row_number, column_number, QTableWidgetItem(str(data)))
    
    def display_student_grades(self, student_id):
        db = Database()
        sql = """
        SELECT G.course_id, C.course_name, G.grade, G.grade_date
        FROM CourseGrades G
        JOIN Courses C ON G.course_id = C.course_id
        WHERE G.student_id = %s
        """
        db.cursor.execute(sql, (student_id,))
        results = db.cursor.fetchall()
        
        self.result_table.setRowCount(0)
        self.result_table.setColumnCount(4)
        self.result_table.setHorizontalHeaderLabels(['Course ID', 'Course Name', 'Grade', 'Grade Date'])
        
        for row_number, row_data in enumerate(results):
            self.result_table.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.result_table.setItem(row_number, column_number, QTableWidgetItem(str(data)))
    
    def display_student_awards(self, student_id):
        db = Database()
        sql = """
        SELECT award_type, award_name, award_date
        FROM Awards
        WHERE student_id = %s
        """
        db.cursor.execute(sql, (student_id,))
        results = db.cursor.fetchall()
        
        self.result_table.setRowCount(0)
        self.result_table.setColumnCount(3)
        self.result_table.setHorizontalHeaderLabels(['Award Type', 'Award Name', 'Award Date'])
        
        for row_number, row_data in enumerate(results):
            self.result_table.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.result_table.setItem(row_number, column_number, QTableWidgetItem(str(data)))
    
    def display_student_major_changes(self, student_id):
        db = Database()
        sql = """
        SELECT change_id, old_major_id, new_major_id, change_date
        FROM MajorChanges
        WHERE student_id = %s
        """
        db.cursor.execute(sql, (student_id,))
        results = db.cursor.fetchall()
        
        self.result_table.setRowCount(0)
        self.result_table.setColumnCount(4)
        self.result_table.setHorizontalHeaderLabels(['Change ID', 'Old Major ID', 'New Major ID', 'Change Date'])
        
        for row_number, row_data in enumerate(results):
            self.result_table.insertRow(row_number)
            for column_number, data in enumerate(row_data):
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


class DeleteCourseDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        """
        初始化删除课程对话框的界面，包含一个输入框和一个删除按钮。
        """
        self.setWindowTitle('Delete Course')
        self.setGeometry(100, 100, 300, 100)
        
        self.layout = QVBoxLayout()
        
        self.course_id_edit = QLineEdit(self)
        self.course_id_edit.setPlaceholderText("Enter Course ID (e.g., C001)")
        self.layout.addWidget(self.course_id_edit)
        
        self.delete_button = QPushButton('Delete Course', self)
        self.delete_button.clicked.connect(self.delete_course)
        self.layout.addWidget(self.delete_button)
        
        self.setLayout(self.layout)

    def delete_course(self):
        """
        调用数据库方法删除课程，并显示成功或错误的提示信息。
        """
        course_id = self.course_id_edit.text()
        db = Database()
        
        try:
            db.delete_course(course_id)
            QMessageBox.information(self, 'Success', 'Course deleted successfully')
            self.accept()  # Close the dialog
        except ValueError as e:
            QMessageBox.critical(self, 'Error', str(e))
        finally:
            db.close_connection()
