class Expense:
    def __init__(self, name, category, amount,date_added, recurring=0, recurring_schedule=None):
        """
        Initialize an Expense object with a name, category, amount, and optional
        recurring information.
        """
        self.name = name
        self.category = category
        self.amount = amount
        self.date_added = date_added
        self.recurring = recurring  
        self.recurring_schedule = recurring_schedule 

    def to_dict(self):
        """
        Convert the expense to a dictionary format for database insertion.
        """
        return {
            "name": self.name,
            "category": self.category,
            "amount": self.amount,
            "date_added": self.date_added,
            "recurring": self.recurring,
            "recurring_schedule": self.recurring_schedule,
        }

    def __str__(self):
        """
        Return a human-readable string representation of the expense.
        """
        return (
            f"{self.name} ({self.category}): ${self.amount} "
            f"(Date: {self.date_added}, Recurring: {self.recurring}, Schedule: {self.recurring_schedule})"
        )
