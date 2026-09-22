class Payroll:
    def __init__(self, payroll_id, employee_id, month, basic_salary, allowances=0, bonus=0, deductions=0, net_salary=0):
        self.payroll_id = payroll_id
        self.employee_id = employee_id
        self.month = month
        self.basic_salary = float(basic_salary) if basic_salary is not None else 0.0
        self.allowances = float(allowances) if allowances is not None else 0.0
        self.bonus = float(bonus) if bonus is not None else 0.0
        self.deductions = float(deductions) if deductions is not None else 0.0
        self.net_salary = float(net_salary) if net_salary is not None else 0.0

    @staticmethod
    def calculate_net_salary(basic_salary, allowances, bonus, deductions):
        gross_salary = basic_salary + allowances + bonus
        return gross_salary - deductions
