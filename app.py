from flask import Flask, render_template, request, redirect, url_for
from db_storage import initialize_db, write_expense, read_expenses, process_recurring_expenses
from datetime import date
# Initialize Flask app
app = Flask(__name__)

# Database setup
DB_NAME = "expenses.db"
initialize_db(DB_NAME)  # Initialize the database

@app.route("/")
def dashboard():
    """
    Render the dashboard with data from the database.
    """
    # Placeholder data - calculate total expenses, etc.
    expenses = read_expenses(DB_NAME)
    total_expenses = sum(float(expense["amount"]) for expense in expenses)
    monthly_breakdown = {}  # Logic for monthly breakdown (to be implemented later)
    category_breakdown = {}  # Logic for category breakdown (to be implemented later)
    today = date.today()

    return render_template(
        "index.html",
        total_expenses=total_expenses,
        monthly_breakdown=monthly_breakdown,
        category_breakdown=category_breakdown,
        today=today,
    )

@app.route("/view-expenses")
def view_expenses():
    """
    Render the View Expenses page with all expenses.
    """
    expenses = read_expenses(DB_NAME)
    return render_template("view_expenses.html", expenses=expenses)

@app.route("/add-expense", methods=["POST"])
def add_expense():
    """
    Handle adding a new expense.
    """
    name = request.form.get("name")
    category = request.form.get("category")
    amount = request.form.get("amount")
    recurring = int(request.form.get("recurring", 0))
    recurring_schedule = request.form.get("recurring_schedule", None)

    # Create an expense object
    expense = {
        "name": name,
        "category": category,
        "amount": amount,
        "date_added": request.form.get("date_added", None),  # Default to today
        "recurring": recurring,
        "recurring_schedule": recurring_schedule,
    }

    # Save to the database
    write_expense(expense, DB_NAME)

    # Redirect to the dashboard
    return redirect(url_for("dashboard"))

@app.route("/process-recurring", methods=["POST"])
def process_recurring():
    """
    Endpoint to process recurring expenses.
    """
    process_recurring_expenses(DB_NAME)
    return redirect(url_for("dashboard"))

if __name__ == "__main__":
    app.run(debug=True)
