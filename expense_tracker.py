"""
Core functionality for the Expense Tracker application.
Handles adding, viewing, and summarizing expenses.

For detailed requirements and features, refer to requirements.md.
"""

import datetime
import calendar
from decimal import Decimal


from storage import read_expenses, write_expense
from db_storage import *

from expense import Expense 



def main():

    initialize_db()

    while True:
        print("\nWelcome to the Expense Tracker!")
        print("1. Add Expense")
        print("2. View Expenses")
        print("3. Summarize Expenses")
        print("4. Show Remaining Budget")
        print("5. Exit")

        choice = input("Choose an option (1-5): ").strip()
        if choice == "1":
            add_expense()
        elif choice == "2":
            view_expenses()
        elif choice == "3":
            summarize_expenses()
        elif choice == "4":
            show_remaining_budget()
        elif choice == "5":
            confirm = input("Are you sure you want to exit? (y/n): ").lower()
            if confirm == 'y':
                print("Goodbye!")
                break
            else:
                continue
        else:
            print("Invalid choice. Please try again.")


def add_expense():
    """
    Collects user input for an expense (name and amount),
    allows the user to select a category from a predefined list,
    creates an Expense object, and saves it to a CSV file.
    """
    try:
        # Get user input for the expense details
        name = input("Enter the expense name: ").strip()
        if not name:
            print("Expense name cannot be empty.")
            return

        amount_str = input("Enter the expense amount: ").strip()
        amount = Decimal(amount_str)  # Use Decimal for money
        if amount < 0:
            print("Amount cannot be negative. Please try again.")
            return

        # Predefined list of categories
        categories = ["Food", "Transport", "Entertainment", "Utilities", "Other"]
        print("\nSelect a category:")
        for i, category in enumerate(categories, 1):
            print(f"{i}. {category}")

        # Get the user's category choice
        while True:
            try:
                category_choice = int(input("Choose a category (1-5): "))
                if 1 <= category_choice <= len(categories):
                    category = categories[category_choice - 1]
                    break
                else:
                    print("Invalid choice. Please choose a number between 1 and 5.")
            except ValueError:
                print("Invalid input. Please enter a number.")

        # Create an Expense object
        expense_obj = Expense(name=name, category=category, amount=str(amount))

        # Save the expense to the CSV file using our helper function
        write_expense(expense_obj.to_dict())

        print(f"Expense '{name}' added successfully in category '{category}'!")

    except ValueError:
        print("Invalid input for amount. Please enter a numeric value.")
    except Exception as e:
        print(f"An error occurred: {e}")


def view_expenses():
    """
    Reads all expenses from the CSV file and displays them 
    in a human-readable tabular format.
    """
    expenses = read_expenses()
    if not expenses:
        print("No expenses recorded yet.")
        return

    # Display the expenses in a table format
    print("\nRecorded Expenses:")
    print(f"{'Name':<20}{'Category':<15}{'Amount':<10}")
    print("-" * 45)
    for expense in expenses:
        print(f"{expense['name']:<20}{expense['category']:<15}${expense['amount']:<10}")


def summarize_expenses():
    """
    Calculates the total amount spent across all recorded expenses 
    and displays the result.
    """
    expenses = read_expenses()
    if not expenses:
        print("No expenses recorded yet.")
        return

    # Calculate the total amount spent (using Decimal for accuracy)
    total_spent = sum(Decimal(expense["amount"]) for expense in expenses)
    print(f"\nTotal amount spent: ${total_spent:.2f}")


def show_remaining_budget():
    """
    Prompts the user to input their monthly budget, calculates the 
    remaining budget based on total expenses, and displays the result.
    Also calculates the remaining daily budget based on the days left 
    in the current month.
    """
    try:
        budget_str = input("Enter your monthly budget: ").strip()
        monthly_budget = Decimal(budget_str)
        if monthly_budget < 0:
            print("Budget cannot be negative.")
            return

        today = datetime.date.today()
        expenses = read_expenses()

        if not expenses:
            print("No expenses recorded yet.")
            print(f"Remaining budget: ${monthly_budget:.2f}")

            # Calculate remaining daily budget
            remaining_days = calendar.monthrange(today.year, today.month)[1] - today.day
            if remaining_days > 0:
                daily_budget = monthly_budget / remaining_days
            else:
                daily_budget = Decimal("0.00")

            print(f"Remaining budget per day: ${daily_budget:.2f}")
            return

        # Calculate the total amount spent
        total_spent = sum(Decimal(expense["amount"]) for expense in expenses)

        # Calculate the remaining budget
        remaining_budget = monthly_budget - total_spent

        # Calculate the remaining daily budget
        last_day_of_month = calendar.monthrange(today.year, today.month)[1]
        remaining_days = last_day_of_month - today.day
        daily_budget = remaining_budget / remaining_days if remaining_days > 0 else Decimal("0.00")

        # Display the results
        print(f"\nTotal spent: ${total_spent:.2f}")
        print(f"Remaining budget: ${remaining_budget:.2f}")
        print(f"Remaining budget per day: ${daily_budget:.2f}")

    except ValueError:
        print("Invalid input. Please enter a numeric value for the budget.")
    except Exception as e:
        print(f"An error occurred while calculating the remaining budget: {e}")


if __name__ == "__main__":
    main()
