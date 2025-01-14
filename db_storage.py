
import sqlite3
from decimal import Decimal

DB_NAME = "expenses.db"

def initialize_db():
    """
    Initialize the database and create the necessary tables 
    if they do not exist.
    """
    pass

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
