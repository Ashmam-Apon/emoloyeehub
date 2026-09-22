import sqlite3
from database.database import get_connection

class LeaveService:
    @staticmethod
    def submit_leave_request(employee_id, leave_type, start_date, end_date, reason):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO leave_requests (employee_id, leave_type, start_date, end_date, reason)
                VALUES (?, ?, ?, ?, ?)
            """, (employee_id, leave_type, start_date, end_date, reason))
            conn.commit()
            return True, "Leave request submitted successfully."
        except sqlite3.Error as e:
            return False, f"Database error: {e}"
        finally:
            conn.close()

    @staticmethod
    def get_leave_requests_by_employee(employee_id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM leave_requests WHERE employee_id = ? ORDER BY start_date DESC", (employee_id,))
        requests = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return requests

    @staticmethod
    def get_pending_leave_requests():
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT l.*, e.name 
            FROM leave_requests l
            JOIN employees e ON l.employee_id = e.employee_id
            WHERE l.status = 'Pending'
            ORDER BY l.start_date ASC
        """)
        requests = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return requests

    @staticmethod
    def update_leave_status(leave_id, status):
        """status should be 'Approved' or 'Rejected'"""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE leave_requests SET status = ? WHERE leave_id = ?", (status, leave_id))
        updated = cursor.rowcount > 0
        conn.commit()
        conn.close()
        return updated
