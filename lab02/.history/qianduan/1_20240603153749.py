import mysql.connector
from mysql.connector import Error

def add_student(name, gender, major_id, birthdate):
    try:
        # 连接到MySQL数据库
        connection = mysql.connector.connect(
            host='your_host',         # 数据库服务器地址
            user='your_username',     # 数据库用户名
            password='your_password', # 数据库密码
            database='your_database'  # 数据库名
        )
        if connection.is_connected():
            cursor = connection.cursor()
            # 创建插入SQL语句
            query = """
            INSERT INTO students (name, gender, major_id, birthdate) 
            VALUES (%s, %s, %s, %s)
            """
            # 执行SQL语句
            cursor.execute(query, (name, gender, major_id, birthdate))
            connection.commit()  # 提交事务
            print("Student added successfully.")
    except Error as e:
        print("Error while connecting to MySQL", e)
    finally:
        # 关闭数据库连接
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")

# 示例：添加一个学生
add_student('John Doe', 'M', 1, '2000-01-01')
