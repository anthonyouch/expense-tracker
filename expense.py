class Expense:
    def __init__(self, name, category, amount):
        """
        Initialize an Expense object with a name, category, and amount.
        """
        self.name = name
        self.category = category
        self.amount = amount

    def to_dict(self):
        """
        Convert the expense to a dictionary format.
        Useful for writing to CSV files.
        """
        return {
            "name": self.name,
            "category": self.category,
            "amount": self.amount
        }

    def __str__(self):
        """
        Return a human-readable string representation of the expense.
        """
        return f"{self.name} ({self.category}): ${self.amount}"
