
import sqlite3
from decimal import Decimal
import datetime

DB_NAME = "expenses.db"

def initialize_db():
    """
    Initialize the database and create the `expenses` table 
    with support for recurring expenses.
    """
    try:
        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()

            # Create the expenses table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS expenses (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    category TEXT NOT NULL,
                    amount TEXT NOT NULL,
                    date_added TEXT DEFAULT (DATE('now')),
                    recurring INTEGER DEFAULT 0,
                    recurring_schedule TEXT
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
        expense (dict): A dictionary with keys:
            - 'name': Name of the expense.
            - 'category': Category of the expense.
            - 'amount': Amount of the expense.
            - 'date_added': Date the expense was added (e.g., '2025-01-14').
            - 'recurring': (optional) 0 for non-recurring, 1 for recurring.
            - 'recurring_schedule': (optional) Recurrence schedule (e.g., 'weekly', 'monthly').
    """
    try:
        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO expenses (name, category, amount, date_added, recurring, recurring_schedule)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                expense["name"],
                expense["category"],
                expense["amount"],
                expense["date_added"],
                expense.get("recurring", 0),  # Default to non-recurring
                expense.get("recurring_schedule", None)  # Default to None
            ))
            conn.commit()
            print(f"Expense '{expense['name']}' added successfully!")
    except sqlite3.Error as e:
        print(f"Error adding expense: {e}")



def read_expenses():
    """
    Retrieve all expenses from the database.

    Returns:
        list[dict]: A list of dictionaries, each representing an expense with keys:
            - 'name': Name of the expense.
            - 'category': Category of the expense.
            - 'amount': Amount of the expense.
            - 'date_added': Date the expense was added.
            - 'recurring': Whether the expense is recurring (0 or 1).
            - 'recurring_schedule': Recurrence schedule (e.g., 'weekly', 'monthly').
    """
    try:
        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT name, category, amount, date_added, recurring, recurring_schedule
                FROM expenses
            """)
            rows = cursor.fetchall()

        # Convert rows to a list of dictionaries
        expenses = [
            {
                "name": row[0],
                "category": row[1],
                "amount": row[2],
                "date_added": row[3],
                "recurring": row[4],
                "recurring_schedule": row[5],
            }
            for row in rows
        ]
        return expenses
    except sqlite3.Error as e:
        print(f"Error reading expenses: {e}")
        return []


def process_recurring_expenses():
    """
    Processes all recurring expenses and adds a new instance if needed.
    Updates the `date_added` field for recurring expenses after processing.
    """
    try:
        today = datetime.date.today()

        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()

            # Fetch all recurring expenses
            cursor.execute("""
                SELECT id, name, category, amount, date_added, recurring_schedule 
                FROM expenses 
                WHERE recurring = 1
            """)
            recurring_expenses = cursor.fetchall()

            for expense in recurring_expenses:
                expense_id, name, category, amount, date_added, schedule = expense
                date_added = datetime.datetime.strptime(date_added, "%Y-%m-%d").date()

                # Determine if the expense needs to recur based on the schedule
                if schedule == "daily":
                    next_occurrence = date_added + datetime.timedelta(days=1)
                elif schedule == "weekly":
                    next_occurrence = date_added + datetime.timedelta(weeks=1)
                elif schedule == "monthly":
                    # Add one month by using the calendar module
                    year, month = date_added.year, date_added.month
                    next_month = (month % 12) + 1
                    year += (month + 1) // 13
                    next_occurrence = date_added.replace(year=year, month=next_month)

                # If today matches or exceeds the next occurrence, add the expense
                if next_occurrence <= today:
                    # Add a new expense for today
                    cursor.execute("""
                        INSERT INTO expenses (name, category, amount, date_added, recurring, recurring_schedule)
                        VALUES (?, ?, ?, ?, ?, ?)
                    """, (name, category, amount, today.strftime("%Y-%m-%d"), 1, schedule))

                    # Update the `date_added` field for the original expense
                    cursor.execute("""
                        UPDATE expenses
                        SET date_added = ?
                        WHERE id = ?
                    """, (today.strftime("%Y-%m-%d"), expense_id))

            conn.commit()
            print("Recurring expenses processed successfully.")

    except sqlite3.Error as e:
        print(f"Error processing recurring expenses: {e}")
