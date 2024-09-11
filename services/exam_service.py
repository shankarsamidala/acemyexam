# services/exam_service.py
import json
from config.db_config import get_db_connection

def fetch_grades(student_id):
    """
    Fetches all grades for a specific student by student_id.
    Returns a list of tuples (exam_id, score) or None if no grades are available.
    """
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT result_id, total_score
            FROM exam_results
            WHERE user_id = ?
        ''', (student_id,))
        results = cursor.fetchall()
        
        if not results:
            return None
        
        return results

# Add this function to your services/exam_service.py

import random

from datetime import datetime
def fetch_questions():
    with get_db_connection() as conn:
        cursor = conn.cursor()
        
        # Fetch all MCQs
        cursor.execute('''
            SELECT question_id, text, options, correct_answer, marks
            FROM questions
            WHERE type = 'MCQ'
        ''')
        mcqs = cursor.fetchall()
        print("MCQs fetched:")
        for mcq in mcqs:
            print(mcq)  # Print each MCQ record

        # Fetch all Descriptive Questions
        cursor.execute('''
            SELECT question_id, text, correct_answer, marks
            FROM questions
            WHERE type = 'Descriptive'
        ''')
        descriptives = cursor.fetchall()
        print("Descriptives fetched:")
        for descriptive in descriptives:
            print(descriptive)  # Print each Descriptive record
    
    return mcqs, descriptives




def check_if_taken_today(student_id):
    today = datetime.now().date()
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM exam_results WHERE user_id = ? AND date(exam_date) = ?', (student_id, today))
        return cursor.fetchone() is not None        
    
import json

def save_exam_results(student_id, mcq_scores, descriptive_scores, total_score):
    """
    Save the results of an exam to the database.

    Parameters:
        student_id (int): The ID of the student who took the exam.
        mcq_scores (dict): A dictionary of MCQ question IDs and their scores (assumes the user's choice is stored in the score variable).
        descriptive_scores (dict): A dictionary of descriptive question IDs and their detailed scores including the user's answer.
        total_score (float): The total score of the exam.
    """
    with get_db_connection() as conn:
        cursor = conn.cursor()
        # Insert each MCQ question's result
        for q_id, score in mcq_scores.items():
            # Assuming the user's choice for the MCQ is stored in a way accessible as `score[0]` and the score itself is `score[1]`
            user_choice, question_score = score
            cursor.execute('''
                INSERT INTO exam_results (user_id, question_id, user_answer, correct_answer, score, total_score, exam_date)
                VALUES (?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
            ''', (student_id, q_id, user_choice, "correct answer here", question_score, total_score))
        
        # Insert each descriptive question's result
        for q_id, details in descriptive_scores.items():
            # Assuming `details` is a dict containing 'user_answer', 'correct_answer', 'score'
            user_answer = details['user_answer']
            correct_answer = details['correct_answer']
            question_score = details['score']
            details_json = json.dumps(details)  # Serialize additional details if needed
            cursor.execute('''
                INSERT INTO exam_results (user_id, question_id, user_answer, correct_answer, score, details, total_score, exam_date)
                VALUES (?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
            ''', (student_id, q_id, user_answer, correct_answer, question_score, details_json, total_score))

        conn.commit()



def update_exam_results(student_id, mcq_scores, descriptive_scores, total_score):
    """
    Update the results of an exam for a student on the same day.
    
    Parameters:
        student_id (int): The ID of the student who retook the exam.
        mcq_scores (dict): A dictionary of MCQ question IDs and their scores.
        descriptive_scores (dict): A dictionary of descriptive question IDs and their detailed scores.
        total_score (float): The updated total score of the exam.
    """
    with get_db_connection() as conn:
        cursor = conn.cursor()
        # Update each question's result
        for q_id, score in mcq_scores.items():
            cursor.execute('''
                UPDATE exam_results SET user_answer = ?, score = ?, total_score = ?, exam_date = CURRENT_TIMESTAMP
                WHERE user_id = ? AND question_id = ? AND date(exam_date) = date('now')
            ''', ("user's choice here", score, total_score, student_id, q_id))

        for q_id, details in descriptive_scores.items():
            cursor.execute('''
                UPDATE exam_results SET user_answer = ?, score = ?, details = ?, total_score = ?, exam_date = CURRENT_TIMESTAMP
                WHERE user_id = ? AND question_id = ? AND date(exam_date) = date('now')
            ''', ("user's answer here", details['score'], json.dumps(details), total_score, student_id, q_id))

        conn.commit()
