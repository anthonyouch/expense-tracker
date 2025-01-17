# Expense Tracker

A simple **Flask** web application that allows you to track daily, weekly, and monthly expenses. You can add new expenses, view them in a dashboard, and delete them as needed. The project uses **SQLite** for data storage.

**Live Demo**: [anton8do1.pythonanywhere.com](https://anton8do1.pythonanywhere.com/)

---

## Features

1. **Add Expenses**: Insert new expenses with name, category, amount.
2. **View Expenses**:
   - **Dashboard (index)**: Shows recent (past 7 days) and future expenses, as well as daily, weekly, and monthly totals.
   - **All Expenses (view_expenses)**: Shows *all* expenses in a dedicated table.
3. **Delete Expenses**: Remove any expense by clicking a “Delete” button.
5. **SQLite Persistence**: Stores all expenses in a local `expenses.db` file.

---

## Screenshots

---

## Installation

1) Create a directory and clone the repo in it:
```
git clone https://github.com/anthonyouch/expense-tracker.git
```
2) Create your virtual environment:
```
python -m venv env
```
3) Activate your virtual environment:
```
env\Scripts\activate
```
4) Install the dependencies:
```
pip install -r requirements.txt
```
5) Run the Flask app
```
python app.py
```
## Discussion
This project started as part of my application for the ON-HIT student team, However I plan to return to this project in the future and polish it further into a portfolio-worthy application. Some other improvements include:
  * Switching to a more robust database such as PostgreSQL
  * Implementing user authentication
  * More Testing 
  * Improved UI/UX
  * Include recurring expenses. 
  * Data visualizations
