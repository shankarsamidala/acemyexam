import streamlit as st
from admin_service import add_question, update_question, delete_question,get_all_questions
import pandas as pd
def admin_panel():
    st.title("Admin Dashboard")
    choice = st.sidebar.selectbox("Admin Actions", [ "View Questions","Add Question", "Update Question", "Delete Question"])

    if choice == "Add Question":
        with st.form("add_question_form"):
            text = st.text_area("Question Text")
            difficulty_level = st.selectbox("Difficulty Level", [1, 2, 3])
            type = st.selectbox("Question Type", ["MCQ", "Descriptive"])
            marks = st.number_input("Marks", min_value=1, max_value=100, value=10)
            
            # Conditional display based on question type
            options = st.text_input("Options (for MCQs, comma-separated)") if type == "MCQ" else None
            correct_answer = st.text_area("Correct Answer (for Descriptive type or correct option for MCQs)")

            submit = st.form_submit_button("Submit")
            if submit:
                # Handle the case where options might be None
                options_to_save = options if options is not None else ""
                add_question(text, options_to_save, correct_answer, difficulty_level, type, marks)
                st.success("Question added successfully!")

    elif choice == "Update Question":
        question_id = st.number_input("Enter Question ID", min_value=1, format="%d")
        with st.form("update_question_form"):
            text = st.text_area("Question Text")
            difficulty_level = st.selectbox("Difficulty Level", [1, 2, 3])
            type = st.selectbox("Question Type", ["MCQ", "Descriptive"])
            marks = st.number_input("Marks", min_value=1, max_value=100, value=10)
            
            options = st.text_input("Options (for MCQs, comma-separated)") if type == "MCQ" else None
            correct_answer = st.text_area("Correct Answer")

            update_submit = st.form_submit_button("Update")
            if update_submit:
                options_to_save = options if options is not None else ""
                update_question(question_id, text, options_to_save, correct_answer, difficulty_level, type, marks)
                st.success("Question updated successfully!")

    elif choice == "Delete Question":
        question_id = st.number_input("Enter Question ID to delete", min_value=1, format="%d")
        if st.button("Delete"):
            delete_question(question_id)
            st.success("Question deleted successfully.")
    elif choice == "View Questions":
        view_questions()

def view_questions():
    questions = get_all_questions()
    if questions:
        # Convert the list of dictionaries to a DataFrame for better display
        df = pd.DataFrame(questions)
        # Optionally, adjust the column order or drop unnecessary columns
        df = df[['question_id', 'text', 'type', 'difficulty_level', 'marks', 'options', 'correct_answer']]
        # Handle display for MCQ options and descriptive answers
        df['options'] = df.apply(lambda x: x['options'] if x['type'] == 'MCQ' else 'N/A', axis=1)
        
        st.write("Questions Overview:")
        st.dataframe(df)  # Display the DataFrame as an interactive table
    else:
        st.write("No questions available.")
if __name__ == "__main__":
    admin_panel()
