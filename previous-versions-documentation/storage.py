import csv
from decimal import Decimal

def read_expenses(file_path="expenses.csv"):
    """
    Reads expenses from a CSV file and returns them as a list of dictionaries.
    If the file doesn't exist, returns an empty list.
    """
    try:
        with open(file_path, mode="r") as file:
            reader = csv.DictReader(file)
            return list(reader)
    except FileNotFoundError:
        return []  # No file yet, return empty
    except Exception as e:
        print(f"An error occurred while reading the file: {e}")
        return []


def write_expense(expense, file_path="expenses.csv"):
    """
    Appends a single expense (as a dict) to the CSV file.
    Creates the file and writes a header if it doesn't exist or is empty.
    """
    try:
        with open(file_path, mode="a", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=["name", "category", "amount"])
            if file.tell() == 0:
                writer.writeheader()
            writer.writerow(expense)
    except Exception as e:
        print(f"An error occurred while writing to the file: {e}")