import unittest
from sync_service import normalize_phone, transform


class SyncTests(unittest.TestCase):
    def test_normalizes_russian_phone_forms(self):
        self.assertEqual(normalize_phone("8 (999) 123-45-67"), "+79991234567")
        self.assertEqual(normalize_phone("9991234567"), "+79991234567")
        self.assertIsNone(normalize_phone("12345"))

    def test_keeps_highest_amount_then_latest_date(self):
        result = transform([
            {"name": "old", "phone": "89991234567", "email": "a", "amount": 5000, "created_at": "2025-01-01T00:00:00Z"},
            {"name": "high", "phone": "+7 999 123 45 67", "email": "b", "amount": 7000, "created_at": "2024-01-01T00:00:00Z"},
            {"name": "same-later", "phone": "79991234567", "email": "c", "amount": 7000, "created_at": "2026-01-01T00:00:00Z"},
            {"name": "bad", "phone": "not-a-phone", "email": "", "amount": 1, "created_at": "2026-01-01T00:00:00Z"},
        ])
        self.assertEqual(result["clients"], [{"name": "same-later", "phone": "+79991234567", "email": "c", "amount": 7000}])
        self.assertEqual(result["stats"], {"received": 4, "unique": 1, "duplicates_merged": 2, "invalid_dropped": 1})


if __name__ == "__main__":
    unittest.main()
