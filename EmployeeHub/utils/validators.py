import re
from datetime import datetime

def is_valid_email(email):
    """Validate email format."""
    pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return re.match(pattern, email) is not None

def is_valid_date(date_str):
    """Validate date format (YYYY-MM-DD)."""
    try:
        datetime.strptime(date_str, '%Y-%m-%d')
        return True
    except ValueError:
        return False

def get_valid_input(prompt, validator, error_msg):
    """Repeatedly ask for input until it passes the validator."""
    while True:
        value = input(prompt).strip()
        if validator(value):
            return value
        print(f"Error: {error_msg}")

def get_valid_float(prompt):
    """Repeatedly ask for input until a valid float is provided."""
    while True:
        value = input(prompt).strip()
        try:
            return float(value)
        except ValueError:
            print("Error: Please enter a valid number.")

def is_valid_phone(phone):
    """Basic validation for phone numbers (digits, optional +, -, spaces)."""
    pattern = r"^\+?[0-9\s-]+$"
    return re.match(pattern, phone) is not None
