from flask import Flask, render_template, request, redirect, url_for
from db_storage import initialize_db, write_expense, read_expenses, process_recurring_expenses, get_recent_and_future_expenses, get_weekly_expenses_amount, get_monthly_expenses_amount, delete_expense
from datetime import date
# Initialize Flask app
app = Flask(__name__)

# Database setup
DB_NAME = "expenses.db"
initialize_db(DB_NAME)  # Initialize the database

@app.route('/')
def dashboard():
    today = date.today()
    recent_and_future_expenses = get_recent_and_future_expenses()
    daily_expenses = sum(float(exp['amount']) for exp in recent_and_future_expenses if exp['date_added'] == str(today))
    weekly_total = get_weekly_expenses_amount()
    monthly_total = get_monthly_expenses_amount()

    return render_template(
        'index.html',
        today=today,
        daily_expenses=daily_expenses,
        recent_and_future_expenses=recent_and_future_expenses,
        weekly_total=weekly_total,
        monthly_expenses=monthly_total,
    )


@app.route("/view-expenses")
def view_expenses():
    """
    Render the View Expenses page with all expenses.
    """
    expenses = read_expenses(DB_NAME)
    return render_template("view_expenses.html", expenses=expenses)

@app.route("/add_expense", methods=["POST"])
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



@app.route("/delete_expense/<int:expense_id>", methods=["POST"])
def delete_expense_route(expense_id):
    """
    Route to handle deleting an expense by its ID.
    """
    try:
        delete_expense(expense_id)  # Call the function from db_storage.py
    except Exception as e:
        print(f"Error deleting expense: {e}")
    return redirect("/")


@app.route("/process-recurring", methods=["POST"])
def process_recurring():
    """
    Endpoint to process recurring expenses.
    """
    process_recurring_expenses(DB_NAME)
    return redirect(url_for("dashboard"))

if __name__ == "__main__":
    app.run(debug=True)


