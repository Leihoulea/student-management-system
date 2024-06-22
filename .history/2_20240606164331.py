import pymysql

class Database:
    def __init__(self):
        self.connection = pymysql.connect(
            host='localhost',
            user='root',
            password='258114',
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
        self.cursor.execute(sql, student_id)
        self.connection.commit()

# Example usage
db = Database()
db.add_student('S001', 'John Doe', 'M', '2000-01-01', 'CS')
students = db.view_students()
print(students)
#db.delete_student('S001')
