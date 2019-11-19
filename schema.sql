
CREATE TABLE IF NOT EXISTS students(
  id integer PRIMARY KEY,
  first_name TEXT NOT NULL,
  last_name TEXT NOT NULL,
  UNIQUE(id));

CREATE TABLE IF NOT EXISTS quizzes(
  id integer PRIMARY KEY,
  subject TEXT NOT NULL,
  questions integer NOT NULL,
  quiz_date TEXT NOT NULL,
  UNIQUE(id));

CREATE TABLE IF NOT EXISTS student_results(
  student_id integer NOT NULL,
  quiz_id integer NOT NULL,
  score integer NOT NULL);
