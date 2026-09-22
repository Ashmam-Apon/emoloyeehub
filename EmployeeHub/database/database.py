import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'employeehub.db')

def get_connection():
    """Establish and return a connection to the SQLite database."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # Return rows as dictionaries
    return conn

def init_db():
    """Initialize the database with the required tables."""
    from database.queries import CREATE_TABLES
    
    conn = get_connection()
    try:
        cursor = conn.cursor()
        for query in CREATE_TABLES:
            cursor.execute(query)
        conn.commit()
    except sqlite3.Error as e:
        print(f"Database error: {e}")
    finally:
        conn.close()
