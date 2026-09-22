import csv
import os

def export_to_csv(filename, data, headers):
    """
    Exports data to a CSV file.
    
    :param filename: Name of the output CSV file
    :param data: List of dictionaries containing the data
    :param headers: List of keys matching the dictionary keys to be exported as columns
    """
    if not data:
        print("No data available to export.")
        return False
        
    filepath = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', filename)
    
    try:
        with open(filepath, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=headers)
            writer.writeheader()
            for row in data:
                # filter row to only include headers
                filtered_row = {k: row.get(k, '') for k in headers}
                writer.writerow(filtered_row)
        print(f"Report successfully exported to: {filepath}")
        return True
    except Exception as e:
        print(f"Error exporting report: {e}")
        return False
