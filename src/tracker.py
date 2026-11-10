"""Core logic of the Personal Finance Tracker.

The functions here only work with the list of expenses in memory. They do not
read files and do not print anything, which makes them easy to test.

Each expense is a dictionary:
    {"id": 1, "description": "Lunch", "amount": 25.5,
     "category": "Food", "date": "2026-11-10"}
"""


def get_next_id(expenses):
    """Return an ID that is not used by any existing expense."""
    if not expenses:
        return 1
    return max(expense["id"] for expense in expenses) + 1


def add_expense(expenses, description, amount, category, date):
    """Create an expense, add it to the list and return it.

    The values must already be validated (see validators.py).
    """
    expense = {
        "id": get_next_id(expenses),
        "description": description,
        "amount": amount,
        "category": category,
        "date": date,
    }
    expenses.append(expense)
    return expense


def sort_expenses(expenses):
    """Return a new list ordered by date (and by ID when dates are equal)."""
    return sorted(expenses, key=lambda expense: (expense["date"], expense["id"]))


def get_total(expenses):
    """Return the sum of all amounts, rounded to 2 decimal places."""
    return round(sum(expense["amount"] for expense in expenses), 2)


def filter_by_category(expenses, category):
    """Return the expenses of a category (upper/lower case is ignored)."""
    wanted = category.strip().lower()
    return [e for e in expenses if e["category"].lower() == wanted]


def filter_by_month(expenses, month):
    """Return the expenses of a month given as 'YYYY-MM'.

    Dates are stored as 'YYYY-MM-DD', so an expense belongs to the month
    when its date starts with that 'YYYY-MM' text.
    """
    return [e for e in expenses if e["date"].startswith(month)]


def delete_expense(expenses, expense_id):
    """Remove the expense with the given ID.

    Return True if it was found and removed, or False otherwise.
    """
    for expense in expenses:
        if expense["id"] == expense_id:
            expenses.remove(expense)
            return True
    return False


def summarize_by_category(expenses):
    """Return a dictionary with the total spent in each category."""
    totals = {}
    for expense in expenses:
        category = expense["category"]
        totals[category] = totals.get(category, 0) + expense["amount"]
    return {category: round(total, 2) for category, total in totals.items()}
