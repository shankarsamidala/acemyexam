import sqlite3

DATABASE_URL = "examination_system.db"

def get_db_connection():
    conn = sqlite3.connect(DATABASE_URL)
    return conn

def initialize_db():
    with get_db_connection() as conn:
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                age INTEGER,
                role TEXT DEFAULT 'student'
            )
        ''')
        c.execute('''
            CREATE TABLE IF NOT EXISTS questions (
                question_id INTEGER PRIMARY KEY AUTOINCREMENT,
                text TEXT NOT NULL,
                options TEXT,  
                correct_answer TEXT,  
                difficulty_level INTEGER NOT NULL CHECK (difficulty_level BETWEEN 1 AND 3),
                type TEXT NOT NULL CHECK (type IN ('MCQ', 'Descriptive')),
                marks INTEGER NOT NULL
            )
        ''')
        c.execute('''
            CREATE TABLE IF NOT EXISTS exam_results (
                result_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                question_id INTEGER NOT NULL,
                user_answer TEXT,
                score REAL,
                total_score REAL,
                exam_date DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(user_id),
                FOREIGN KEY (question_id) REFERENCES questions(question_id)
            )
        ''')
        c.execute('''
            CREATE TABLE IF NOT EXISTS exam_results (
                result_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                exam_id INTEGER,
                question_id INTEGER NOT NULL,
                user_answer TEXT,
                correct_answer TEXT,
                score REAL,
                details TEXT,
                total_score REAL,
                exam_date DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(user_id),
                FOREIGN KEY (question_id) REFERENCES questions(question_id)
            )
        ''')
        conn.commit()

initialize_db()
