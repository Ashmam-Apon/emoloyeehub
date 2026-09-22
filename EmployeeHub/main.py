import sys
from getpass import getpass
from database.database import init_db
from services.auth_service import login, seed_admin_if_not_exists, create_user
from services.employee_service import EmployeeService
from services.attendance_service import AttendanceService
from services.leave_service import LeaveService
from services.payroll_service import PayrollService
from reports.report_generator import export_to_csv
from utils.helpers import clear_screen, print_header, print_table
from utils.validators import get_valid_input, is_valid_email, is_valid_date, is_valid_phone, get_valid_float

class EmployeeHubApp:
    def __init__(self):
        init_db()
        seed_admin_if_not_exists()
        self.current_user = None

    def run(self):
        while True:
            if not self.current_user:
                self.login_menu()
            else:
                self.main_menu()

    def login_menu(self):
        print_header("EMPLOYEEHUB LOGIN")
        username = input("Username: ").strip()
        password = getpass("Password: ").strip()
        
        user = login(username, password)
        if user:
            self.current_user = user
            print(f"\nWelcome, {username}! Logged in as {user['role']}.")
            input("Press Enter to continue...")
        else:
            print("\nInvalid username or password.")
            input("Press Enter to try again...")

    def main_menu(self):
        while True:
            print_header("EMPLOYEEHUB HR SYSTEM")
            print("1. Dashboard")
            print("2. Employee Management")
            print("3. Department Management")
            print("4. Attendance")
            print("5. Leave Management")
            print("6. Payroll")
            print("7. Reports & Analytics")
            if self.current_user['role'] == 'Admin':
                print("8. User Management")
            print("9. Logout")
            print("0. Exit")
            print("-" * 60)
            
            choice = input("Enter choice: ").strip()
            
            if choice == '1':
                self.dashboard()
            elif choice == '2':
                self.employee_management()
            elif choice == '3':
                self.department_management()
            elif choice == '4':
                self.attendance_management()
            elif choice == '5':
                self.leave_management()
            elif choice == '6':
                self.payroll_management()
            elif choice == '7':
                self.reports_menu()
            elif choice == '8' and self.current_user['role'] == 'Admin':
                self.user_management()
            elif choice == '9':
                self.current_user = None
                return
            elif choice == '0':
                print("Exiting EmployeeHub. Goodbye!")
                sys.exit(0)
            else:
                print("Invalid choice. Please try again.")
                input("Press Enter to continue...")

    def dashboard(self):
        print_header("DASHBOARD")
        stats = EmployeeService.get_dashboard_stats()
        print(f"Active Employees: {stats['active_employees']}")
        print(f"Total Departments: {stats['total_departments']}")
        
        pending_leaves = LeaveService.get_pending_leave_requests()
        print(f"Pending Leave Requests: {len(pending_leaves)}")
        print("\n")
        input("Press Enter to continue...")

    def employee_management(self):
        while True:
            print_header("EMPLOYEE MANAGEMENT")
            print("1. Add Employee")
            print("2. List Employees")
            print("3. Search Employee")
            print("4. Update Designation")
            print("5. Delete Employee")
            print("0. Back to Main Menu")
            print("-" * 60)
            
            choice = input("Enter choice: ").strip()
            
            if choice == '1':
                if self.current_user['role'] == 'Employee':
                    print("Access Denied. Only Admin/HR can add employees.")
                else:
                    self.add_employee()
            elif choice == '2':
                self.list_employees()
            elif choice == '3':
                self.search_employee()
            elif choice == '4':
                if self.current_user['role'] == 'Employee':
                    print("Access Denied.")
                else:
                    self.update_employee()
            elif choice == '5':
                if self.current_user['role'] != 'Admin':
                    print("Access Denied. Only Admin can delete employees.")
                else:
                    self.delete_employee()
            elif choice == '0':
                break
            else:
                print("Invalid choice.")
            
            if choice != '0':
                input("Press Enter to continue...")

    def add_employee(self):
        print_header("ADD EMPLOYEE")
        name = input("Name: ").strip()
        email = get_valid_input("Email: ", is_valid_email, "Invalid email format.")
        phone = get_valid_input("Phone: ", is_valid_phone, "Invalid phone format.")
        
        depts = EmployeeService.get_all_departments()
        if not depts:
            print("No departments exist. Please create a department first.")
            return
            
        print("\nAvailable Departments:")
        for d in depts:
            print(f"- {d['department_name']} (ID: {d['department_id']})")
        
        dept_id = input("\nEnter Department ID: ").strip()
        designation = input("Designation: ").strip()
        joining_date = get_valid_input("Joining Date (YYYY-MM-DD): ", is_valid_date, "Invalid date format.")
        salary = get_valid_float("Salary: ")
        
        success, msg = EmployeeService.add_employee(name, email, phone, dept_id, designation, joining_date, salary)
        print(msg)

    def list_employees(self):
        print_header("EMPLOYEE LIST")
        employees = EmployeeService.get_all_employees()
        if employees:
            headers = ["employee_id", "name", "department_name", "designation", "status"]
            # format for display
            display_data = [{k: e.get(k, '') for k in headers} for e in employees]
            print_table(display_data, headers)
        else:
            print("No employees found.")

    def search_employee(self):
        print_header("SEARCH EMPLOYEE")
        query = input("Enter search term (ID, Name, Dept, Designation): ").strip()
        employees = EmployeeService.search_employees(query)
        if employees:
            headers = ["employee_id", "name", "email", "department_name", "designation", "status"]
            print_table(employees, headers)
        else:
            print("No matching employees found.")

    def update_employee(self):
        print_header("UPDATE DESIGNATION")
        emp_id = input("Enter Employee ID: ").strip()
        new_desig = input("Enter New Designation: ").strip()
        
        if EmployeeService.update_employee_designation(emp_id, new_desig):
            print("Designation updated successfully.")
        else:
            print("Employee not found.")

    def delete_employee(self):
        print_header("DELETE EMPLOYEE")
        emp_id = input("Enter Employee ID to delete (mark as Terminated): ").strip()
        
        confirm = input(f"Are you sure you want to delete {emp_id}? (y/n): ").strip().lower()
        if confirm == 'y':
            if EmployeeService.delete_employee(emp_id):
                print("Employee deleted successfully.")
            else:
                print("Employee not found.")

    def department_management(self):
        while True:
            print_header("DEPARTMENT MANAGEMENT")
            print("1. Add Department")
            print("2. List Departments")
            print("0. Back to Main Menu")
            print("-" * 60)
            
            choice = input("Enter choice: ").strip()
            if choice == '1':
                if self.current_user['role'] == 'Employee':
                    print("Access Denied.")
                else:
                    name = input("Department Name: ").strip()
                    success, msg = EmployeeService.add_department(name)
                    print(msg)
            elif choice == '2':
                depts = EmployeeService.get_all_departments()
                print_table(depts, ["department_id", "department_name"])
            elif choice == '0':
                break
            else:
                print("Invalid choice.")
                
            if choice != '0':
                input("Press Enter to continue...")

    def attendance_management(self):
        while True:
            print_header("ATTENDANCE MANAGEMENT")
            print("1. Mark Attendance")
            print("2. View My Attendance (Employee)")
            print("3. View Employee Attendance Percentage (HR/Admin)")
            print("0. Back to Main Menu")
            print("-" * 60)
            
            choice = input("Enter choice: ").strip()
            
            if choice == '1':
                if self.current_user['role'] == 'Employee':
                    print("Access Denied. Currently only HR/Admin marks attendance in this demo.")
                else:
                    emp_id = input("Employee ID: ").strip()
                    date = get_valid_input("Date (YYYY-MM-DD): ", is_valid_date, "Invalid date.")
                    check_in = input("Check In (HH:MM): ").strip()
                    check_out = input("Check Out (HH:MM): ").strip()
                    status = input("Status (Present/Absent/Late): ").strip().capitalize()
                    
                    if status in ['Present', 'Absent', 'Late']:
                        success, msg = AttendanceService.mark_attendance(emp_id, date, check_in, check_out, status)
                        print(msg)
                    else:
                        print("Invalid status.")
            
            elif choice == '2':
                # Simplified for demo: ask for ID to view records
                emp_id = input("Enter your Employee ID: ").strip()
                records = AttendanceService.get_attendance_by_employee(emp_id)
                print_table(records, ["date", "check_in", "check_out", "status"])
                
            elif choice == '3':
                if self.current_user['role'] == 'Employee':
                    print("Access Denied.")
                else:
                    emp_id = input("Employee ID: ").strip()
                    month = input("Month (YYYY-MM): ").strip()
                    perc = AttendanceService.calculate_attendance_percentage(emp_id, month)
                    print(f"Attendance Percentage for {month}: {perc:.2f}%")
                    
            elif choice == '0':
                break
            else:
                print("Invalid choice.")
                
            if choice != '0':
                input("Press Enter to continue...")

    def leave_management(self):
        while True:
            print_header("LEAVE MANAGEMENT")
            print("1. Submit Leave Request")
            print("2. View My Leave Requests")
            print("3. Manage Pending Leave Requests (HR/Admin)")
            print("0. Back to Main Menu")
            print("-" * 60)
            
            choice = input("Enter choice: ").strip()
            
            if choice == '1':
                emp_id = input("Employee ID: ").strip()
                leave_type = input("Leave Type (Sick, Casual, Annual): ").strip()
                start = get_valid_input("Start Date (YYYY-MM-DD): ", is_valid_date, "Invalid date.")
                end = get_valid_input("End Date (YYYY-MM-DD): ", is_valid_date, "Invalid date.")
                reason = input("Reason: ").strip()
                
                success, msg = LeaveService.submit_leave_request(emp_id, leave_type, start, end, reason)
                print(msg)
                
            elif choice == '2':
                emp_id = input("Employee ID: ").strip()
                requests = LeaveService.get_leave_requests_by_employee(emp_id)
                print_table(requests, ["leave_id", "leave_type", "start_date", "end_date", "status"])
                
            elif choice == '3':
                if self.current_user['role'] == 'Employee':
                    print("Access Denied.")
                else:
                    pending = LeaveService.get_pending_leave_requests()
                    if not pending:
                        print("No pending requests.")
                    else:
                        print_table(pending, ["leave_id", "employee_id", "name", "leave_type", "start_date", "end_date"])
                        leave_id = input("\nEnter Leave ID to manage (or press Enter to cancel): ").strip()
                        if leave_id:
                            action = input("Approve or Reject (a/r): ").strip().lower()
                            if action == 'a':
                                if LeaveService.update_leave_status(leave_id, 'Approved'):
                                    print("Leave approved.")
                            elif action == 'r':
                                if LeaveService.update_leave_status(leave_id, 'Rejected'):
                                    print("Leave rejected.")
                                
            elif choice == '0':
                break
            else:
                print("Invalid choice.")
                
            if choice != '0':
                input("Press Enter to continue...")

    def payroll_management(self):
        while True:
            print_header("PAYROLL MANAGEMENT")
            print("1. Generate Payroll (HR/Admin)")
            print("2. View Employee Payroll History")
            print("0. Back to Main Menu")
            print("-" * 60)
            
            choice = input("Enter choice: ").strip()
            
            if choice == '1':
                if self.current_user['role'] == 'Employee':
                    print("Access Denied.")
                else:
                    emp_id = input("Employee ID: ").strip()
                    month = input("Month (YYYY-MM): ").strip()
                    basic = get_valid_float("Basic Salary: ")
                    allowances = get_valid_float("Allowances: ")
                    bonus = get_valid_float("Bonus: ")
                    deductions = get_valid_float("Deductions: ")
                    
                    success, msg = PayrollService.generate_payroll(emp_id, month, basic, allowances, bonus, deductions)
                    print(msg)
                    
            elif choice == '2':
                emp_id = input("Employee ID: ").strip()
                records = PayrollService.get_payroll_by_employee(emp_id)
                print_table(records, ["month", "basic_salary", "allowances", "bonus", "deductions", "net_salary"])
                
            elif choice == '0':
                break
            else:
                print("Invalid choice.")
                
            if choice != '0':
                input("Press Enter to continue...")

    def reports_menu(self):
        while True:
            print_header("REPORTS & ANALYTICS")
            print("1. Export Monthly Payroll to CSV")
            print("2. Export Employee List to CSV")
            print("0. Back to Main Menu")
            print("-" * 60)
            
            choice = input("Enter choice: ").strip()
            
            if choice == '1':
                month = input("Month (YYYY-MM): ").strip()
                records = PayrollService.get_all_payroll_by_month(month)
                if records:
                    filename = f"payroll_{month}.csv"
                    headers = ["payroll_id", "employee_id", "name", "month", "net_salary"]
                    export_to_csv(filename, records, headers)
                else:
                    print("No payroll data for this month.")
            
            elif choice == '2':
                employees = EmployeeService.get_all_employees()
                if employees:
                    filename = "employees.csv"
                    headers = ["employee_id", "name", "email", "department_name", "designation", "status"]
                    export_to_csv(filename, employees, headers)
                else:
                    print("No employees to export.")
                    
            elif choice == '0':
                break
            else:
                print("Invalid choice.")
                
            if choice != '0':
                input("Press Enter to continue...")

    def user_management(self):
        while True:
            print_header("USER MANAGEMENT (Admin)")
            print("1. Create New User")
            print("0. Back to Main Menu")
            print("-" * 60)
            
            choice = input("Enter choice: ").strip()
            
            if choice == '1':
                username = input("New Username: ").strip()
                password = getpass("New Password: ").strip()
                role = input("Role (Admin, HR, Employee): ").strip().capitalize()
                
                if role in ['Admin', 'HR', 'Employee']:
                    if create_user(username, password, role):
                        print("User created successfully.")
                    else:
                        print("Username already exists.")
                else:
                    print("Invalid role.")
            
            elif choice == '0':
                break
            else:
                print("Invalid choice.")
                
            if choice != '0':
                input("Press Enter to continue...")

if __name__ == "__main__":
    app = EmployeeHubApp()
    try:
        app.run()
    except KeyboardInterrupt:
        print("\nExiting EmployeeHub. Goodbye!")
        sys.exit(0)
