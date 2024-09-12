import sqlite3
from db_config import get_db_connection

def add_question(text, options, correct_answer, difficulty_level, type, marks):
    conn = get_db_connection()
    with conn:
        conn.execute('''
            INSERT INTO questions (text, options, correct_answer, difficulty_level, type, marks)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (text, options, correct_answer, difficulty_level, type, marks))
        conn.commit()

def update_question(question_id, text, options, correct_answer, difficulty_level, type, marks):
    conn = get_db_connection()
    with conn:
        conn.execute('''
            UPDATE questions SET text=?, options=?, correct_answer=?, difficulty_level=?, type=?, marks=?
            WHERE question_id=?
        ''', (text, options, correct_answer, difficulty_level, type, marks, question_id))
        conn.commit()

def delete_question(question_id):
    conn = get_db_connection()
    with conn:
        conn.execute('DELETE FROM questions WHERE question_id=?', (question_id,))
        conn.commit()
        
def get_all_questions():
    conn = get_db_connection()
    questions = []
    with conn:
        cur = conn.execute('SELECT * FROM questions')
        rows = cur.fetchall()
        for row in rows:
            questions.append({
                'question_id': row[0],
                'text': row[1],
                'options': row[2],
                'correct_answer': row[3],
                'difficulty_level': row[4],
                'type': row[5],
                'marks': row[6]
            })
    return questions

