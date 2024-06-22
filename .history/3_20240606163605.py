# In StudentManagementSystem class

def add_student(self):
    student_id = QLineEdit('Enter Student ID')
    name = QLineEdit('Enter Name')
    gender = QLineEdit('Enter Gender')
    birthdate = QLineEdit('Enter Birthdate')
    major_id = QLineEdit('Enter Major ID')
    
    # Collect data and add to database
    db = Database()
    db.add_student(student_id.text(), name.text(), gender.text(), birthdate.text(), major_id.text())

def view_students(self):
    db = Database()
    students = db.view_students()
    
    self.student_table.setRowCount(0)
    for row_number, row_data in enumerate(students):
        self.student_table.insertRow(row_number)
        for column_number, data in enumerate(row_data):
            self.student_table.setItem(row_number, column_number, QTableWidgetItem(str(data)))

def delete_student(self):
    student_id = QLineEdit('Enter Student ID')
    
    db = Database()
    db.delete_student(student_id.text())
