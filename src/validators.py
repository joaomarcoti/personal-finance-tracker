"""Input validation helpers.

Every function receives the raw text typed by the user (or read from the CSV
file), returns a clean value and raises ValueError with a friendly message
when the input is not acceptable.
"""

import math
from datetime import datetime

MAX_DESCRIPTION_LENGTH = 100
MAX_CATEGORY_LENGTH = 30
MAX_AMOUNT = 1_000_000_000


def validate_description(text):
    """Return the description without extra spaces around it."""
    description = text.strip()
    if not description:
        raise ValueError("The description cannot be empty.")
    if len(description) > MAX_DESCRIPTION_LENGTH:
        raise ValueError(
            f"The description must have at most {MAX_DESCRIPTION_LENGTH} characters."
        )
    return description


def validate_category(text):
    """Return the category in a standard format (e.g. ' fOOD ' -> 'Food')."""
    category = text.strip()
    if not category:
        raise ValueError("The category cannot be empty.")
    if len(category) > MAX_CATEGORY_LENGTH:
        raise ValueError(
            f"The category must have at most {MAX_CATEGORY_LENGTH} characters."
        )
    return category.capitalize()


def validate_amount(text):
    """Return the amount as a float with 2 decimal places.

    Both '25.90' and '25,90' are accepted.
    """
    cleaned = text.strip().replace(",", ".")
    try:
        amount = float(cleaned)
    except ValueError:
        raise ValueError("The amount must be a number, like 25.90.") from None

    if not math.isfinite(amount):
        raise ValueError("The amount must be a valid number.")

    amount = round(amount, 2)
    if amount <= 0:
        raise ValueError("The amount must be greater than zero.")
    if amount > MAX_AMOUNT:
        raise ValueError("The amount is too large.")
    return amount


def validate_date(text):
    """Return the date as an ISO string (YYYY-MM-DD)."""
    try:
        parsed = datetime.strptime(text.strip(), "%Y-%m-%d")
    except ValueError:
        raise ValueError(
            "The date must be valid and use the format YYYY-MM-DD, like 2026-11-10."
        ) from None
    return parsed.date().isoformat()


def validate_month(text):
    """Return the month as a string in the format YYYY-MM."""
    try:
        parsed = datetime.strptime(text.strip(), "%Y-%m")
    except ValueError:
        raise ValueError(
            "The month must use the format YYYY-MM, like 2026-11."
        ) from None
    return parsed.strftime("%Y-%m")


def validate_expense_id(text):
    """Return the expense ID as a positive integer."""
    try:
        expense_id = int(text.strip())
    except ValueError:
        raise ValueError("The ID must be a whole number.") from None
    if expense_id <= 0:
        raise ValueError("The ID must be a positive number.")
    return expense_id
