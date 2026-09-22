class LeaveRequest:
    def __init__(self, leave_id, employee_id, leave_type, start_date, end_date, reason, status='Pending'):
        self.leave_id = leave_id
        self.employee_id = employee_id
        self.leave_type = leave_type
        self.start_date = start_date
        self.end_date = end_date
        self.reason = reason
        self.status = status
