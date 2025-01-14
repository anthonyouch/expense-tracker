# Design Rationale: Expense Tracker

## The Problem

In Version 1, I created a console-based Expense Tracker that writes data to a CSV file. This worked well for personal use and small data sets, but I realized a few limitations:

1. Scalability: CSV files can become cumbersome or corrupt as data grows.
2. Multi-User Support: I’d like to allow multiple users or accounts, but CSV storage doesn’t handle concurrency or user-based data separation well.
3. Recurring Transactions & Advanced Queries: Features like automatic monthly bills or filtering expenses by category/date are easier to implement with a proper database.
4. Robust Reporting: Summaries and analyses (e.g., top categories, monthly breakdowns, trending spend) require more powerful data manipulation than CSV can efficiently handle.

To address these limitations, Version 2 focuses on database integration and backend feature enhancements—all while keeping it console-based to maintain a simple user interface.

---

## The Step-by-Step Process

### 1. Understanding the Problem
- **Why move to a database?**  
  With a growing data set and potential multi-user environment, a database ensures better performance, data integrity, and easier querying.
- **What is lacking in Version 1?**:
  - No concurrency or user concept for multi-user scenarios.
  - Limited reporting and advanced budgeting features.
  - Harder to manage recurring expenses in a CSV-based system.

Solution: Replace CSV with a lightweight database (e.g., SQLite or PostgreSQL), introduce user accounts for separating data, and provide advanced budgeting/reporting features.

---

## 2. Breaking Down the New Features

### Database Integration
- **Rationale**: Improve reliability, allow for structured queries, and scale for more records and potential multi-user usage.  
- **Implementation**:  
  - Set up a `db_storage.py` module containing functions like `read_expenses_db()` and `write_expense_db()`.  
  - Update references in the main app to call the new database functions.

### Recurring Expenses
- **Rationale**: Automatically track monthly bills, subscriptions, or any predictable expenses.  
- **Implementation**:  
  - Allow an expense to be flagged as “recurring” (monthly, weekly, etc.).  
  - Periodically (or upon user action) generate these expenses in the database for the upcoming period.

### Advanced Budgeting & Reporting
- **Rationale**: Offer deeper insights into spending habits—like monthly category totals, top 5 spending categories, or daily averages over time.  
- **Implementation**:  
  - Use SQL queries to aggregate data by category/date range.  
  - Add CLI commands to generate these reports on-demand or automatically.

### Potential User Management (It might be deferred to a future version)
- **Rationale**: Let multiple users each have their own expense records without interfering with each other.  
- **Implementation**:  
  - Create a `users` table to store user credentials (hashed passwords, if security is a concern).  
  - Each expense record references a user ID.  
  - Provide login flow in the CLI.

---

## 3. Designing the Program

### Modular Storage Layer
- **Why separate it?**  
  A dedicated `db_storage.py` keeps database logic isolated from the rest of the code. This makes it easier to maintain or switch databases in the future.

### Database Schema
- **Expenses Table**: `id`, `user_id`, `name`, `category`, `amount`, `date`, `recurring_flag`, etc.  
- **Users Table**: `id`, `username`, `hashed_password`.

### Command-Line Structure
- Retain the existing menu-based approach from Version 1 (Add Expense, View Expense, Summarize, Show Budget, etc.).  
- Add new options or submenus if needed (e.g., “Manage Recurring Expenses,” “Generate Advanced Reports”).  

### Error Handling and Validation
- Validate user input, especially for amounts, categories, and recurring intervals.  
- Handle database exceptions (e.g., connection issues) gracefully, with meaningful console messages.

---

## Future Enhancements (Beyond Version 2)

Although Version 2 prioritizes database integration and backend features, future versions might include:

### Front-End/Web Interface
- Use a framework like **Flask** or **Django** to offer a web-based UI, making the application more accessible.

### Automated Alerts/Notifications
- Send email or push notifications when nearing budget limits or upon receiving large expenses.

### Data Visualization
- Incorporate advanced charts (e.g., bar or pie charts) to display monthly spending, category trends, etc.

### Cloud Integration
- Deploy to a cloud server for real-time access across multiple devices.

---

## Reflection

This second iteration evolves from a minimal CSV-based script into a more robust application capable of handling larger datasets, recurring expenses, and multiple user accounts—all while remaining console-based. By focusing on **database integration**, it not only addresses the scalability and shortcomings of Version 1 but also sets the stage for future expansions, such as web interfaces or advanced analytics.


