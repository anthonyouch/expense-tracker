# App Requirements: Expense Tracker (Version 2)

## 1. Overview
This version enhances the **console-based Expense Tracker** by introducing **database support**, **advanced budgeting**, and other backend-focused features while retaining the core functionality from Version 1.

---

## 2. Core Features (Extended)

1. **Database Integration**  
   - **Requirement**: Replace CSV storage with a database (e.g., SQLite, PostgreSQL, or other).
   - **Rationale**: Improve scalability, data integrity, and allow more complex operations (queries, concurrency).
   - **Implementation Details**:
     - A new storage layer (`db_storage.py`) with functions like `read_expenses_db()` and `write_expense_db()`.
     - Migrate existing CSV data to the new database tables if needed.

2. **Recurring Expenses**  
   - **Requirement**: Users can mark expenses as “recurring” (e.g., monthly rent, weekly subscription).
   - **Rationale**: Automate addition of repeated expenses and reduce manual input.
   - **Implementation Details**:
     - A column/field `recurring_flag` (boolean) or a `frequency` enum (e.g., `monthly`, `weekly`).
     - A mechanism or command to periodically insert these expenses.

3. **Advanced Budgeting and Reporting**  
   - **Requirement**: Provide more comprehensive summaries (e.g., monthly category totals, top 5 categories, etc.).
   - **Rationale**: Give users deeper insights into spending patterns.
   - **Implementation Details**:
     - Command-line prompts or flags (e.g., `python expense_tracker.py report --monthly`).
     - Queries grouping expenses by category, date range, or user.

4. **Optional User Accounts** (If Implemented in V2)  
   - **Requirement**: Support multiple users with separate expense data.
   - **Rationale**: Enable households or small groups to use the same app while keeping finances distinct.
   - **Implementation Details**:
     - A `users` table with `username` and a hashed `password`.
     - Each expense references a `user_id`.

5. **CLI Interactions**  
   - **Requirement**: Keep the core “menu-driven” flow but optionally allow direct command-line flags.
   - **Rationale**: Power users can skip the interactive prompts; new or casual users can rely on the menu.
   - **Implementation Details**:
     - A library like `argparse` or `click` might be used for advanced flags.
     - Menu-based prompts remain for backward compatibility.

---

## 3. User Flow (High-Level)

1. **Add Expense**  
   - User enters expense details (name, category, amount).  
   - App checks if expense is recurring.  
   - Data is **saved to the database** instead of a CSV.

2. **View Expenses**  
   - App queries the database for all expenses or applies filters (e.g., by date range).  
   - Displays them in a table format in the console.

3. **Summarize Expenses**  
   - App calculates total expenses (and possibly categorizes them for advanced reporting).

4. **Show Remaining Budget**  
   - User inputs monthly budget.  
   - App calculates `Remaining = Budget - TotalSpent`.  
   - Optionally breaks this down by day or warns if close to the limit.

5. **Recurring Expense Generation**  
   - If recurring expenses exist, the app automatically inserts them at the specified intervals (monthly, weekly, etc.).

6. **Exit**  
   - Program ends, optionally asking for confirmation (as in Version 1).

---

## 4. Constraints
- **Console-Based Only**: Version 2 remains an interactive or CLI-driven app; no GUI/front-end.  
- **Database**: Must store and handle data in a reliable manner (transactions, error handling).  
- **No Large-Scale Multi-Server Setup**: This is a local or single-server solution, suitable for individuals or small teams.

---

## 5. Technical Design

1. **Database Schema**  
   - **Tables**:  
     - `expenses` (fields: `id`, `user_id` [optional], `name`, `category`, `amount`, `date`, `recurring_flag`, etc.).  
     - `users` (if multi-user: fields: `id`, `username`, `password_hash`).  
   - **Queries**: Summaries, totals, grouping by category/date.

2. **Modules**  
   - **`db_storage.py`**: Contains functions to create, read, update, and delete expense entries in the DB.  
   - **`main.py`** (or `expense_tracker.py`): Contains the main menu/CLI logic.  
   - **Optional**: A `models.py` or `entities.py` file to define Python classes or data models.

3. **Error Handling**  
   - Graceful handling of database connection issues or invalid queries.  
   - Validation of user input (e.g., amounts must be numeric, categories must exist).

---

## 6. Testing
- **Unit Tests**: For all new database functions (insert, query, etc.) using a local test DB.  
- **Integration Tests**: Verifying the entire flow (Add expense, then Summarize, etc.).  
- **User Acceptance Tests**: Manual checks to ensure the CLI prompts and new features (recurring expenses, advanced reporting) work as expected.
