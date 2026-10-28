"""Offline book database backed by a CSV file."""

import csv
import os

from isbnlookup.parsing import (
    isbn10_to_isbn13,
    isbn13_to_isbn10,
    normalize_isbn,
)


class OfflineBookDatabase:
    """In-memory index of book records loaded from a CSV.

    Expected CSV columns: isbn, title, author, edition (extra columns ignored).
    ISBN-10 and ISBN-13 forms of the same book are cross-indexed.
    """

    def __init__(self, path=None):
        self.path = path
        self.records = []
        self._by_isbn = {}
        if path:
            self.load(path)

    def load(self, path):
        self.path = path
        self.records = []
        self._by_isbn = {}
        if not path or not os.path.exists(path):
            return
        with open(path, newline="", encoding="utf-8") as handle:
            reader = csv.DictReader(handle)
            for row in reader:
                isbn = normalize_isbn(row.get("isbn", ""))
                if not isbn:
                    continue
                record = {
                    "isbn": isbn,
                    "title": (row.get("title") or "").strip(),
                    "author": (row.get("author") or "").strip(),
                    "edition": (row.get("edition") or "").strip(),
                }
                self.records.append(record)
                self._by_isbn.setdefault(isbn, record)
                converted = self._convert(isbn)
                if converted:
                    self._by_isbn.setdefault(converted, record)

    @staticmethod
    def _convert(isbn):
        if len(isbn) == 13:
            return isbn13_to_isbn10(isbn)
        if len(isbn) == 10:
            return isbn10_to_isbn13(isbn)
        return None

    def find(self, isbn):
        """Return the record for ``isbn`` (exact or ISBN-10/13 equivalent)."""
        isbn = normalize_isbn(isbn)
        return self._by_isbn.get(isbn) if isbn else None

    def all(self):
        """Return a copy of all records."""
        return list(self.records)
