import contextlib
import io
import tempfile
import unittest
from pathlib import Path

from src import storage


class StorageTests(unittest.TestCase):
    def setUp(self):
        folder = tempfile.TemporaryDirectory()
        self.addCleanup(folder.cleanup)
        self.path = Path(folder.name) / "expenses.csv"

    def test_load_missing_file_returns_empty_list(self):
        self.assertEqual(storage.load_expenses(self.path), [])

    def test_save_and_load_round_trip(self):
        expenses = [
            {"id": 1, "description": "Lunch", "amount": 25.5,
             "category": "Food", "date": "2026-10-05"},
            {"id": 2, "description": "Bus", "amount": 4.8,
             "category": "Transport", "date": "2026-10-06"},
        ]
        storage.save_expenses(self.path, expenses)
        self.assertEqual(storage.load_expenses(self.path), expenses)

    def test_save_creates_missing_folder(self):
        nested = self.path.parent / "new_folder" / "expenses.csv"
        storage.save_expenses(nested, [])
        self.assertTrue(nested.exists())

    def test_commas_and_quotes_are_preserved(self):
        expenses = [
            {"id": 1, "description": 'Pizza, "large" size', "amount": 40.0,
             "category": "Food", "date": "2026-10-05"},
        ]
        storage.save_expenses(self.path, expenses)
        self.assertEqual(storage.load_expenses(self.path), expenses)

    def test_invalid_rows_are_skipped_with_warning(self):
        self.path.write_text(
            "id,description,amount,category,date\n"
            "1,Lunch,25.50,Food,2026-10-05\n"
            "2,Broken amount,abc,Food,2026-10-06\n"
            "3,Bad date,10.00,Food,2026-13-45\n",
            encoding="utf-8",
        )
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            loaded = storage.load_expenses(self.path)

        self.assertEqual([e["id"] for e in loaded], [1])
        self.assertIn("line 3", output.getvalue())
        self.assertIn("line 4", output.getvalue())

    def test_incomplete_rows_are_skipped(self):
        self.path.write_text(
            "id,description,amount,category,date\n"
            "1,Only three columns,10.00\n",
            encoding="utf-8",
        )
        with contextlib.redirect_stdout(io.StringIO()):
            loaded = storage.load_expenses(self.path)
        self.assertEqual(loaded, [])


if __name__ == "__main__":
    unittest.main()
