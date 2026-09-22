import sqlite3
from database.database import get_connection
from utils.helpers import generate_employee_id
from models.employee import Employee

class EmployeeService:
    @staticmethod
    def add_department(department_name):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO departments (department_name) VALUES (?)", (department_name,))
            conn.commit()
            return True, "Department added successfully."
        except sqlite3.IntegrityError:
            return False, "Department already exists."
        finally:
            conn.close()

    @staticmethod
    def get_all_departments():
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM departments")
        departments = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return departments

    @staticmethod
    def get_department_id_by_name(name):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT department_id FROM departments WHERE department_name = ?", (name,))
        row = cursor.fetchone()
        conn.close()
        return row['department_id'] if row else None

    @staticmethod
    def add_employee(name, email, phone, department_id, designation, joining_date, salary):
        conn = get_connection()
        cursor = conn.cursor()
        
        # Generate new ID
        cursor.execute("SELECT employee_id FROM employees ORDER BY rowid DESC LIMIT 1")
        last_row = cursor.fetchone()
        last_id = last_row['employee_id'] if last_row else None
        new_id = generate_employee_id(last_id)
        
        try:
            cursor.execute("""
                INSERT INTO employees (employee_id, name, email, phone, department_id, designation, joining_date, salary, status)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, 'Active')
            """, (new_id, name, email, phone, department_id, designation, joining_date, salary))
            conn.commit()
            return True, f"Employee added successfully with ID: {new_id}"
        except sqlite3.IntegrityError:
            return False, "Error: Email already exists or invalid department."
        finally:
            conn.close()

    @staticmethod
    def get_all_employees():
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT e.employee_id, e.name, e.email, e.phone, d.department_name, e.designation, e.salary, e.status
            FROM employees e
            LEFT JOIN departments d ON e.department_id = d.department_id
        """)
        employees = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return employees

    @staticmethod
    def search_employees(query):
        conn = get_connection()
        cursor = conn.cursor()
        search_term = f"%{query}%"
        cursor.execute("""
            SELECT e.employee_id, e.name, e.email, d.department_name, e.designation, e.status
            FROM employees e
            LEFT JOIN departments d ON e.department_id = d.department_id
            WHERE e.employee_id LIKE ? OR e.name LIKE ? OR d.department_name LIKE ? OR e.designation LIKE ?
        """, (search_term, search_term, search_term, search_term))
        employees = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return employees

    @staticmethod
    def update_employee_designation(employee_id, new_designation):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE employees SET designation = ? WHERE employee_id = ?", (new_designation, employee_id))
        updated = cursor.rowcount > 0
        conn.commit()
        conn.close()
        return updated

    @staticmethod
    def delete_employee(employee_id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE employees SET status = 'Terminated' WHERE employee_id = ?", (employee_id,))
        updated = cursor.rowcount > 0
        conn.commit()
        conn.close()
        return updated

    @staticmethod
    def get_dashboard_stats():
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM employees WHERE status = 'Active'")
        active_emp = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM departments")
        dept_count = cursor.fetchone()[0]
        
        conn.close()
        return {
            'active_employees': active_emp,
            'total_departments': dept_count
        }
