from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QTableWidget, QGroupBox, QPushButton, QTabWidget, QLabel, QInputDialog, QMessageBox, QTableWidgetItem, QLineEdit, QDialog, QFormLayout, QComboBox
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from dialogs import *
from database import Database
import sys
from io import BytesIO  # 用于处理 BLOB 数据

# 登录窗口
class LoginDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Login')
        self.setGeometry(100, 100, 400, 200)
        self.layout = QFormLayout(self)
        
        self.username_edit = QLineEdit(self)
        self.password_edit = QLineEdit(self)
        self.password_edit.setEchoMode(QLineEdit.Password)
        
        self.role_combobox = QComboBox(self)
        self.role_combobox.addItems(['Student', 'Admin'])
        
        self.login_button = QPushButton('Login', self)
        self.login_button.clicked.connect(self.handle_login)
        
        self.layout.addRow('Username:', self.username_edit)
        self.layout.addRow('Password:', self.password_edit)
        self.layout.addRow('Role:', self.role_combobox)
        self.layout.addRow(self.login_button)
        
        self.setLayout(self.layout)
    
    def handle_login(self):
        username = self.username_edit.text()
        password = self.password_edit.text()
        role = self.role_combobox.currentText()
        
        # 在这里添加登录验证逻辑，根据验证结果加载不同的主窗口
        if self.validate_login(username, password, role):
            self.accept()  # Close the login dialog

    def validate_login(self, username, password, role):
        """
        模拟登录验证，实际应用中应连接到数据库或认证服务。
        """
        # 以下是简单的示例，真实场景应有更复杂的验证逻辑
        if role == 'Admin' and username == 'admin' and password == 'admin':
            self.main_window = AdminMainWindow()
            self.main_window.show()
            return True
        elif role == 'Student' and username == 'student' and password == 'student':
            self.main_window = StudentMainWindow()
            self.main_window.show()
            return True
        else:
            QMessageBox.warning(self, 'Error', 'Invalid credentials or role')
            return False

# 学生主窗口
class StudentMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        """
        初始化学生界面，显示与学生相关的功能。
        """
        self.setWindowTitle('Student Dashboard')
        self.setGeometry(100, 100, 800, 600)
        
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)
        
        self.tabs = QTabWidget()
        self.layout.addWidget(self.tabs)
        
        self.student_info_tab = QWidget()
        self.student_courses_tab = QWidget()
        
        self.tabs.addTab(self.student_info_tab, "Student Info")
        self.tabs.addTab(self.student_courses_tab, "Courses")
        
        self.init_student_info_tab()
        self.init_student_courses_tab()

    def init_student_info_tab(self):
        """
        初始化学生信息标签页，显示学生的基本信息。
        """
        student_info_layout = QVBoxLayout()
        
        # 模拟学生信息
        student_info_label = QLabel("Name: John Doe\nGender: M\nBirthdate: 2000-01-01\nMajor: Computer Science")
        student_info_layout.addWidget(student_info_label)
        
        self.student_info_tab.setLayout(student_info_layout)

    def init_student_courses_tab(self):
        """
        初始化课程标签页，显示学生所选课程。
        """
        courses_layout = QVBoxLayout()
        
        self.courses_table = QTableWidget()
        self.courses_table.setRowCount(5)  # Example: 5 courses
        self.courses_table.setColumnCount(4)
        self.courses_table.setHorizontalHeaderLabels(['Course ID', 'Course Name', 'Credits', 'Hours'])
        
        # 模拟课程数据
        example_courses = [
            ('C101', 'Math', 3, 48),
            ('C102', 'Science', 4, 64),
            ('C103', 'History', 2, 32),
            ('C104', 'Literature', 3, 48),
            ('C105', 'Physics', 4, 64)
        ]
        
        for row_number, row_data in enumerate(example_courses):
            for column_number, data in enumerate(row_data):
                self.courses_table.setItem(row_number, column_number, QTableWidgetItem(str(data)))
        
        courses_layout.addWidget(self.courses_table)
        self.student_courses_tab.setLayout(courses_layout)

