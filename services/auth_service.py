from config.db_config import get_db_connection
import sqlite3

def register_user(email, password,  age, role='student'):
    conn = get_db_connection()
    try:
        with conn:
            conn.execute('''
                INSERT INTO users (email, password,  age, role)
                VALUES (?, ?, ?,  ?)
            ''', (email, password,  age, role))
    except sqlite3.IntegrityError:
        raise ValueError("A user with this email already exists")

def login_user(email, password):
    conn = get_db_connection()
    try:
        with conn:
            user = conn.execute('''
                SELECT user_id, email, role FROM users WHERE email = ? AND password = ?
            ''', (email, password)).fetchone()
            if user:
                return {"user_id": user[0], "email": user[1], "role": user[2]}
            else:
                raise ValueError("Invalid credentials")
    finally:
        conn.close()


# from firebase_admin import auth,exceptions
# from config.firebase_config import db

# def register_user(email, password, additional_info, role='student'):
#     try:
#         # Create user with Firebase Authentication
#         user_record = auth.create_user(email=email, password=password)
#         # Include the role in the additional_info dictionary
#         user_info = {**additional_info, "role": role}
#         # Save user info in Firestore
#         db.collection('users').document(user_record.uid).set(user_info)
#         return user_record
#     except auth.FirebaseError as e:
#         raise ValueError(f"Failed to register user: {str(e)}")
        

# def login_user(email, password):
#     try:
#         user_record = auth.get_user_by_email(email)
#         # Simulating password check via custom token (for demonstration purposes)
#         # Note: This is NOT a real password validation; it assumes if the user exists, authentication is successful.
#         # Generate a custom token
#         custom_token = auth.create_custom_token(user_record.uid)
#         if custom_token:
#             return {"email": user_record.email, "uid": user_record.uid, "token": custom_token}
#         else:
#             raise ValueError("Authentication failed.")
#     except auth.UserNotFoundError:
#         raise ValueError("User not found")
#     except exceptions.FirebaseError as e:
#         raise Exception("Firebase error: {}".format(e))