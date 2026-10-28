# STATUS

## What was built

A local-first Python CLI for looking up a book's title, author, and edition
by ISBN, intended for reselling and author records (KDP/eBay/Amazon
cataloging).

- `isbn_lookup_cli.py` — command-line entry point (argparse)
- `isbnlookup/parsing.py` — ISBN normalization, ISBN-10/ISBN-13 validation
  (check digits), and ISBN-10 <-> ISBN-13 conversion (978 prefix only)
- `isbnlookup/database.py` — offline CSV book database with ISBN-10/13
  cross-indexing
- `isbnlookup/lookup.py` — lookup engine: Open Library then Google Books
  online, offline CSV database as fallback
- `isbnlookup/matching.py` — edition/year parsing and title/author match
  scoring (`best_match`)
- `isbnlookup/export.py` — CSV export of lookup results
- `offline_books.csv` — sample offline database (7 sample titles, no personal
  data)
- `tests/test_all.py` — 18 unit tests covering parsing, database, matching,
  lookup, and export (network mocked)
- `LICENSE` — MIT, Copyright (c) 2026 Asdale Dynamics, LLC
- `README.md` — usage docs; credits Asdale Dynamics, LLC
- `STATUS.md` — this file

No accounts, API keys, secrets, or personal data. No GitHub Actions
workflows. Standard library only.

## How to run

```bash
# Online lookup (offline database is the fallback)
python3 isbn_lookup_cli.py 978-0306-40615-7

# Offline only
python3 isbn_lookup_cli.py 9780306406157 --offline

# Export to CSV
python3 isbn_lookup_cli.py 9780141439518 --export lookup.csv

# Custom offline database
python3 isbn_lookup_cli.py 9780306406157 --db my_books.csv --offline

# Run tests
python3 -m unittest discover -s tests
```

## Verification results

- `python3 -m unittest discover -s tests`: 18 tests, OK (parsing,
  database, matching, lookup, export; network calls mocked)
- Offline CLI lookup by ISBN-13 and ISBN-10 forms: works, source "offline"
- Online CLI lookup via Open Library: works, source "openlibrary"
- CSV export (`--export`): writes `isbn,title,author,edition,source` header
  and row correctly
- Invalid ISBN handling: exits with error message on stderr, exit code 1
- Not-found handling: returns "not found" result, exit code 0
- Python 3.13.5, stdlib only, no `pip install` required

## Known gaps

- Online lookups depend on network access and third-party APIs (Open Library,
  Google Books) that may rate-limit or change responses; offline mode is the
  reliable fallback.
- Open Library author fetching makes one request per author (up to 3).
- Edition detection is heuristic (edition N in title, or year from
  publish_date); not authoritative.
- No deduplication or edit UI for the offline database; edit the CSV directly.
- No fuzzy ISBN search; exact ISBN-10/ISBN-13 (or converted equivalent)
  matching only.
