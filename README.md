# ISBN Lookup CLI

Look up a book's title, author, and edition by ISBN — built for reselling
and author records. Local first: online lookup (Open Library, Google Books)
with an offline CSV database fallback, plus CSV export. No accounts, API
keys, or personal data required.

Built and maintained by Asdale Dynamics, LLC (Indiana, formed October 2026).
Part of the LLC's small-business and author tools line for KDP/book
publishing, reselling (eBay/Amazon), and author records. MIT licensed.

## Features

- Look up title, author, and edition by ISBN-10 or ISBN-13
- Hyphens and spaces in ISBNs are accepted
- Online sources: Open Library then Google Books (no API key, no account)
- Offline CSV database fallback — works entirely without network access
- CSV export of lookup results (`--export`)
- Offline database matches ISBN-10 and ISBN-13 forms of the same book
- Extend the offline database with your own titles for author/reseller records

## Requirements

Python 3. No third-party packages.

## Usage

```bash
# Online lookup (falls back to the offline database when offline)
python3 isbn_lookup_cli.py 978-0306-40615-7

# Offline only
python3 isbn_lookup_cli.py 9780306406157 --offline

# Export result to CSV
python3 isbn_lookup_cli.py 9780141439518 --export lookup.csv

# Use a different offline database
python3 isbn_lookup_cli.py 9780306406157 --db my_books.csv
```

Add your own books to the offline database (CSV columns: `isbn,title,author,edition`) so your catalog is available without network access.

## Tests

```bash
python3 -m unittest discover -s tests
```

## License

MIT License. Copyright (c) 2026 Asdale Dynamics, LLC. See LICENSE.

## About

Asdale Dynamics, LLC is a beginner-friendly AI education, books, and tools
studio founded by Dylan Asdale (registered nurse turned AI author). This tool
is part of the LLC's small-business and author tools for book publishing and
reselling. Learn more at dylanasdale.github.io.
