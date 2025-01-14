
import sqlite3
from decimal import Decimal

DB_NAME = "expenses.db"

def initialize_db():
    """
    Initialize the database and create the necessary tables 
    if they do not exist.
    """
    try:
        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()
            
            # Create the expenses table if it doesn't already exist
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS expenses (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    category TEXT NOT NULL,
                    amount TEXT NOT NULL,
                    date_added TEXT DEFAULT (DATE('now'))
                )
            """)
            conn.commit()

        print(f"Database initialized successfully: {DB_NAME}")
    except sqlite3.Error as e:
        print(f"Error initializing database: {e}")

def write_expense(expense):
    """
    Add a new expense to the database.
    
    Args:
        expense (dict): A dictionary with keys 'name', 'category', and 'amount'.
    """
    pass

def read_expenses():
    """
    Retrieve all expenses from the database.

    Returns:
        list[dict]: A list of dictionaries, each representing an expense.
    """
    pass

def summarize_expenses():
    """
    Calculate the total amount spent across all recorded expenses.

    Returns:
        Decimal: The total amount spent.
    """
    pass
