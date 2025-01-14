import os
import sqlite3
import unittest
from unittest.mock import patch
import datetime

from db_storage import initialize_db, write_expense, read_expenses, process_recurring_expenses


class TestDBStorage(unittest.TestCase):
    TEST_DB = "test_expenses.db"

    def setUp(self):
        """
        Runs before each test. Initializes a fresh test database.
        """
        initialize_db(self.TEST_DB)

    def tearDown(self):
        """
        Runs after each test. Removes the test database.
        """
        if os.path.exists(self.TEST_DB):
            os.remove(self.TEST_DB)

    def test_initialize_db(self):
        """
        Test that the database initializes correctly.
        """
        with sqlite3.connect(self.TEST_DB) as conn:
            cursor = conn.cursor()

            # Check if the expenses table exists
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='expenses';")
            result = cursor.fetchone()
            self.assertIsNotNone(result)

    def test_write_expense(self):
        """
        Test writing an expense to the database.
        """
        expense = {
            "name": "Lunch",
            "category": "Food",
            "amount": "12.50",
            "date_added": "2025-01-15",
            "recurring": 0,
            "recurring_schedule": None
        }

        # Write the expense
        write_expense(expense, self.TEST_DB)

        # Verify the expense was added
        with sqlite3.connect(self.TEST_DB) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM expenses")
            rows = cursor.fetchall()

        self.assertEqual(len(rows), 1)  # One expense added
        self.assertEqual(rows[0][1], expense["name"])  # Name matches
        self.assertEqual(rows[0][2], expense["category"])  # Category matches
        self.assertEqual(rows[0][3], expense["amount"])  # Amount matches

    def test_read_expenses(self):
        """
        Test reading expenses from the database.
        """
        expenses = [
            {
                "name": "Lunch",
                "category": "Food",
                "amount": "12.50",
                "date_added": "2025-01-15",
                "recurring": 0,
                "recurring_schedule": None
            },
            {
                "name": "Bus Ticket",
                "category": "Transport",
                "amount": "2.75",
                "date_added": "2025-01-15",
                "recurring": 0,
                "recurring_schedule": None
            }
        ]

        # Write the expenses
        for expense in expenses:
            write_expense(expense, self.TEST_DB)

        # Read the expenses
        result = read_expenses(self.TEST_DB)

        # Verify the expenses match
        self.assertEqual(len(result), len(expenses))
        for i, expense in enumerate(expenses):
            self.assertEqual(result[i]["name"], expense["name"])
            self.assertEqual(result[i]["category"], expense["category"])
            self.assertEqual(result[i]["amount"], expense["amount"])


class TestRecurringExpenses(unittest.TestCase):
    TEST_DB = "test_expenses.db"

    def setUp(self):
        # Initialize a test database
        initialize_db(self.TEST_DB)

        # Write a recurring expense to the database
        self.recurring_expense = {
            "name": "Gym Membership",
            "category": "Health",
            "amount": "50",
            "date_added": "2025-01-01",
            "recurring": 1,
            "recurring_schedule": "daily"
        }
        write_expense(self.recurring_expense, self.TEST_DB)

    def tearDown(self):
        # Remove the test database file
        if os.path.exists(self.TEST_DB):
            os.remove(self.TEST_DB)

    def test_process_recurring_expenses(self):
        # Mock only the `today` method of `datetime.date`
        class MockDate(datetime.date):
            @classmethod
            def today(cls):
                return cls(2025, 1, 2)

        with patch('datetime.date', MockDate):
            # Call the function to process recurring expenses
            process_recurring_expenses(self.TEST_DB)

        # Verify that the recurring expense was processed
        expenses = read_expenses(self.TEST_DB)
        self.assertEqual(len(expenses), 2)  # Original + new recurring expense
        self.assertEqual(expenses[-1]["date_added"], "2025-01-02")  # Date of the new recurring expense
        self.assertEqual(expenses[-1]["name"], "Gym Membership")  # Check if it's the same expense


if __name__ == "__main__":
    unittest.main()
