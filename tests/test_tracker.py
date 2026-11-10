import unittest

from src import tracker


def make_expense(expense_id, description, amount, category, date):
    return {
        "id": expense_id,
        "description": description,
        "amount": amount,
        "category": category,
        "date": date,
    }


class TrackerTests(unittest.TestCase):
    def setUp(self):
        self.expenses = [
            make_expense(1, "Lunch", 25.50, "Food", "2026-10-05"),
            make_expense(2, "Bus ticket", 4.80, "Transport", "2026-10-06"),
            make_expense(3, "Cinema", 32.00, "Leisure", "2026-11-02"),
            make_expense(4, "Groceries", 120.20, "Food", "2026-11-03"),
        ]

    def test_add_expense_gets_next_id(self):
        new = tracker.add_expense(self.expenses, "Coffee", 6.5, "Food", "2026-11-04")
        self.assertEqual(new["id"], 5)
        self.assertEqual(len(self.expenses), 5)
        self.assertIn(new, self.expenses)

    def test_first_expense_gets_id_one(self):
        expenses = []
        new = tracker.add_expense(expenses, "Coffee", 6.5, "Food", "2026-11-04")
        self.assertEqual(new["id"], 1)

    def test_id_is_not_reused_after_deleting_a_middle_expense(self):
        tracker.delete_expense(self.expenses, 2)
        new = tracker.add_expense(self.expenses, "Coffee", 6.5, "Food", "2026-11-04")
        self.assertEqual(new["id"], 5)

    def test_total(self):
        self.assertAlmostEqual(tracker.get_total(self.expenses), 182.5)

    def test_total_of_empty_list_is_zero(self):
        self.assertEqual(tracker.get_total([]), 0)

    def test_filter_by_category_ignores_case(self):
        result = tracker.filter_by_category(self.expenses, "food")
        self.assertEqual([e["id"] for e in result], [1, 4])

    def test_filter_by_unknown_category_returns_empty_list(self):
        self.assertEqual(tracker.filter_by_category(self.expenses, "Health"), [])

    def test_filter_by_month(self):
        result = tracker.filter_by_month(self.expenses, "2026-11")
        self.assertEqual([e["id"] for e in result], [3, 4])
        self.assertEqual(tracker.filter_by_month(self.expenses, "2026-12"), [])

    def test_delete_existing_expense(self):
        self.assertTrue(tracker.delete_expense(self.expenses, 2))
        self.assertEqual([e["id"] for e in self.expenses], [1, 3, 4])

    def test_delete_missing_expense_changes_nothing(self):
        self.assertFalse(tracker.delete_expense(self.expenses, 99))
        self.assertEqual(len(self.expenses), 4)

    def test_summarize_by_category(self):
        summary = tracker.summarize_by_category(self.expenses)
        self.assertEqual(summary, {"Food": 145.7, "Transport": 4.8, "Leisure": 32.0})

    def test_summarize_empty_list(self):
        self.assertEqual(tracker.summarize_by_category([]), {})

    def test_sort_expenses_by_date_then_id(self):
        messy = [
            make_expense(3, "C", 1.0, "X", "2026-11-02"),
            make_expense(2, "B", 1.0, "X", "2026-10-01"),
            make_expense(1, "A", 1.0, "X", "2026-11-02"),
        ]
        result = tracker.sort_expenses(messy)
        self.assertEqual([e["id"] for e in result], [2, 1, 3])


if __name__ == "__main__":
    unittest.main()
