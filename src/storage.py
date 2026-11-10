"""Reading and writing expenses in a CSV file."""

import csv
from pathlib import Path

from . import validators

FIELDNAMES = ["id", "description", "amount", "category", "date"]


def _row_to_expense(row):
    """Convert one CSV row (a dict of strings) into an expense dictionary.

    The same validators used for keyboard input are reused here, so a
    damaged row raises ValueError instead of corrupting the data.
    """
    return {
        "id": validators.validate_expense_id(row.get("id") or ""),
        "description": validators.validate_description(row.get("description") or ""),
        "amount": validators.validate_amount(row.get("amount") or ""),
        "category": validators.validate_category(row.get("category") or ""),
        "date": validators.validate_date(row.get("date") or ""),
    }


def load_expenses(file_path):
    """Return the list of expenses stored in the CSV file.

    If the file does not exist yet, an empty list is returned. Invalid rows
    are skipped with a warning, so one bad line does not break the program.
    """
    path = Path(file_path)
    if not path.exists():
        return []

    expenses = []
    with path.open("r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        # Line 1 is the header, so the first expense is on line 2.
        for line_number, row in enumerate(reader, start=2):
            try:
                expenses.append(_row_to_expense(row))
            except ValueError:
                print(f"Warning: skipping invalid row on line {line_number}.")
    return expenses


def save_expenses(file_path, expenses):
    """Write all expenses to the CSV file, replacing its previous content."""
    path = Path(file_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=FIELDNAMES, lineterminator="\n")
        writer.writeheader()
        for expense in expenses:
            row = dict(expense)
            row["amount"] = f"{expense['amount']:.2f}"
            writer.writerow(row)
