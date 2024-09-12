import streamlit as st
from auth_service import login_user, register_user
from admin_panel import admin_panel  # Ensure you have this module
from exam_interface import student_interface  # Ensure you have this module

def main():
    st.title("Welcome ")

    # Initialize session state for user details if not already set
    if 'user_details' not in st.session_state:
        st.session_state['user_details'] = {'logged_in': False, 'role': None, 'user_id': None}

    # Navigation based on user login status
    if st.session_state['user_details']['logged_in']:
        # Redirect based on role, handling case sensitivity
        role = st.session_state['user_details']['role'].lower()  # Convert role to lowercase
        if role == 'admin':
            admin_panel()
        elif role == 'student':
            student_id = st.session_state['user_details']['user_id']
            if student_id:  # Check if student_id is available
                student_interface(student_id)  # Pass student_id to the student interface
            else:
                st.error("Student ID not found. Please log in again.")
        # Optionally, handle other roles
    else:
        # User is not logged in, show login and registration options
        tab1, tab2 = st.tabs(["Login", "Register"])

        with tab1:
            with st.form("login_form"):
                email = st.text_input("Email")
                password = st.text_input("Password", type="password")
                login_submit = st.form_submit_button("Login")

                if login_submit:
                    # Attempt to login
                    try:
                        user_details = login_user(email, password)
                        if user_details:
                            st.session_state['user_details'] = {'logged_in': True, 'role': user_details['role'], 'user_id': user_details['user_id']}
                            st.experimental_rerun()  # Use rerun to refresh the page with new session state
                    except ValueError as ve:
                        st.error(ve)
                    except Exception as e:
                        st.error(f"Login failed: {e}")

        with tab2:
            with st.form("register_form"):
                reg_email = st.text_input("Register Email")
                reg_password = st.text_input("Register Password", type="password")
                reg_age = st.number_input("Age", min_value=18, max_value=70)
                reg_role = st.selectbox("Role", ["Student", "Admin", "Teacher"])
                register_submit = st.form_submit_button("Register")

                if register_submit:
                    # Attempt to register
                    try:
                        register_user(reg_email, reg_password,reg_age,reg_role)
                        st.success("Registration successful. Please log in.")
                    except Exception as e:
                        st.error(f"Registration failed: {e}")

if __name__ == "__main__":
    main()
