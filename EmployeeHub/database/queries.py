CREATE_USERS_TABLE = """
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    role TEXT NOT NULL CHECK(role IN ('Admin', 'HR', 'Employee'))
);
"""

CREATE_DEPARTMENTS_TABLE = """
CREATE TABLE IF NOT EXISTS departments (
    department_id INTEGER PRIMARY KEY AUTOINCREMENT,
    department_name TEXT UNIQUE NOT NULL
);
"""

CREATE_EMPLOYEES_TABLE = """
CREATE TABLE IF NOT EXISTS employees (
    employee_id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    phone TEXT,
    department_id INTEGER,
    designation TEXT,
    joining_date TEXT,
    salary REAL,
    status TEXT DEFAULT 'Active' CHECK(status IN ('Active', 'Inactive', 'Terminated')),
    FOREIGN KEY(department_id) REFERENCES departments(department_id)
);
"""

CREATE_ATTENDANCE_TABLE = """
CREATE TABLE IF NOT EXISTS attendance (
    attendance_id INTEGER PRIMARY KEY AUTOINCREMENT,
    employee_id TEXT NOT NULL,
    date TEXT NOT NULL,
    check_in TEXT,
    check_out TEXT,
    status TEXT CHECK(status IN ('Present', 'Absent', 'Late')),
    FOREIGN KEY(employee_id) REFERENCES employees(employee_id),
    UNIQUE(employee_id, date)
);
"""

CREATE_LEAVE_REQUESTS_TABLE = """
CREATE TABLE IF NOT EXISTS leave_requests (
    leave_id INTEGER PRIMARY KEY AUTOINCREMENT,
    employee_id TEXT NOT NULL,
    leave_type TEXT NOT NULL,
    start_date TEXT NOT NULL,
    end_date TEXT NOT NULL,
    reason TEXT,
    status TEXT DEFAULT 'Pending' CHECK(status IN ('Pending', 'Approved', 'Rejected')),
    FOREIGN KEY(employee_id) REFERENCES employees(employee_id)
);
"""

CREATE_PAYROLL_TABLE = """
CREATE TABLE IF NOT EXISTS payroll (
    payroll_id INTEGER PRIMARY KEY AUTOINCREMENT,
    employee_id TEXT NOT NULL,
    month TEXT NOT NULL,  -- Format: YYYY-MM
    basic_salary REAL NOT NULL,
    allowances REAL DEFAULT 0,
    bonus REAL DEFAULT 0,
    deductions REAL DEFAULT 0,
    net_salary REAL NOT NULL,
    FOREIGN KEY(employee_id) REFERENCES employees(employee_id),
    UNIQUE(employee_id, month)
);
"""

CREATE_TABLES = [
    CREATE_USERS_TABLE,
    CREATE_DEPARTMENTS_TABLE,
    CREATE_EMPLOYEES_TABLE,
    CREATE_ATTENDANCE_TABLE,
    CREATE_LEAVE_REQUESTS_TABLE,
    CREATE_PAYROLL_TABLE
]
