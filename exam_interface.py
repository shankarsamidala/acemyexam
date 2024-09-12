# Assuming you have a file called student_interface.py or similar
import streamlit as st
from exam_service import fetch_grades,fetch_questions

def student_interface(student_id):
    st.sidebar.title("Student Dashboard")
    options = ["Previous Grades", "Take Exam"]
    choice = st.sidebar.radio("Navigate", options)

    if choice == "Previous Grades":
        display_grades(student_id)
    elif choice == "Take Exam":
        take_exam(student_id)

def display_grades(student_id):
    grades = fetch_grades(student_id)
    if grades:
        for exam_id, score in grades:
            st.write(f"Exam {exam_id}: Score {score}")
    else:
        st.write("No grades available.")

# Update in your student_interface.py or main Streamlit script

from datetime import datetime
from nlp_evaluation import evaluate_answer
from exam_service import fetch_questions, save_exam_results, check_if_taken_today, update_exam_results

from exam_service import fetch_questions, save_exam_results, update_exam_results, check_if_taken_today



def take_exam(student_id):
    st.title("Take Exam")
    mcqs, descriptives = fetch_questions()

    mcq_answers = {}
    for q_id, text, options, correct_answer, marks in mcqs:
        # Ensure options are treated as a string
        if isinstance(options, str):
            options_list = options.split(',')  # Split the options string into a list
        else:
            st.error(f"Expected options to be a string but got {type(options)}")
            options_list = []

        st.write(f"Question {q_id}: {text} (Marks: {marks})")  # Display question text and marks
        st.write(f"Options: {options_list}")  # Display options
        answer = st.radio(f"Select answer for Question {q_id}", options_list)
        mcq_answers[q_id] = (answer, correct_answer, marks)

    descriptive_answers = {}
    for q_id, text, correct_answer, marks in descriptives:
        st.write(f"Question {q_id}: {text} (Marks: {marks})")  # Display question text and marks
        answer = st.text_area(f"Answer for Question {q_id}", height=150)
        descriptive_answers[q_id] = (answer, correct_answer, marks)

    if st.button("Submit Exam"):
        # Calculate scores for MCQs
        mcq_scores = {}
        for q_id, (user_answer, correct_answer, marks) in mcq_answers.items():
            score = marks if user_answer == correct_answer else 0
            mcq_scores[q_id] = score

        total_mcq_score = sum(mcq_scores.values())

        # Calculate scores for descriptive questions
        descriptive_scores = {}
        normalized_scores_details = {}  # Store detailed normalized scores
        for q_id, (user_answer, correct_answer, marks) in descriptive_answers.items():
            result = evaluate_answer(user_answer, correct_answer)
            score = calculate_descriptive_score(result, marks)  # Pass max_marks to the function
            descriptive_scores[q_id] = score
            
            # Calculate and store normalized scores
            normalized_scores = {
                "Semantic Similarity": min(10, result["Semantic Similarity"] / 10),
                "Concept Matching": min(10, result["Concept Matching"] / 10),
                "Detail Level": min(10, result["Detail Level"] / 10),
                "Grammar Quality": min(10, result["Grammar Quality"] / 10)  # Normalize to 10
            }
            normalized_scores_details[q_id] = normalized_scores

        total_descriptive_score = sum(descriptive_scores.values())
        total_score = total_mcq_score + total_descriptive_score

        # Determine pass/fail status
        pass_fail_status = "Pass" if total_score > 50 else "Fail"  # Adjust pass criteria as needed

        st.write(f"Debug: Total score: {total_score}, Pass/Fail: {pass_fail_status}")
        st.write(f"Results: MCQs: {mcq_scores}, Descriptives: {descriptive_scores}, Total: {total_score}")

        # Detailed report for descriptive questions
        st.write("Detailed Report for Descriptive Questions:")
        for q_id, normalized_scores in normalized_scores_details.items():
            st.write(f"Question {q_id}:")
            st.write(f"  Normalized Scores:")
            for criteria, score in normalized_scores.items():
                st.write(f"    {criteria}: {score:.2f} / 10")

        # Save or update exam results
        if check_if_taken_today(student_id):
            update_exam_results(student_id, mcq_scores, descriptive_scores, total_score)
        else:
            st.write('-------------Saving Results----------------')
            save_exam_results(student_id, mcq_scores, descriptive_answers, total_score)

        st.success(f"Exam submitted successfully! You {'passed' if pass_fail_status == 'Pass' else 'failed'} with {total_score}%.")






