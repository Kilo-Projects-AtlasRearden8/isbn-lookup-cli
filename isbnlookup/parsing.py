"""ISBN parsing, validation, and conversion.

Standard library only. Supports ISBN-10 and ISBN-13, with or without
hyphens and spaces.
"""

import re

_STRIP_RE = re.compile(r"[-\s]")
_ISBN10_RE = re.compile(r"^\d{9}[\dX]$")


def normalize_isbn(raw):
    """Return an uppercase, hyphen-free ISBN string, or ``None`` if empty."""
    if raw is None:
        return None
    isbn = _STRIP_RE.sub("", str(raw)).strip().upper()
    return isbn or None


def validate_isbn(isbn):
    """Return ``True`` when ``isbn`` is a valid ISBN-10 or ISBN-13."""
    isbn = normalize_isbn(isbn)
    if not isbn:
        return False
    if len(isbn) == 13:
        return _valid_isbn13(isbn)
    if len(isbn) == 10:
        return _valid_isbn10(isbn)
    return False


def _valid_isbn13(isbn):
    if not isbn.isdigit():
        return False
    total = sum((3 if i % 2 else 1) * int(d) for i, d in enumerate(isbn[:12]))
    return (10 - (total % 10)) % 10 == int(isbn[12])


def _valid_isbn10(isbn):
    if not _ISBN10_RE.match(isbn):
        return False
    total = sum((i + 1) * (10 if d == "X" else int(d)) for i, d in enumerate(isbn[:9]))
    check = total % 11
    expected = "X" if check == 10 else str(check)
    return expected == isbn[9]


def isbn13_to_isbn10(isbn):
    """Convert an ISBN-13 to ISBN-10 (only 978/979 prefix converts).

    Returns ``None`` when the conversion is not possible.
    """
    isbn = normalize_isbn(isbn)
    if not validate_isbn(isbn) or isbn[:3] != "978":
        return None
    core = isbn[3:12]
    total = sum((i + 1) * int(d) for i, d in enumerate(core))
    check = total % 11
    return core + ("X" if check == 10 else str(check))


def isbn10_to_isbn13(isbn):
    """Convert an ISBN-10 to ISBN-13. Returns ``None`` on invalid input."""
    isbn = normalize_isbn(isbn)
    if not validate_isbn(isbn):
        return None
    core = "978" + isbn[:9]
    total = sum((3 if i % 2 else 1) * int(d) for i, d in enumerate(core[:12]))
    return core + str((10 - (total % 10)) % 10)
