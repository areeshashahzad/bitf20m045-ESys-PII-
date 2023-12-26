import pymysql

def connect_db():
    return pymysql.connect(
        host='localhost',
        user='root',
        password='shamoon',
        database='studentsdata',
    )

def execute_query(query, params=None, fetchall=False):
    connection = connect_db()
    try:
        with connection.cursor() as cursor:
            cursor.execute(query, params)
            result = cursor.fetchall() if fetchall else cursor.fetchone()
        return result
    finally:
        connection.close()

def get_db_connection():
    return connect_db()




class Database:
    connection = None

    def __init__(self):
        self.connection = pymysql.connect(
            host='localhost', user='root', password='shamoon', database='studentsdata')
        self.create_tables()
        self.insert_dummy_data()  # Call this method to insert dummy data

    def create_tables(self):
        with self.connection.cursor() as cursor:
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS students (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    full_name VARCHAR(255),
                    roll_no VARCHAR(20),
                    email VARCHAR(255),
                    gender VARCHAR(10),
                    dob DATE,
                    city VARCHAR(50),
                    interest VARCHAR(50),
                    department VARCHAR(50),
                    degree_title VARCHAR(50),
                    subject VARCHAR(255),
                    start_date DATE,
                    end_date DATE
                )
            ''')
        self.connection.commit()

    def insert_dummy_data(self):
        return

    def get_all_students(self):
        with self.connection.cursor() as cursor:
            cursor.execute('SELECT * FROM students')
            return cursor.fetchall()

    def get_student_by_id(self, student_id):
        with self.connection.cursor() as cursor:
            cursor.execute('SELECT * FROM students WHERE id = %s', (student_id,))
            return cursor.fetchone()

    def update_student(self, student_id, full_name, roll_no, email, gender, dob, city, interest, department, degree_title, subject, start_date, end_date):
        with self.connection.cursor() as cursor:
            cursor.execute('UPDATE students SET full_name=%s, roll_no=%s, email=%s, gender=%s, dob=%s, city=%s,interest=%s, department=%s, degree_title=%s, subject=%s,start_date=%s, end_date=%s WHERE id=%s', (full_name, roll_no, email, gender, dob, city, interest, department, degree_title, subject, start_date, end_date, student_id))
        self.connection.commit()

    def delete_student(self, student_id):
        with self.connection.cursor() as cursor:
            cursor.execute('DELETE FROM students WHERE id = %s', (student_id,))
        self.connection.commit()

# Create an instance of the Database class
db = Database()
