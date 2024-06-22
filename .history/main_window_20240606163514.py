import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, QLineEdit, QLabel

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
        
        # Add buttons and table for student management
        self.add_student_button = QPushButton('Add Student')
        self.view_student_button = QPushButton('View Students')
        self.delete_student_button = QPushButton('Delete Student')
        
        self.layout.addWidget(self.add_student_button)
        self.layout.addWidget(self.view_student_button)
        self.layout.addWidget(self.delete_student_button)
        
        self.student_table = QTableWidget()
        self.layout.addWidget(self.student_table)
        
        # Connect buttons to functions
        self.add_student_button.clicked.connect(self.add_student)
        self.view_student_button.clicked.connect(self.view_students)
        self.delete_student_button.clicked.connect(self.delete_student)
        
        self.show()

    def add_student(self):
        # Function to add student
        pass

    def view_students(self):
        # Function to view students
        pass

    def delete_student(self):
        # Function to delete student
        pass

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = StudentManagementSystem()
    sys.exit(app.exec_())
