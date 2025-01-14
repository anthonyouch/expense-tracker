# App Requirements: Expense Tracker (Version 1)

## Core Features
1. **User Enters Expense**
   - The user can input the following details for an expense:
     - `Name`: A description of the expense (e.g., "Groceries").
     - `Category`: The category of the expense (e.g., "Food", "Transport").
     - `Amount`: The cost of the expense.

2. **Save Expense to CSV File**
   - Each expense will be saved as a new row in a file named `expenses.csv`.
   - The file will include the following fields:
     - `Name`, `Category`, and `Amount`.

3. **Summarize Expense Totals**
   - The app will calculate the total amount spent across all expenses.
   - This summary will be displayed when the user views expenses.

4. **Show Remaining Budget**
   - The user can set a monthly budget.
   - The app will calculate and display the remaining budget:
     ```
     Remaining Budget = Monthly Budget - Total Expenses
     ```

---

## User Flow
1. **Add Expense**:
   - The user enters the expense details.
   - The expense is saved to `expenses.csv`.

2. **View Summary**:
   - Display all recorded expenses from `expenses.csv`.
   - Calculate and show the total expenses.
   - Calculate and display the remaining budget.

3. **Exit**:
   - The user can exit the app.

---

## Constraints
- The app will run in the terminal (console-based).
- Data will be stored in a CSV file for simplicity.
- The app will not include advanced features like filtering or sorting in version 1.

---

## Technical Design
1. **Expense Class**
   - Attributes:
     - `name`: Name of the expense.
     - `category`: Category of the expense.
     - `amount`: Cost of the expense.
     - `date` (Optional): Date the expense was added (default: today's date).

2. **CSV File Structure**
   The `expenses.csv` file will store data in the following format:

   | Name       | Category      | Amount |
   |------------|---------------|--------|
   | Groceries  | Food          | 50.00  |
   | Bus Ticket | Transport     | 2.50   |

---

## Error Handling
- Ensure that the `amount` field is numeric.
- Prompt the user again if mandatory fields (`name`, `category`) are left empty.