# 管理员主窗口
class AdminMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        """
        初始化管理员界面，显示与管理员相关的功能。
        """
        self.setWindowTitle('Admin Dashboard')
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
        self.major_tab = QWidget()
        
        self.tabs.addTab(self.student_tab, "Students")
        self.tabs.addTab(self.course_tab, "Courses")
        self.tabs.addTab(self.grade_tab, "Grades")
        self.tabs.addTab(self.enrollment_tab, "Enrollments")
        self.tabs.addTab(self.award_tab, "Awards")
        self.tabs.addTab(self.major_tab, "Majors")

        self.init_student_tab()
        self.init_course_tab()
        self.init_grade_tab()
        self.init_enrollment_tab()
        self.init_award_tab()
        self.init_major_tab()

    def init_student_tab(self):
        """
        初始化学生管理标签页，包括学生的增删改查等操作的按钮和表格。
        """
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
        """
        初始化课程管理标签页，包括课程的增删改查等操作的按钮和表格。
        """
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
        """
        初始化成绩管理标签页，包括课程成绩的增删改查等操作的按钮和表格。
        """
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
        """
        初始化选课管理标签页，包括学生选课的管理操作的按钮和表格。
        """
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
        """
        初始化奖惩管理标签页，包括学生奖惩的管理操作的按钮和表格。
        """
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

    def init_major_tab(self):
        """
        初始化专业管理标签页，包括专业变更和查看的操作的按钮和表格。
        """
        major_layout = QVBoxLayout()

        major_buttons = QGroupBox("Major Management")
        major_buttons_layout = QVBoxLayout()
        
        self.add_major_change_button = QPushButton('Add Major Change')
        self.view_major_changes_button = QPushButton('View Major Changes')
        self.view_majors_button = QPushButton('View Majors')
        
        major_buttons_layout.addWidget(self.add_major_change_button)
        major_buttons_layout.addWidget(self.view_major_changes_button)
        major_buttons_layout.addWidget(self.view_majors_button)
        
        major_buttons.setLayout(major_buttons_layout)
        major_layout.addWidget(major_buttons)
        
        self.major_table = QTableWidget()
        major_layout.addWidget(self.major_table)
        
        self.add_major_change_button.clicked.connect(self.add_major_change)
        self.view_major_changes_button.clicked.connect(self.view_major_changes)
        self.view_majors_button.clicked.connect(self.view_majors)
        
        self.major_tab.setLayout(major_layout)

    def add_student(self):
        """
        打开添加学生的对话框，允许用户输入新学生的信息并将其添加到数据库中。
        """
        self.add_student_dialog = AddStudentDialog()
        self.add_student_dialog.exec_()

    def update_student(self):
        """
        打开更新学生的对话框，允许用户输入现有学生的新信息并更新数据库中的记录。
        """
        self.update_student_dialog = UpdateStudentDialog()
        self.update_student_dialog.exec_()

    def delete_student(self):
        """
        打开删除学生的对话框，允许用户输入学生ID以删除数据库中的相应学生记录。
        """
        self.delete_student_dialog = DeleteStudentDialog()
        self.delete_student_dialog.exec_()

    def view_students(self):
        """
        从数据库中获取所有学生的信息，并在表格中显示这些信息，包括学生的照片。
        """
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
                    pixmap = QPixmap()
                    pixmap.loadFromData(data)  # Load BLOB data directly into QPixmap
                    pixmap = pixmap.scaled(50, 50, Qt.KeepAspectRatio)
                    photo_label.setPixmap(pixmap)
                    self.student_table.setCellWidget(row_number, column_number, photo_label)
                else:
                    self.student_table.setItem(row_number, column_number, QTableWidgetItem(str(data)))

    def add_course(self):
        """
        打开添加课程的对话框，允许用户输入新课程的信息并将其添加到数据库中。
        """
        self.add_course_dialog = AddCourseDialog()
        self.add_course_dialog.exec_()

    def update_course(self):
        """
        打开更新课程的对话框，允许用户输入现有课程的新信息并更新数据库中的记录。
        """
        self.update_course_dialog = UpdateCourseDialog()
        self.update_course_dialog.exec_()

    def view_courses(self):
        """
        从数据库中获取所有课程的信息，并在表格中显示这些信息。
        """
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
        """
        打开添加课程成绩的对话框，允许用户输入学生的课程成绩并将其添加到数据库中。
        """
        self.add_course_grade_dialog = AddCourseGradeDialog()
        self.add_course_grade_dialog.exec_()

    def update_course_grade(self):
        """
        打开更新课程成绩的对话框，允许用户输入现有课程成绩的新信息并更新数据库中的记录。
        """
        self.update_course_grade_dialog = UpdateCourseGradeDialog()
        self.update_course_grade_dialog.exec_()

    def delete_course_grade(self):
        """
        打开删除课程成绩的对话框，允许用户输入成绩ID以删除数据库中的相应成绩记录。
        """
        self.delete_course_grade_dialog = DeleteCourseGradeDialog()
        self.delete_course_grade_dialog.exec_()

    def view_course_grades(self):
        """
        从数据库中获取所有课程成绩的信息，并在表格中显示这些信息。
        """
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
        """
        打开学生选课的对话框，允许用户输入学生ID和课程ID以添加选课记录。
        """
        self.enroll_student_dialog = EnrollStudentDialog()
        self.enroll_student_dialog.exec_()

    def view_enrollments(self):
        """
        从数据库中获取所有选课记录的信息，并在表格中显示这些信息。
        """
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
        """
        打开添加奖惩的对话框，允许用户输入学生的奖惩信息并将其添加到数据库中。
        """
        self.add_award_dialog = AddAwardDialog()
        self.add_award_dialog.exec_()

    def view_awards(self):
        """
        打开查看奖惩的对话框，显示所有学生的奖惩记录。
        """
        self.view_awards_dialog = ViewAwardsDialog()
        self.view_awards_dialog.exec_()

    def query_student(self):
        """
        打开查询学生的对话框，允许用户输入查询条件以检索特定学生的信息。
        """
        self.query_student_dialog = QueryStudentDialog()
        self.query_student_dialog.exec_()

    def query_course(self):
        """
        打开查询课程的对话框，允许用户输入查询条件以检索特定课程的信息。
        """
        self.query_course_dialog = QueryCourseDialog()
        self.query_course_dialog.exec_()

    def add_major_change(self):
        """
        打开添加专业变更的对话框，允许用户输入学生ID、旧专业ID、新专业ID和变更日期，
        并将专业变更记录添加到数据库中。
        """
        student_id, ok1 = QInputDialog.getText(self, 'Add Major Change', 'Enter Student ID:')
        if ok1:
            old_major_id, ok2 = QInputDialog.getText(self, 'Add Major Change', 'Enter Old Major ID:')
            if ok2:
                new_major_id, ok3 = QInputDialog.getText(self, 'Add Major Change', 'Enter New Major ID:')
                if ok3:
                    change_date, ok4 = QInputDialog.getText(self, 'Add Major Change', 'Enter Change Date (YYYY-MM-DD):')
                    if ok4:
                        db = Database()
                        try:
                            db.add_major_change(student_id, old_major_id, new_major_id, change_date)
                            QMessageBox.information(self, 'Success', 'Major change added successfully')
                        except ValueError as e:
                            QMessageBox.critical(self, 'Error', str(e))

    def view_major_changes(self):
        """
        从数据库中获取所有专业变更记录的信息，并在表格中显示这些信息。
        """
        db = Database()
        major_changes = db.view_major_changes()
        
        self.major_table.setRowCount(0)
        self.major_table.setColumnCount(4)
        self.major_table.setHorizontalHeaderLabels(['Change ID', 'Student ID', 'Old Major ID', 'New Major ID', 'Change Date'])
        
        for row_number, row_data in enumerate(major_changes):
            self.major_table.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.major_table.setItem(row_number, column_number, QTableWidgetItem(str(data)))

    def view_majors(self):
        """
        从数据库中获取所有专业的信息，并在表格中显示这些信息。
        """
        db = Database()
        majors = db.view_majors()
        
        self.major_table.setRowCount(0)
        self.major_table.setColumnCount(2)
        self.major_table.setHorizontalHeaderLabels(['Major ID', 'Major Name'])
        
        for row_number, row_data in enumerate(majors):
            self.major_table.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.major_table.setItem(row_number, column_number, QTableWidgetItem(str(data)))

    def get_student_avg_grade(self):
        """
        打开获取学生平均成绩的对话框，允许用户输入学生ID并显示该学生的平均成绩。
        """
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
    """
    程序的入口，创建 QApplication 实例和登录对话框 LoginDialog。
    根据登录结果加载相应的主窗口（学生或管理员）。
    """
    app = QApplication(sys.argv)
    
    login_dialog = LoginDialog()
    if login_dialog.exec_() == QDialog.Accepted:
        sys.exit(app.exec_())
