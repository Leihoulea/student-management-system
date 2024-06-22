import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QTableWidget, 
                             QTableWidgetItem, QLineEdit, QLabel, QFormLayout, QDialog, QMessageBox, 
                             QInputDialog)
import pymysql

class Database:
    def __init__(self):
        self.connection = pymysql.connect(
            host='localhost',
            user='root',
            password='your_password_here',  # 请替换为你的MySQL密码
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
        
        self.layout.addWidget(self.add_student_button)
        self.layout.addWidget(self.view_student_button)
        self.layout.addWidget(self.delete_student_button)
        
        self.student_table = QTableWidget()
        self.layout.addWidget(self.student_table)
        
        self.add_student_button.clicked.connect(self.add_student)
        self.view_student_button.clicked.connect(self.view_students)
        self.delete_student_button.clicked.connect(self.delete_student)
        
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
            db.delete_student(student_id)
            QMessageBox.information(self, 'Success', 'Student deleted successfully')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = StudentManagementSystem()
    sys.exit(app.exec_())
