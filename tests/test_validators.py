import unittest

from src import validators


class ValidateAmountTests(unittest.TestCase):
    def test_accepts_dot_and_comma(self):
        self.assertEqual(validators.validate_amount("25.90"), 25.9)
        self.assertEqual(validators.validate_amount("25,90"), 25.9)

    def test_accepts_whole_numbers_and_spaces(self):
        self.assertEqual(validators.validate_amount("  10 "), 10.0)

    def test_rejects_zero_and_negative(self):
        for text in ["0", "-5", "0.001"]:
            with self.subTest(text=text):
                with self.assertRaises(ValueError):
                    validators.validate_amount(text)

    def test_rejects_non_numbers(self):
        for text in ["", "abc", "12abc", "nan", "inf"]:
            with self.subTest(text=text):
                with self.assertRaises(ValueError):
                    validators.validate_amount(text)

    def test_rejects_huge_amounts(self):
        with self.assertRaises(ValueError):
            validators.validate_amount("999999999999")


class ValidateDateTests(unittest.TestCase):
    def test_accepts_valid_date(self):
        self.assertEqual(validators.validate_date("2026-11-10"), "2026-11-10")

    def test_normalizes_short_format(self):
        self.assertEqual(validators.validate_date("2026-1-5"), "2026-01-05")

    def test_rejects_invalid_dates(self):
        for text in ["", "10/11/2026", "2026-02-30", "2026-13-01", "hello"]:
            with self.subTest(text=text):
                with self.assertRaises(ValueError):
                    validators.validate_date(text)


class ValidateMonthTests(unittest.TestCase):
    def test_accepts_valid_month(self):
        self.assertEqual(validators.validate_month("2026-11"), "2026-11")
        self.assertEqual(validators.validate_month("2026-1"), "2026-01")

    def test_rejects_invalid_month(self):
        for text in ["", "2026-13", "11/2026", "november"]:
            with self.subTest(text=text):
                with self.assertRaises(ValueError):
                    validators.validate_month(text)


class ValidateTextTests(unittest.TestCase):
    def test_description_is_trimmed(self):
        self.assertEqual(validators.validate_description("  Lunch  "), "Lunch")

    def test_description_cannot_be_empty_or_too_long(self):
        with self.assertRaises(ValueError):
            validators.validate_description("   ")
        with self.assertRaises(ValueError):
            validators.validate_description("a" * 101)

    def test_category_is_standardized(self):
        self.assertEqual(validators.validate_category("  fOOD "), "Food")

    def test_category_cannot_be_empty_or_too_long(self):
        with self.assertRaises(ValueError):
            validators.validate_category("")
        with self.assertRaises(ValueError):
            validators.validate_category("a" * 31)


class ValidateExpenseIdTests(unittest.TestCase):
    def test_accepts_positive_integer(self):
        self.assertEqual(validators.validate_expense_id(" 7 "), 7)

    def test_rejects_invalid_ids(self):
        for text in ["", "0", "-1", "1.5", "abc"]:
            with self.subTest(text=text):
                with self.assertRaises(ValueError):
                    validators.validate_expense_id(text)


if __name__ == "__main__":
    unittest.main()
