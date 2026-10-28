import tempfile
import unittest

from isbnlookup.database import OfflineBookDatabase
from isbnlookup.export import write_csv
from isbnlookup.lookup import LookupEngine
from isbnlookup.matching import (
    best_match,
    match_score,
    parse_edition_from_title,
    year_from_date,
)
from isbnlookup.parsing import (
    isbn10_to_isbn13,
    isbn13_to_isbn10,
    normalize_isbn,
    validate_isbn,
)


class ParsingTests(unittest.TestCase):
    def test_normalize_strips_formatting(self):
        self.assertEqual(normalize_isbn("978-0306-40615-7"), "9780306406157")
        self.assertEqual(normalize_isbn(" 0-306-40615-2 "), "0306406152")
        self.assertEqual(normalize_isbn("030640615x"), "030640615X")
        self.assertIsNone(normalize_isbn(""))
        self.assertIsNone(normalize_isbn(None))

    def test_valid_isbn13(self):
        self.assertTrue(validate_isbn("9780306406157"))
        self.assertTrue(validate_isbn("978-0-306-40615-7"))
        self.assertFalse(validate_isbn("9780306406158"))  # bad check digit
        self.assertFalse(validate_isbn("1234567890123"))

    def test_valid_isbn10(self):
        self.assertTrue(validate_isbn("0306406152"))
        self.assertTrue(validate_isbn("0-306-40615-2"))
        self.assertTrue(validate_isbn("000000006X"))  # X check digit
        self.assertFalse(validate_isbn("0306406153"))  # bad check digit

    def test_conversions(self):
        self.assertEqual(isbn13_to_isbn10("9780306406157"), "0306406152")
        self.assertEqual(isbn10_to_isbn13("0306406152"), "9780306406157")
        self.assertEqual(
            isbn13_to_isbn10(isbn10_to_isbn13("0306406152")), "0306406152"
        )
        self.assertIsNone(isbn13_to_isbn10("9780306406158"))  # invalid
        self.assertIsNone(isbn10_to_isbn13("0306406153"))  # invalid


class DatabaseTests(unittest.TestCase):
    def _write_csv(self, rows):
        import csv

        handle = tempfile.NamedTemporaryFile(
            "w", suffix=".csv", delete=False, newline=""
        )
        writer = csv.DictWriter(handle, fieldnames=["isbn", "title", "author"])
        writer.writeheader()
        for row in rows:
            writer.writerow(row)
        handle.close()
        return handle.name

    def test_find_exact_isbn(self):
        path = self._write_csv(
            [
                {"isbn": "978-0306-40615-7", "title": "TSOSR", "author": "Kuhn"},
            ]
        )
        db = OfflineBookDatabase(path)
        record = db.find("9780306406157")
        self.assertIsNotNone(record)
        self.assertEqual(record["title"], "TSOSR")

    def test_find_isbn10_when_stored_as_isbn13(self):
        path = self._write_csv(
            [
                {"isbn": "9780306406157", "title": "TSOSR", "author": "Kuhn"},
            ]
        )
        db = OfflineBookDatabase(path)
        record = db.find("0306406152")
        self.assertIsNotNone(record)
        self.assertEqual(record["isbn"], "9780306406157")

    def test_find_isbn13_when_stored_as_isbn10(self):
        path = self._write_csv(
            [
                {"isbn": "0306406152", "title": "TSOSR", "author": "Kuhn"},
            ]
        )
        db = OfflineBookDatabase(path)
        record = db.find("9780306406157")
        self.assertIsNotNone(record)

    def test_missing_file_is_empty(self):
        db = OfflineBookDatabase("/nonexistent/path.csv")
        self.assertEqual(db.records, [])
        self.assertIsNone(db.find("9780306406157"))

    def test_not_found(self):
        db = OfflineBookDatabase()
        db.records = [{"isbn": "1", "title": "x", "author": "y", "edition": ""}]
        db._by_isbn = {"1": db.records[0]}
        self.assertIsNone(db.find("9780306406157"))


class MatchingTests(unittest.TestCase):
    def test_parse_edition_from_title(self):
        self.assertEqual(parse_edition_from_title("Python (5th edition)"), "5")
        self.assertEqual(parse_edition_from_title("3rd edition of X"), "3")
        self.assertEqual(parse_edition_from_title("edition 2"), "2")
        self.assertIsNone(parse_edition_from_title("Plain Title"))

    def test_year_from_date(self):
        self.assertEqual(year_from_date("2003-07-30"), "2003")
        self.assertEqual(year_from_date("published 1999"), "1999")
        self.assertIsNone(year_from_date("no date"))

    def test_match_score_ranks_title_above_author(self):
        record = {"title": "Learning Python", "author": "Mark Lutz"}
        self.assertGreater(
            match_score("Learning Python", record),
            match_score("Mark Lutz", record),
        )
        self.assertGreater(match_score("Learning Python", record), 0.5)

    def test_best_match_returns_top_record(self):
        records = [
            {"isbn": "1", "title": "Pride and Prejudice", "author": "Jane Austen"},
            {"isbn": "2", "title": "1984", "author": "George Orwell"},
        ]
        best = best_match("pride and prejudice", records)
        self.assertEqual(best["isbn"], "1")
        self.assertIsNone(best_match("anything", []))


class LookupTests(unittest.TestCase):
    def test_invalid_isbn(self):
        engine = LookupEngine(offline=True)
        result = engine.lookup("123")
        self.assertEqual(result["error"], "invalid ISBN")
        self.assertIsNone(result["source"])

    def test_offline_lookup_uses_database(self):
        db = OfflineBookDatabase()
        db.records = [
            {
                "isbn": "9780306406157",
                "title": "The Structure of Scientific Revolutions",
                "author": "Thomas S. Kuhn",
                "edition": "2nd",
            }
        ]
        db._by_isbn = {r["isbn"]: r for r in db.records}
        engine = LookupEngine(database=db, offline=True)
        result = engine.lookup("978-0306-40615-7")
        self.assertIsNone(result.get("error"))
        self.assertEqual(result["title"], "The Structure of Scientific Revolutions")
        self.assertEqual(result["author"], "Thomas S. Kuhn")
        self.assertEqual(result["source"], "offline")

    def test_offline_isbn10_13_cross_match(self):
        db = OfflineBookDatabase()
        db.records = [
            {
                "isbn": "0306406152",
                "title": "The Structure of Scientific Revolutions",
                "author": "Thomas S. Kuhn",
                "edition": "",
            }
        ]
        db._by_isbn = {
            "0306406152": db.records[0],
            "9780306406157": db.records[0],
        }
        engine = LookupEngine(database=db, offline=True)
        result = engine.lookup("9780306406157")
        self.assertIsNone(result.get("error"))
        self.assertEqual(result["title"], "The Structure of Scientific Revolutions")

    def test_not_found_offline(self):
        db = OfflineBookDatabase()
        engine = LookupEngine(database=db, offline=True)
        result = engine.lookup("9780306406157")
        self.assertEqual(result["error"], "not found")

    def test_export_csv(self):
        import os

        path = tempfile.mktemp(suffix=".csv")
        try:
            write_csv(
                [
                    {
                        "isbn": "9780306406157",
                        "title": "TSOSR",
                        "author": "Kuhn",
                        "edition": "2nd",
                        "source": "offline",
                    }
                ],
                path,
            )
            with open(path, encoding="utf-8") as handle:
                content = handle.read()
            self.assertIn("9780306406157", content)
            self.assertIn("TSOSR", content)
        finally:
            if os.path.exists(path):
                os.remove(path)


if __name__ == "__main__":
    unittest.main()
