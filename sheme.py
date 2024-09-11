import sqlite3

DATABASE_URL = "examination_system.db"

def check_and_update_schema():
    conn = sqlite3.connect(DATABASE_URL)
    cur = conn.cursor()
    
    # Check if the 'difficulty_level' column exists
    cur.execute("PRAGMA table_info(questions);")
    columns = [row[1] for row in cur.fetchall()]
    
    if 'difficulty_level' not in columns:
        print("Column 'difficulty_level' is missing. Adding...")
        cur.execute('''
            ALTER TABLE questions ADD COLUMN difficulty_level INTEGER NOT NULL CHECK (difficulty_level BETWEEN 1 AND 3);
        ''')
        conn.commit()
        print("Column added successfully.")
    else:
        print("Column 'difficulty_level' already exists.")
    
    conn.close()

check_and_update_schema()
