import sqlite3 as sql
import os

import logging
log = logging.getLogger('w12hw.sub')

def getHandle():
    dbHandle = sql.connect('file:hw13.db', uri=True)
    cursor = dbHandle.cursor()

    return dbHandle
    #dbHandle.close()

def createDB(dbHandle):
    cursor = dbHandle.cursor()
    log.info("Create table if NOT exists")
    with open('c:/Users/silaz/github/capstone/is211/w12/db_book/schema.sql', 'r') as sqlite_file:
        sql_script = sqlite_file.read()
    cursor.executescript(sql_script)
    dbHandle.commit()

def insertStudent(first_name, last_name, dbHandle):
    log.warning(f"Inserting users {first_name} {last_name}")
    cursor = dbHandle.cursor()
    log.warning(f"INSERT INTO students (first_name, last_name) VALUES ({first_name},{last_name})")
    cursor.execute("INSERT INTO students (first_name, last_name) VALUES (?,?)", (first_name, last_name))
    try:
        dbHandle.commit()
        return 1
    except:
        log.warning("Exception inserting Student")
        return 0

def addQuiz(subject, questions, quiz_date, dbHandle):
    cursor = dbHandle.cursor()
    cursor.execute('''INSERT INTO quizzes
            (subject, questions, quiz_date)
            VALUES(?, ?, ?)''', (subject, questions, quiz_date))
    try:
        dbHandle.commit()
        return 1
    except:
        log.warning("Exception inserting Student")
        return 0

def load_test_data(dbHandle):
    insertStudent('John', 'Smith', dbHandle)
    addQuiz('Python Basics', 5, 'February 5, 2005', dbHandle)
    cursor = dbHandle.cursor()
    cursor.execute("INSERT INTO student_results (student_id, quiz_id, score) VALUES (?,?,?)", (1, 1, 100))
    dbHandle.commit()
