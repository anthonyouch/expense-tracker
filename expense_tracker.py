"""
Core functionality for the Expense Tracker application.
Handles adding, viewing, and summarizing expenses.

For detailed requirements and features, refer to requirements.md.
"""

from expense import Expense
import csv  # For file handling
import datetime


def main():
    """
    Main function that serves as the entry point of the application.
    Displays a menu to the user and calls corresponding functions 
    based on the user's choice.
    """
    print("Welcome to the Expense Tracker!")
    print("1. Add Expense")
    print("2. View Expenses")
    print("3. Summarize Expenses")
    print("4. Show Remaining Budget")
    print("5. Exit")
    
    while True:
        choice = input("Choose an option (1-5): ")
        if choice == "1":
            add_expense()
        elif choice == "2":
            view_expenses()
        elif choice == "3":
            summarize_expenses()
        elif choice == "4":
            show_remaining_budget()
        elif choice == "5":
            print("Goodbye!")
            break
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
        amount = float(input("Enter the expense amount: "))

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
        expense = Expense(name=name, category=category, amount=amount)

        # Save the expense to the CSV file
        with open("expenses.csv", mode="a", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=["name", "category", "amount"])
            
            # Write the header if the file is empty
            if file.tell() == 0:
                writer.writeheader()

            # Write the expense to the file
            writer.writerow(expense.to_dict())

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
    try:
        # Open the CSV file in read mode
        with open("expenses.csv", mode="r") as file:
            reader = csv.DictReader(file)

            # Check if the file is empty
            expenses = list(reader)
            if not expenses:
                print("No expenses recorded yet.")
                return

            # Display the expenses in a table format
            print("\nRecorded Expenses:")
            print(f"{'Name':<20}{'Category':<15}{'Amount':<10}")
            print("-" * 45)
            for expense in expenses:
                print(f"{expense['name']:<20}{expense['category']:<15}${expense['amount']:<10}")
    except FileNotFoundError:
        print("No expenses found. Start by adding some!")
    except Exception as e:
        print(f"An error occurred while reading expenses: {e}")


def summarize_expenses():
    """
    Calculates the total amount spent across all recorded expenses 
    and displays the result.
    """
    try:
        # Open the CSV file in read mode
        with open("expenses.csv", mode="r") as file:
            reader = csv.DictReader(file)

            # Convert the reader to a list of expenses
            expenses = list(reader)

            # Check if there are no expenses
            if not expenses:
                print("No expenses recorded yet.")
                return

            # Calculate the total amount spent
            total_spent = sum(float(expense["amount"]) for expense in expenses)

            # Display the total amount
            print(f"\nTotal amount spent: ${total_spent:.2f}")

    except FileNotFoundError:
        print("No expenses found. Start by adding some!")
    except Exception as e:
        print(f"An error occurred while summarizing expenses: {e}")


import datetime
import calendar

def show_remaining_budget():
    """
    Prompts the user to input their monthly budget, calculates the 
    remaining budget based on total expenses, and displays the result.
    Also calculates the remaining daily budget based on the days left 
    in the current month.
    """
    try:
        # Get user input for the monthly budget
        monthly_budget = float(input("Enter your monthly budget: "))

        today = datetime.date.today()

        # Open the CSV file in read mode
        try:
            with open("expenses.csv", mode="r") as file:
                reader = csv.DictReader(file)

                # Convert the reader to a list of expenses
                expenses = list(reader)

                # Check if there are no expenses
                if not expenses:
                    print("No expenses recorded yet.")
                    print(f"Remaining budget: ${monthly_budget:.2f}")
                    
                    # Calculate remaining daily budgettoday = datetime.date.today()
                    remaining_days = calendar.monthrange(today.year, today.month)[1] - today.day
                    daily_budget = monthly_budget / remaining_days
                    print(f"Remaining budget per day: ${daily_budget:.2f}")
                    return

                # Calculate the total amount spent
                total_spent = sum(float(expense["amount"]) for expense in expenses)

        except FileNotFoundError:
            print("No expenses found. Start by adding some!")
            print(f"Remaining budget: ${monthly_budget:.2f}")
            
            # Calculate remaining daily budget
            remaining_days = calendar.monthrange(today.year, today.month)[1] - today.day
            daily_budget = monthly_budget / remaining_days
            print(f"Remaining budget per day: ${daily_budget:.2f}")
            return

        # Calculate the remaining budget
        remaining_budget = monthly_budget - total_spent

        # Calculate the remaining daily budget
        last_day_of_month = calendar.monthrange(today.year, today.month)[1]
        remaining_days = last_day_of_month - today.day
        daily_budget = remaining_budget / remaining_days if remaining_days > 0 else 0

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