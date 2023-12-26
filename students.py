# student_class.py
from db import execute_query

class Student:
    def __init__(self, full_name, roll_no, email, gender, dob, city, interest, department, degree_title, subject, start_date, end_date):
        self.full_name = full_name
        self.roll_no = roll_no
        self.email = email
        self.gender = gender
        self.dob = dob
        self.city = city
        self.interest = interest
        self.department = department
        self.degree_title = degree_title
        self.subject = subject
        self.start_date = start_date
        self.end_date = end_date

    def save_to_db(self):
        query = "INSERT INTO students (full_name, roll_no, email, gender, dob, city, interest, department, degree_title, subject, start_date, end_date)VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        params = (
            self.full_name, self.roll_no, self.email, self.gender, self.dob, self.city,
            self.interest, self.department, self.degree_title, self.subject, self.start_date, self.end_date
        )

        execute_query(query, params)

    def get_student_by_id(cls, id):
        query = 'SELECT * FROM students WHERE id = %s'
        result = execute_query(query, (id,), fetchall=False)
        if result:
            return cls
        return None
