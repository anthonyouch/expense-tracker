"""
Core functionality for the Expense Tracker application.
Handles adding, viewing, and summarizing expenses.

For detailed requirements and features, refer to requirements.md.
"""

from expense import Expense
import csv  # For file handling


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
    in a human-readable format.
    """
    pass

def summarize_expenses():
    """
    Calculates the total amount spent across all recorded expenses 
    and displays the result.
    """
    pass

def show_remaining_budget():
    """
    Prompts the user to input their monthly budget, calculates the 
    remaining budget based on total expenses, and displays the result.
    """
    pass

if __name__ == "__main__":
    main()