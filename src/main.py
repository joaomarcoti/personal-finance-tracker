"""Command-line interface for the Personal Finance Tracker.

Run it from the project root with:
    python -m src.main
"""

from datetime import date
from pathlib import Path

from . import storage, tracker, validators

DATA_FILE = Path(__file__).resolve().parent.parent / "data" / "expenses.csv"

MENU = """
===== Personal Finance Tracker =====
1. Add expense
2. List all expenses
3. Show total spent
4. Filter expenses by category
5. Show expenses by month
6. Delete expense
7. Financial summary by category
0. Exit
"""


def ask(prompt, validator, default=None):
    """Keep asking until the user types a valid value.

    If a default is given, pressing Enter without typing uses it.
    """
    while True:
        raw = input(prompt)
        if raw.strip() == "" and default is not None:
            raw = default
        try:
            return validator(raw)
        except ValueError as error:
            print(f"  Invalid input: {error}")


def save(expenses):
    """Save the expenses to disk. Return True on success."""
    try:
        storage.save_expenses(DATA_FILE, expenses)
        return True
    except OSError as error:
        print(f"Error: could not save the data ({error}).")
        return False


def print_expenses(expenses):
    """Print a list of expenses as a table, followed by their total."""
    if not expenses:
        print("No expenses found.")
        return

    print(f"{'ID':<5}{'Date':<12}{'Category':<16}{'Description':<34}{'Amount':>10}")
    print("-" * 77)
    for expense in tracker.sort_expenses(expenses):
        # The ".15" and ".33" cut long texts so the columns stay aligned.
        print(
            f"{expense['id']:<5}{expense['date']:<12}"
            f"{expense['category']:<16.15}{expense['description']:<34.33}"
            f"{expense['amount']:>10.2f}"
        )
    print("-" * 77)
    print(f"{len(expenses)} expense(s) | Total: {tracker.get_total(expenses):.2f}")


def handle_add(expenses):
    print("\n-- Add expense --")
    description = ask("Description: ", validators.validate_description)
    amount = ask("Amount: ", validators.validate_amount)
    category = ask("Category: ", validators.validate_category)
    today = date.today().isoformat()
    expense_date = ask(
        f"Date (YYYY-MM-DD) [{today}]: ", validators.validate_date, default=today
    )

    tracker.add_expense(expenses, description, amount, category, expense_date)
    if save(expenses):
        print("Expense added and saved.")


def handle_list(expenses):
    print("\n-- All expenses --")
    print_expenses(expenses)


def handle_total(expenses):
    total = tracker.get_total(expenses)
    print(f"\nTotal spent: {total:.2f} ({len(expenses)} expense(s))")


def handle_filter_category(expenses):
    print("\n-- Filter by category --")
    category = ask("Category: ", validators.validate_category)
    print_expenses(tracker.filter_by_category(expenses, category))


def handle_filter_month(expenses):
    print("\n-- Expenses by month --")
    month = ask("Month (YYYY-MM): ", validators.validate_month)
    print_expenses(tracker.filter_by_month(expenses, month))


def handle_delete(expenses):
    print("\n-- Delete expense --")
    if not expenses:
        print("There are no expenses to delete.")
        return

    print_expenses(expenses)
    expense_id = ask("ID of the expense to delete: ", validators.validate_expense_id)

    answer = input(f"Are you sure you want to delete expense {expense_id}? (y/n): ")
    if answer.strip().lower() != "y":
        print("Nothing was deleted.")
        return

    if tracker.delete_expense(expenses, expense_id):
        if save(expenses):
            print("Expense deleted.")
    else:
        print(f"No expense found with ID {expense_id}.")


def handle_summary(expenses):
    print("\n-- Financial summary by category --")
    if not expenses:
        print("No expenses registered yet.")
        return

    totals = tracker.summarize_by_category(expenses)
    grand_total = tracker.get_total(expenses)

    # Biggest spending first.
    ranking = sorted(totals.items(), key=lambda item: item[1], reverse=True)
    for category, total in ranking:
        percentage = total / grand_total * 100
        print(f"{category:<20}{total:>10.2f}  ({percentage:5.1f}%)")
    print("-" * 40)
    print(f"{'TOTAL':<20}{grand_total:>10.2f}")


def main():
    try:
        expenses = storage.load_expenses(DATA_FILE)
    except (OSError, ValueError) as error:
        print(f"Error: could not read {DATA_FILE.name} ({error}).")
        return

    # Each menu option points to the function that handles it.
    actions = {
        "1": handle_add,
        "2": handle_list,
        "3": handle_total,
        "4": handle_filter_category,
        "5": handle_filter_month,
        "6": handle_delete,
        "7": handle_summary,
    }

    try:
        while True:
            print(MENU)
            choice = input("Choose an option: ").strip()

            if choice == "0":
                print("Goodbye!")
                break

            action = actions.get(choice)
            if action is None:
                print("Invalid option. Please choose a number from the menu.")
                continue
            action(expenses)
    except (KeyboardInterrupt, EOFError):
        # Ctrl+C / Ctrl+D: data is already saved after every change.
        print("\nGoodbye!")


if __name__ == "__main__":
    main()
