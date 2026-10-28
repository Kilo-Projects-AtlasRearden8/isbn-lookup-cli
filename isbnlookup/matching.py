"""Matching helpers: edition parsing and record scoring."""

import difflib
import re

_EDITION_POS_RE = re.compile(r"(?i)\b(\d{1,2})(?:st|nd|rd|th)?\s*ed(?:ition)?\b")
_EDITION_AFTER_RE = re.compile(r"(?i)\bed(?:ition)?\s*(\d{1,2})\b")
_YEAR_RE = re.compile(r"\b(1\d{3}|2\d{3})\b")


def parse_edition_from_title(title):
    """Return an edition number string found in a title, or ``None``."""
    if not title:
        return None
    match = _EDITION_POS_RE.search(title) or _EDITION_AFTER_RE.search(title)
    return match.group(1) if match else None


def year_from_date(date_str):
    """Return the first four-digit year found in a date string, or ``None``."""
    match = _YEAR_RE.search(date_str or "")
    return match.group(1) if match else None


def match_score(query, record):
    """Score how well ``query`` matches a record's title/author (0.0-1.0)."""
    query = (query or "").lower()
    title = (record.get("title") or "").lower()
    author = (record.get("author") or "").lower()
    title_ratio = difflib.SequenceMatcher(None, query, title).ratio()
    author_ratio = difflib.SequenceMatcher(None, query, author).ratio()
    return 0.6 * title_ratio + 0.4 * author_ratio


def best_match(query, records):
    """Return the record with the highest match score, or ``None``."""
    if not records:
        return None
    return max(records, key=lambda record: match_score(query, record))
