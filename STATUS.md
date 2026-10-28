# STATUS

## What was built

A local-first Python CLI for looking up a book's title, author, and edition
by ISBN, for reselling (eBay/Amazon) and author/KDP records.

- `isbn_lookup_cli.py` — argparse CLI
  (`--offline`, `--db`, `--export`)
- `isbnlookup/parsing.py` — ISBN normalization, ISBN-10/ISBN-13 check-digit
  validation, ISBN-10 <-> ISBN-13 conversion (978 prefix only)
- `isbnlookup/database.py` — offline CSV book database with ISBN-10/13
  cross-indexing
- `isbnlookup/lookup.py` — lookup engine: Open Library then Google Books
  online, offline CSV database as fallback
- `isbnlookup/matching.py` — edition/year parsing and title/author match
  scoring (`match_score`, `best_match`)
- `isbnlookup/export.py` — CSV export (`isbn,title,author,edition,source`)
- `offline_books.csv` — sample offline database (7 sample titles; no personal
  data)
- `tests/test_all.py` — unit tests (21 tests; network mocked)
- `LICENSE` — MIT, copyright line exactly `Copyright (c) 2026 Asdale Dynamics, LLC`
- `README.md` — usage docs; credits Asdale Dynamics, LLC
- `STATUS.md` — this file

No accounts, API keys, secrets, personal data, or `.github/workflows`.
Standard library only. Built for Asdale Dynamics, LLC by Dylan Asdale.

## How to run

```bash
# Online lookup (offline database is the automatic fallback)
python3 isbn_lookup_cli.py 978-0306-40615-7

# Offline only
python3 isbn_lookup_cli.py 9780306406157 --offline

# Export to CSV
python3 isbn_lookup_cli.py 9780141439518 --export results.csv

# Custom offline database
python3 isbn_lookup_cli.py 9780306406157 --db my_books.csv --offline

# Run tests
python3 -m unittest discover -s tests
```

## Verification results

- `python3 -m unittest discover -s tests`: 21 tests, OK
  - parsing (ISBN-10/13 validation + conversion)
  - matching (edition/year parsing, title/author match scoring)
  - database (exact + ISBN-10/13 cross match, missing file, not found)
  - lookup (online Open Library, online Google Books, offline fallback when
    online fails, offline-only, invalid ISBN, not found)
  - export (CSV round-trip)
- Offline CLI lookup by ISBN-13 and ISBN-10: works, `Source: offline`
- Online CLI lookup via Open Library: works, `Source: openlibrary`
- `--export`: writes `isbn,title,author,edition,source` header + row
- Invalid ISBN: stderr error message, exit code 1
- Python 3.13.5, stdlib only; no `pip install` required

## Known gaps

- Online lookups depend on third-party APIs (Open Library, Google Books) that
  may rate-limit or change responses; offline mode is the reliable fallback.
- Open Library author fetching makes one request per author (up to 3).
- Edition detection is heuristic (edition number in title, or year from
  publish_date); not authoritative. A title that is a bare year (e.g. "1984")
  may surface its publication year as the edition.
- Offline catalog has no UI for adding/editing rows; edit the CSV directly.
- No fuzzy ISBN search; exact ISBN-10/ISBN-13 (or converted equivalent)
  matching only.
- No multi-ISBN batch mode in one invocation; loop over ISBNs from a file if
  needed.
