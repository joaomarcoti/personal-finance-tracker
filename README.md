# Personal Finance Tracker

A simple command-line application to record and review your personal expenses.
It is written in pure Python (standard library only), saves everything in a CSV
file and keeps your data available every time you reopen the program.

I built this project to practice Python fundamentals: functions, lists,
dictionaries, loops, conditionals, file handling, input validation, error
handling and unit testing.

## Features

- **Add expenses** with description, amount, category and date
- **List** all registered expenses in a readable table
- **Show the total** amount spent
- **Filter expenses by category** (case-insensitive)
- **Query expenses by month** (e.g. `2026-11`)
- **Delete** an expense by its ID (with confirmation)
- **Financial summary** with the total and percentage spent in each category
- **Persistent storage** in a CSV file
- **Input validation** and friendly error messages

## Technologies

- Python 3.8 or newer
- Standard library only: `csv`, `datetime`, `pathlib`, `math`, `unittest`
- No external packages, frameworks or databases

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/joaomarcoti/personal-finance-tracker.git
cd personal-finance-tracker
```

### 2. Run the application

Run the command from the project root folder:

```bash
python -m src.main
```

On Linux/macOS you may need to use `python3` instead of `python`.

The first time you run it, the file `data/expenses.csv` is created
automatically when you add your first expense.

### 3. (Optional) Try it with sample data

```bash
# Linux / macOS
cp data/sample_expenses.csv data/expenses.csv

# Windows (Command Prompt)
copy data\sample_expenses.csv data\expenses.csv
```

### 4. Run the tests

```bash
python -m unittest
```

For more detail, add the `-v` flag.

## Usage Examples

### Main menu

```text
===== Personal Finance Tracker =====
1. Add expense
2. List all expenses
3. Show total spent
4. Filter expenses by category
5. Show expenses by month
6. Delete expense
7. Financial summary by category
0. Exit
```

### Adding an expense

Amounts accept both `.` and `,` as the decimal separator. Press Enter on the
date question to use today's date.

```text
-- Add expense --
Description: Coffee beans
Amount: 18,50
Category: drinks
Date (YYYY-MM-DD) [2026-11-10]: 2026-11-09
Expense added and saved.
```

### Invalid data is rejected

```text
Amount: abc
  Invalid input: The amount must be a number, like 25.90.
Amount: -3
  Invalid input: The amount must be greater than zero.
```

### Querying expenses by month (option 5)

```text
Month (YYYY-MM): 2026-10
ID   Date        Category        Description                           Amount
-----------------------------------------------------------------------------
5    2026-10-05  Housing         Monthly rent share                    650.00
6    2026-10-09  Food            Lunch with friends, downtown           47.50
7    2026-10-18  Leisure         Cinema tickets                         56.00
8    2026-10-22  Health          Pharmacy                               38.75
9    2026-10-25  Transport       Bus pass                              120.00
-----------------------------------------------------------------------------
5 expense(s) | Total: 912.25
```

### Financial summary (option 7)

```text
-- Financial summary by category --
Housing                1950.00  ( 68.7%)
Food                    435.20  ( 15.3%)
Transport               240.00  (  8.5%)
Education                89.90  (  3.2%)
Leisure                  85.90  (  3.0%)
Health                   38.75  (  1.4%)
----------------------------------------
TOTAL                  2839.75
```

## Data Format

Expenses are stored in `data/expenses.csv`:

```csv
id,description,amount,category,date
1,Monthly rent share,650.00,Housing,2026-09-05
2,Groceries,182.40,Food,2026-09-12
```

- `id`: unique whole number, generated automatically
- `amount`: positive number with two decimal places
- `date`: `YYYY-MM-DD`

If a row in the file is damaged, the program skips it and shows a warning
instead of crashing.

## Project Structure

```text
personal-finance-tracker/
├── src/
│   ├── __init__.py
│   ├── main.py          # Menu and user interaction
│   ├── tracker.py       # Core logic: add, filter, delete, totals, summary
│   ├── storage.py       # Reading and writing the CSV file
│   └── validators.py    # Validation of user input
├── tests/
│   ├── __init__.py
│   ├── test_tracker.py
│   ├── test_storage.py
│   └── test_validators.py
├── data/
│   └── sample_expenses.csv   # Example data to try the app
├── .gitignore
└── README.md
```

## Design Notes

- **Separation of concerns:** `tracker.py` has no `print` or `input`, so the
  business logic can be tested without simulating a user at the keyboard.
- **Validation in one place:** the same validators are used for keyboard input
  and for rows loaded from the CSV file.
- **Data is saved after every change**, so nothing is lost if the program is
  closed unexpectedly.
