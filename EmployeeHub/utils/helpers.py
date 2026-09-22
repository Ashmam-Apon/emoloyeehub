import os
from tabulate import tabulate

def clear_screen():
    """Clear the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header(title):
    """Print a formatted header."""
    clear_screen()
    print("=" * 60)
    print(title.center(60))
    print("=" * 60)

def print_table(data, headers):
    """Print data in a formatted table."""
    if not data:
        print("No records found.")
    else:
        print(tabulate(data, headers=headers, tablefmt="grid"))
    print("\n")

def generate_employee_id(last_id):
    """Generate the next employee ID (e.g., EMP001)."""
    if not last_id:
        return "EMP001"
    
    # Extract the numeric part and increment
    try:
        num_part = int(last_id.replace("EMP", ""))
        return f"EMP{num_part + 1:03d}"
    except ValueError:
        return "EMP001"
