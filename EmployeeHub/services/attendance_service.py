import sqlite3
from database.database import get_connection
from datetime import datetime

class AttendanceService:
    @staticmethod
    def mark_attendance(employee_id, date, check_in, check_out, status):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO attendance (employee_id, date, check_in, check_out, status)
                VALUES (?, ?, ?, ?, ?)
            """, (employee_id, date, check_in, check_out, status))
            conn.commit()
            return True, "Attendance marked successfully."
        except sqlite3.IntegrityError:
            return False, "Attendance for this date already exists."
        finally:
            conn.close()

    @staticmethod
    def get_attendance_by_employee(employee_id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM attendance WHERE employee_id = ? ORDER BY date DESC", (employee_id,))
        records = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return records

    @staticmethod
    def calculate_attendance_percentage(employee_id, month_prefix):
        """month_prefix like '2023-10'"""
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT COUNT(*) FROM attendance 
            WHERE employee_id = ? AND date LIKE ?
        """, (employee_id, f"{month_prefix}%"))
        total_days_recorded = cursor.fetchone()[0]
        
        cursor.execute("""
            SELECT COUNT(*) FROM attendance 
            WHERE employee_id = ? AND date LIKE ? AND status IN ('Present', 'Late')
        """, (employee_id, f"{month_prefix}%"))
        present_days = cursor.fetchone()[0]
        
        conn.close()
        
        if total_days_recorded == 0:
            return 0.0
            
        return (present_days / total_days_recorded) * 100
