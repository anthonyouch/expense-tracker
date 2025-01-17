
import sqlite3
from decimal import Decimal
import datetime


def initialize_db(db_name="expenses.db"):
    """
    Initialize the database and create the `expenses` table 
    with support for recurring expenses.
    """
    try:
        with sqlite3.connect(db_name) as conn:
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
            print(f"Database initialized successfully: {db_name}")
    except sqlite3.Error as e:
        print(f"Error initializing database: {e}")


def write_expense(expense, db_name="expenses.db"):
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
        if not expense.get("date_added"):
            raise ValueError("The 'date_added' field is required.")

        with sqlite3.connect(db_name) as conn:
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
    except ValueError as ve:
        print(f"Validation Error: {ve}")
    except sqlite3.Error as e:
        print(f"Error adding expense: {e}")




def read_expenses(db_name="expenses.db"):
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
        with sqlite3.connect(db_name) as conn:
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


def process_recurring_expenses(db_name="expenses.db"):
    """
    Processes all recurring expenses and adds a new instance if needed.
    Updates the `date_added` field for recurring expenses after processing.
    """
    try:
        today = datetime.date.today()

        with sqlite3.connect(db_name) as conn:
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


def get_weekly_expenses(db_name="expenses.db"):
    """
    Retrieve all expenses from the past week.

    Args:
        db_name (str): The name of the database.

    Returns:
        list[dict]: A list of dictionaries, each representing an expense.
    """
    try:
        with sqlite3.connect(db_name) as conn:
            cursor = conn.cursor()

            # Calculate the date 7 days ago
            today = datetime.date.today()
            last_week = today - datetime.timedelta(days=7)

            # Query for expenses in the past week
            cursor.execute("""
                SELECT name, category, amount, date_added, recurring, recurring_schedule
                FROM expenses
                WHERE date(date_added) >= date(?) AND date(date_added) <= date(?)
            """, (last_week, today))

            rows = cursor.fetchall()

        # Convert rows to a list of dictionaries
        weekly_expenses = [
            {
                "name": row[0],
                "category": row[1],
                "amount": float(row[2]),
                "date_added": row[3],
                "recurring": bool(row[4]),  # Convert to boolean for clarity
                "recurring_schedule": row[5],
            }
            for row in rows
        ]
        return weekly_expenses

    except sqlite3.Error as e:
        print(f"Error fetching weekly expenses: {e}")
        return []


def get_monthly_expenses_amount(db_name="expenses.db"):
    """
    Calculate the total expenses for the current month.

    Args:
        db_name (str): Name of the database file.

    Returns:
        float: Total expenses for the current month.
    """
    try:
        with sqlite3.connect(db_name) as conn:
            cursor = conn.cursor()
            # Get current month and year
            current_month = datetime.datetime.now().strftime("%Y-%m")
            
            # Query expenses for the current month
            cursor.execute("""
                SELECT SUM(CAST(amount AS REAL)) 
                FROM expenses 
                WHERE strftime('%Y-%m', date_added) = ?
            """, (current_month,))
            total = cursor.fetchone()[0]
            return total if total else 0.0
    except sqlite3.Error as e:
        print(f"Error calculating monthly expenses: {e}")
        return 0.0

def get_weekly_expenses_amount(db_name="expenses.db"):
    """
    Calculate the total expenses amount for the current week (Monday to Sunday).

    Args:
        db_name (str): Name of the database file.

    Returns:
        float: Total expenses for the current week.
    """
    try:
        with sqlite3.connect(db_name) as conn:
            cursor = conn.cursor()
            
            # Get the current week and year
            current_year_week = datetime.datetime.now().strftime("%Y-%W")
            
            # Query for the total expenses for the current week
            cursor.execute("""
                SELECT SUM(CAST(amount AS REAL))
                FROM expenses
                WHERE strftime('%Y-%W', date_added) = ?
            """, (current_year_week,))
            total = cursor.fetchone()[0]
            return total if total else 0.0
    except sqlite3.Error as e:
        print(f"Error calculating weekly expenses: {e}")
        return 0.0