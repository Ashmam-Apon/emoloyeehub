class Employee:
    def __init__(self, employee_id, name, email, phone, department_id, designation, joining_date, salary, status='Active'):
        self.employee_id = employee_id
        self.name = name
        self.email = email
        self.phone = phone
        self.department_id = department_id
        self.designation = designation
        self.joining_date = joining_date
        self.salary = float(salary) if salary is not None else 0.0
        self.status = status

    def to_dict(self):
        return {
            'employee_id': self.employee_id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'department_id': self.department_id,
            'designation': self.designation,
            'joining_date': self.joining_date,
            'salary': self.salary,
            'status': self.status
        }
