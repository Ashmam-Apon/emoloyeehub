import bcrypt
import sqlite3
from database.database import get_connection

def hash_password(password):
    """Hash a password using bcrypt."""
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

def check_password(password, hashed):
    """Check a password against a hash."""
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

def seed_admin_if_not_exists():
    """Create a default admin user if the users table is empty."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM users")
    count = cursor.fetchone()[0]
    
    if count == 0:
        admin_pass = hash_password("admin123")
        cursor.execute(
            "INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)",
            ("admin", admin_pass, "Admin")
        )
        conn.commit()
    conn.close()

def login(username, password):
    """Authenticate a user and return their role."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT user_id, password_hash, role FROM users WHERE username = ?", (username,))
    row = cursor.fetchone()
    conn.close()
    
    if row and check_password(password, row['password_hash']):
        return {'user_id': row['user_id'], 'username': username, 'role': row['role']}
    return None

def create_user(username, password, role):
    """Create a new user."""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        hashed = hash_password(password)
        cursor.execute(
            "INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)",
            (username, hashed, role)
        )
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()