# def take_exam(student_id):
#     st.title("Take Exam")
#     mcqs, descriptives = fetch_questions()

#     mcq_answers = {}
#     for q_id, text, options, correct_answer, marks in mcqs:
#         # Ensure options are treated as a string
#         if isinstance(options, str):
#             options_list = options.split(',')  # Split the options string into a list
#         else:
#             st.error(f"Expected options to be a string but got {type(options)}")
#             options_list = []

#         st.write(f"Debug: Options list for question {q_id} - {options_list}")  # Debug output to visualize options
#         answer = st.radio(f"Q: {text}", options_list)
#         mcq_answers[q_id] = (answer, correct_answer, marks)

#     descriptive_answers = {}
#     for q_id, text, correct_answer, marks in descriptives:
#         answer = st.text_area(f"Q: {text}", height=150)
#         descriptive_answers[q_id] = (answer, correct_answer, marks)

#     if st.button("Submit Exam"):
#         # Calculate scores for MCQs
#         mcq_scores = {}
#         for q_id, (user_answer, correct_answer, marks) in mcq_answers.items():
#             score = marks if user_answer == correct_answer else 0
#             mcq_scores[q_id] = score
        
#         total_mcq_score = sum(mcq_scores.values())

#         # Calculate scores for descriptive questions
#         descriptive_scores = {}
#         for q_id, (user_answer, correct_answer, marks) in descriptive_answers.items():
#             result = evaluate_answer(user_answer, correct_answer)
#             score = calculate_descriptive_score(result)  # Function to calculate descriptive score
#             descriptive_scores[q_id] = score

#         total_descriptive_score = sum(descriptive_scores.values())
#         total_score = total_mcq_score + total_descriptive_score
        
#         # Determine pass/fail status
#         pass_fail_status = "Pass" if total_score > 50 else "Fail"  # Adjust pass criteria as needed
        
#         st.write(f"Debug: Total score: {total_score}, Pass/Fail: {pass_fail_status}")
#         st.write(f"Results: MCQs: {mcq_scores}, Descriptives: {descriptive_scores}, Total: {total_score}")

#         # Save or update exam results
#         if check_if_taken_today(student_id):
#             update_exam_results(student_id, mcq_scores, descriptive_scores, total_score)
#         else:
#             st.write('-------------Saving Results----------------')
#             save_exam_results(student_id, mcq_scores, descriptive_answers, total_score)

#         st.success(f"Exam submitted successfully! You {'passed' if pass_fail_status == 'Pass' else 'failed'} with {total_score}%.")

def calculate_descriptive_score(nlp_results, max_marks):
    """
    Calculate and normalize the total score for a descriptive answer based on NLP evaluation results.
    
    Parameters:
        nlp_results (dict): A dictionary containing the results of the NLP evaluation for a descriptive answer.
        max_marks (int): The maximum marks allocated for the question.
        
    Returns:
        float: The normalized score for the descriptive answer.
    """
    # Define the weight of each component
    weights = {
        "Semantic Similarity": 0.4,  # 40% weight
        "Concept Matching": 0.2,     # 20% weight
        "Detail Level": 0.2,         # 20% weight
        "Grammar Quality": 0.2     # 20% weight
    }

    # Calculate the total score by multiplying each result by its weight and summing them up
    total_score = 0.0
    for key, weight in weights.items():
        component_score = nlp_results.get(key, 0)
        # Ensure component_score is scaled to 100 before weighting
        component_score = min(component_score, 100)  
        total_score += component_score * weight

    # Normalize the score to fit within the allocated marks
    normalized_score = (total_score / 100) * max_marks
    
    return normalized_score
