"""Lookup engine: online sources first, offline database as fallback."""

import json
import urllib.error
import urllib.request

from isbnlookup.database import OfflineBookDatabase
from isbnlookup.matching import parse_edition_from_title, year_from_date
from isbnlookup.parsing import (
    isbn10_to_isbn13,
    isbn13_to_isbn10,
    normalize_isbn,
    validate_isbn,
)

_USER_AGENT = "isbn-lookup-cli/1.0"
_TIMEOUT = 15


class LookupError(Exception):
    """Raised when a lookup cannot be completed."""


def _fetch_json(url):
    """Fetch JSON from ``url``. Returns ``None`` on any transport/parse error."""
    try:
        request = urllib.request.Request(url, headers={"User-Agent": _USER_AGENT})
        with urllib.request.urlopen(request, timeout=_TIMEOUT) as response:
            body = response.read()
        return json.loads(body.decode("utf-8"))
    except (urllib.error.URLError, OSError, ValueError, json.JSONDecodeError):
        return None


def _openlibrary_lookup(isbn):
    data = _fetch_json(f"https://openlibrary.org/isbn/{isbn}.json")
    if not data:
        return None
    title = data.get("title") or ""
    authors = []
    for entry in data.get("authors") or []:
        if len(authors) >= 3:
            break
        key = entry.get("key") if isinstance(entry, dict) else None
        if not key:
            continue
        author_data = _fetch_json(f"https://openlibrary.org{key}.json")
        if author_data and author_data.get("name"):
            authors.append(author_data["name"])
    publish_date = data.get("publish_date") or ""
    edition = (
        parse_edition_from_title(title)
        or year_from_date(publish_date)
        or "Unknown"
    )
    return {
        "isbn": isbn,
        "title": title or "Unknown",
        "author": ", ".join(authors) or "Unknown",
        "edition": edition,
        "source": "openlibrary",
    }


def _google_books_lookup(isbn):
    data = _fetch_json(f"https://www.googleapis.com/books/v1/volumes?q=isbn:{isbn}")
    if not data:
        return None
    items = data.get("items") or []
    if not items:
        return None
    info = items[0].get("volumeInfo", {}) or {}
    title = info.get("title") or ""
    authors = info.get("authors") or []
    published = info.get("publishedDate") or ""
    edition = (
        parse_edition_from_title(title) or year_from_date(published) or "Unknown"
    )
    return {
        "isbn": isbn,
        "title": title or "Unknown",
        "author": ", ".join(authors) or "Unknown",
        "edition": edition,
        "source": "google-books",
    }


class LookupEngine:
    """Resolve an ISBN to title/author/edition.

    Online sources (Open Library, then Google Books) are tried first unless
    offline mode is set. The offline CSV database is the final fallback, so
    lookups work entirely without network access.
    """

    def __init__(self, database=None, offline=False):
        self.database = database or OfflineBookDatabase()
        self.offline = offline

    def lookup(self, isbn):
        normalized = normalize_isbn(isbn)
        if not normalized or not validate_isbn(normalized):
            return {
                "isbn": normalized or "",
                "title": "",
                "author": "",
                "edition": "",
                "source": None,
                "error": "invalid ISBN",
            }

        if not self.offline:
            for fetch in (_openlibrary_lookup, _google_books_lookup):
                try:
                    result = fetch(normalized)
                except Exception:
                    result = None
                if result:
                    return result

        record = self.database.find(normalized)
        if record:
            return {**record, "source": "offline"}

        return {
            "isbn": normalized,
            "title": "",
            "author": "",
            "edition": "",
            "source": None,
            "error": "not found",
        }
