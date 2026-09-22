import sqlite3
from database.database import get_connection
from models.payroll import Payroll

class PayrollService:
    @staticmethod
    def generate_payroll(employee_id, month, basic_salary, allowances, bonus, deductions):
        net_salary = Payroll.calculate_net_salary(basic_salary, allowances, bonus, deductions)
        
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO payroll (employee_id, month, basic_salary, allowances, bonus, deductions, net_salary)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (employee_id, month, basic_salary, allowances, bonus, deductions, net_salary))
            conn.commit()
            return True, f"Payroll generated. Net Salary: ${net_salary:.2f}"
        except sqlite3.IntegrityError:
            return False, "Payroll for this month already exists."
        finally:
            conn.close()

    @staticmethod
    def get_payroll_by_employee(employee_id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM payroll WHERE employee_id = ? ORDER BY month DESC", (employee_id,))
        records = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return records

    @staticmethod
    def get_all_payroll_by_month(month):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT p.*, e.name 
            FROM payroll p
            JOIN employees e ON p.employee_id = e.employee_id
            WHERE p.month = ?
            ORDER BY p.payroll_id ASC
        """, (month,))
        records = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return records
