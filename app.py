import json
import logging
import os
import pandas as pd
import sys

from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from pandas.io.json import json_normalize
from urllib.request import urlopen

from db_book import *
from logging.config import dictConfig

app = Flask('w12hw')
app.logger.setLevel(logging.INFO)

print(os.getcwd())
os.chdir('c:/Users/silaz/github/capstone/is211/w12')

@app.route('/', methods=['POST', 'GET'])
def home():
    app.logger.info("In home, redirect to loging")
    return redirect(url_for('login'))

@app.route('/login', methods=['POST', 'GET'])
def login():
    app.logger.info('in login, before db')
    dbHandle = db_work.getHandle()
    app.logger.info(f"Got conn handle {dbHandle}")
    db_work.createDB(dbHandle)
    cursor = dbHandle.cursor()
    app.logger.info("after create and cursor")
    cursor.execute("SELECT count(*) from students where first_name = ?", ('John',))
    john_cnt = cursor.fetchall()[0][0]
    if john_cnt == 0:
        #app.logger.info("Don't load test data")
        db_work.load_test_data(dbHandle)
    app.logger.info(john_cnt)

    if request.method == 'POST':
        app.logger.info("Getting posted data")
        user = request.form['username']
        pw = request.form['password']
        app.logger.info(f"The user is {user}")
        #TO DO, check for user

        if user == 'admin' and pw == 'password':
            app.logger.info("redirect to dashboard")
            return redirect(url_for('dashboard'))
        else:
            app.logger.info('error')
            error = 'ERROR: username or password is incorrect.'
            return render_template('index.html', error = error)
    else:
        app.logger.info("Loading index.html")
        return render_template('index.html')

@app.route('/dashboard', methods=['POST', 'GET'])
def dashboard():
    dbHandle = db_work.getHandle()
    if request.method == 'POST':
        pass
    if request.method == 'GET':
        students_df = pd.read_sql_query("select * from students;", dbHandle)
        students_df['href'] = students_df.apply(lambda row: '<a href="/student/' + str(row.id) + '">Student Report</a>', axis=1)
        quizzes_df = pd.read_sql_query("select * from quizzes;", dbHandle)
        return render_template('dashboard.html', tables=[students_df.to_html(escape=False), quizzes_df.to_html()], titles=['na', 'students', 'quizzes'])

@app.route('/student/add', methods=['POST', 'GET'])
def add_student():
    dbHandle = db_work.getHandle()
    if request.method == 'POST':
        first_name  = request.form['first_name']
        last_name = request.form['last_name']
        row_count = db_work.insertStudent(first_name, last_name, dbHandle)
        app.logger.info(f"Row count for insert is {row_count}")
        if row_count == 1:
            return redirect(url_for('dashboard'))
        else:
            error = "Failed to insert into db"
            return redirect(url_for('student/add'), error = error)

    if request.method == 'GET':
        return render_template('add_student.html')

@app.route('/student/<student_id>', methods=['POST', 'GET'])
def report_student(student_id):
    dbHandle = db_work.getHandle()
    if request.method == 'POST':
        pass
    if request.method == 'GET':
        q = "select r.score, s.first_name, s.last_name, q.subject from student_results r, quizzes q, students s where r.student_id=s.id and r.quiz_id=q.id and s.id = ?"
        students_results_df = pd.read_sql_query(q, con=dbHandle, params={student_id})

        return render_template('student_results.html', tables=[students_results_df.to_html(escape=False)], titles=['na', 'Student', 'quizzes'])

@app.route('/quiz/add', methods=['POST', 'GET'])
def add_quiz():
    dbHandle = db_work.getHandle()
    if request.method == 'POST':
        subject  = request.form['subject']
        num_questions = request.form['questions']
        quiz_date = request.form['quiz_date']
        row_count = db_work.addQuiz(subject, num_questions, quiz_date, dbHandle)
        app.logger.info(f"Row count for insert is {row_count}")
        if row_count == 1:
            return redirect(url_for('dashboard'))
        else:
            error = "Failed to insert into db"
            return redirect(url_for('quiz/add'), error = error)

    if request.method == 'GET':
        return render_template('add_quiz.html')


@app.route('/results/add', methods=['POST', 'GET'])
def add_quiz_results():
    dbHandle = db_work.getHandle()
    cursor = dbHandle.cursor()
    if request.method == 'POST':
        app.logger.info(request.form)
        cursor.execute("INSERT INTO student_results (student_id, quiz_id, score) VALUES (?,?,?)", (request.form['student'], request.form['quiz'], request.form['score']))
        dbHandle.commit()
        return redirect(url_for('dashboard'))
    if request.method == 'GET':
        cursor.execute("SELECT * from students")
        students = cursor.fetchall()
        app.logger.info(students)
        cursor.execute("SELECT * from quizzes")
        quizzes = cursor.fetchall()
        app.logger.info(quizzes)
        return render_template('add_results.html', students = students, quizzes = quizzes)


if __name__ == '__main__':
    print(app.root_path)
    app.run(debug=True)
