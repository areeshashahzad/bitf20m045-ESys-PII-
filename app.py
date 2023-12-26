# app.py
import random
from db import Database
import pymysql
from flask import Flask, render_template, request, redirect, url_for
from flask import Flask, render_template, request, redirect, url_for
from db import get_db_connection
from db import execute_query
from students import Student
db = Database

app = Flask(__name__)

# Sample data for dropdowns (replace with your own data)
CITIES = ["City", "City2", "City3"]
INTERESTS = ["Interest", "Interest2", "Interest3"]
DEPARTMENTS = ["Department", "Department2", "Department3"]
DEGREE_TITLES = ["Associate", "Bachelor", "MPhil", "Post Graduate Diploma", "Doctorate", "Post Doctorate"]

# Routes


# Mock data for the dashboard
def get_mock_data():
    # Replace this with actual data fetching logic from the database
    interests = ['Programming', 'Music', 'Art', 'Sports', 'Reading']
    interest_counts = {interest: random.randint(1, 100) for interest in interests}

    daily_submissions = [random.randint(1, 50) for _ in range(30)]
    age_distribution = {'18-25': 30, '26-30': 40, '31-35': 20, '36-40': 10}
    department_distribution = {'Computer Science': 40, 'Mathematics': 30, 'Physics': 20, 'Chemistry': 10}
    degree_distribution = {'Bachelor': 50, 'Master': 30, 'PhD': 20}
    gender_distribution = {'Male': 60, 'Female': 40}
    daily_activity = [random.randint(1, 20) for _ in range(30)]
    hourly_activity = {'{hour:02}:00': random.randint(1, 10) for hour in range(24)}

    return {
        'top_interests': dict(sorted(interest_counts.items(), key=lambda x: x[1], reverse=True)[:5]),
        'bottom_interests': dict(sorted(interest_counts.items(), key=lambda x: x[1])[:5]),
        'distinct_interests': len(interests),
        'daily_submissions': daily_submissions,
        'age_distribution': age_distribution,
        'department_distribution': department_distribution,
        'degree_distribution': degree_distribution,
        'gender_distribution': gender_distribution,
        'daily_activity': daily_activity,
        'hourly_activity': hourly_activity,
        'students_status_grid': {
            'currently_studying': 500,
            'recently_enrolled': 50,
            'about_to_graduate': 30,
            'graduated': 100
        },
        'most_active_hours': [hour for hour, count in sorted(hourly_activity.items(), key=lambda x: x[1], reverse=True)[:3]],
        'least_active_hours': [hour for hour, count in sorted(hourly_activity.items(), key=lambda x: x[1])[:3]],
        'dead_hours': [hour for hour, count in hourly_activity.items() if count == 0]
    }

@app.route('/')
def dashboard():
    mock_data = get_mock_data()
    return render_template('dashboard.html', data=mock_data)



@app.route('/add_student', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        # Get form data
        full_name = request.form['full_name']
        roll_no = request.form['roll_no']
        email = request.form['email']
        gender = request.form['gender']
        dob = request.form['dob']
        city = request.form['city']
        interest = request.form['interest']
        department = request.form['department']
        degree_title = request.form['degree_title']
        subject = request.form['subject']
        start_date = request.form['start_date']
        end_date = request.form['end_date']

        # Create a Student object
        student = Student(full_name, roll_no, email, gender, dob, city, interest, department, degree_title, subject, start_date, end_date)

        # Save the student data to the database
        student.save_to_db()

        return redirect(url_for('studentlist'))

    # Pass dropdown data to the template
    return render_template('add_student.html', cities=CITIES, interests=INTERESTS, departments=DEPARTMENTS, degree_titles=DEGREE_TITLES)



@app.route('/studentlist')
def studentlist():
    # Fetch all students from the database
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute('SELECT * FROM students')
            students = cursor.fetchall()

    finally:
        connection.close()
    # Pass the student data to the template
    return render_template('studentlist.html', student=students)


# Additional routes for viewing, editing, and deleting a single student

@app.route('/view_student/<int:student_id>')
def view_student(student_id):
    # Fetch the student data from the database
    with db.connection.cursor() as cursor:
        cursor.execute('SELECT * FROM students WHERE id = %s', (student_id,))
        student = cursor.fetchone()

    # Pass the student data to the template
    return render_template('view_student.html', student=student)

@app.route('/edit_student/<int:student_id>', methods=['GET', 'POST'])
def edit_student(student_id):
    if request.method == 'POST':
        # Get form data
        full_name = request.form['full_name']
        roll_no = request.form['roll_no']
        email = request.form['email']
        gender = request.form['gender']
        dob = request.form['dob']
        city = request.form['city']
        interest = request.form['interest']
        department = request.form['department']
        degree_title = request.form['degree_title']
        subject = request.form['subject']
        start_date = request.form['start_date']
        end_date = request.form['end_date']

        # Update the student data in the database
        with db.connection.cursor() as cursor:
            cursor.execute('''
                UPDATE students
                SET full_name=%s, roll_no=%s, email=%s, gender=%s, dob=%s, city=%s,
                    interest=%s, department=%s, degree_title=%s, subject=%s,
                    start_date=%s, end_date=%s
                WHERE id=%s
            ''', (full_name, roll_no, email, gender, dob, city, interest, department, degree_title, subject, start_date, end_date, student_id))
        db.connection.commit()

        return redirect(url_for('studentlist'))

    # Fetch the current student data from the database
    with db.connection.cursor() as cursor:
        cursor.execute('SELECT * FROM students WHERE id = %s', (student_id,))
        student = cursor.fetchone()

    # Pass dropdown data and the student data to the template
    return render_template('edit_student.html', student=student)

@app.route('/delete_student/<int:student_id>')
def delete_student(student_id):
    # Delete the student from the database
    with db.connection.cursor() as cursor:
        cursor.execute('DELETE FROM students WHERE id = %s', (student_id,))
    db.connection.commit()

    return redirect(url_for('studentlist'))

if __name__ == '__main__':
    app.run(debug=True)
