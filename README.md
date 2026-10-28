# ISBN Lookup CLI

A small, local-first Python CLI for looking up a book's title, author, and
edition by ISBN — built for reselling on eBay/Amazon and for KDP/author
records. It checks online (Open Library, Google Books) first, then falls back
to a local CSV database you can edit yourself, and exports results to CSV.
No accounts, API keys, secrets, or personal data required — just Python.

Built and maintained by Asdale Dynamics, LLC (Indiana, formed October 2026).
A tool in the LLC's small-business and author-tools line for book publishing,
reselling, and author records. MIT licensed.

## Who is this for

Dylan Asdale — founder of Asdale Dynamics, LLC, registered nurse turned AI
author, writer of *The Massive AI Manual* (see dylanasdale.github.io) — makes
AI "like a friend would": plain English, step by step, never condescending.
This CLI is one of his beginner-friendly, local-first tools: easy to read,
easy to run, no moving parts, no cloud account, no surprises.

## Features

- Look up **title, author, and edition** by ISBN-10 or ISBN-13
- Accepts ISBNs with or without hyphens and spaces
- **Local first**: online sources (Open Library, then Google Books) with an
  **offline CSV database fallback** — looks work with no internet at all
- **CSV export** of any lookup result (`--export`)
- Offline database matches ISBN-10 and ISBN-13 forms of the same book
- Hand-editable offline catalog for your own reselling/author records
- Beginner-friendly output; no jargon, no setup

## Install

Requires Python 3. No packages to install (standard library only).

## Usage

```bash
# Online lookup (falls back to your offline database automatically if a
# book isn't online or you have no network)
python3 isbn_lookup_cli.py 978-0306-40615-7

# Offline only (use your CSV database; never touches the network)
python3 isbn_lookup_cli.py 9780306406157 --offline

# Export the result straight to CSV for a spreadsheet/bookkeeping sheet
python3 isbn_lookup_cli.py 9780141439518 --export results.csv

# Bring your own offline catalog
python3 isbn_lookup_cli.py 9780306406157 --db my_books.csv --offline
```

### Example output

```
ISBN:    9780306406157
Title:   The Structure of Scientific Revolutions
Author:  Thomas S. Kuhn
Edition:
Source:  offline
```

### Offline database format

A simple CSV with these columns (extra columns are ignored):

```
isbn,title,author,edition
9780306406157,The Structure of Scientific Revolutions,Thomas S. Kuhn,
9780061120084,To Kill a Mockingbird,Harper Lee,
```

Store ISBN-10 or ISBN-13; lookups match either form for the same book.

## For resellers

- Run a batch of ISBNs through the CLI and `--export` each row into one
  CSV spreadsheet for listing prep (title, author, edition, source).
- When offline (thrift stores, garage sales, no Wi-Fi), `--offline` still
  finds books in your own catalog.

## For authors / self-publishers

- Maintain your back-catalog and comparable-title research in `offline_books.csv`
  and look up comparable titles by ISBN without leaving the terminal.
- Add your own KDP titles to the offline DB so edition and author records
  travel with you — local-first, no account needed.

## Tests

```bash
python3 -m unittest discover -s tests
```

## License

MIT License. Copyright (c) 2026 Asdale Dynamics, LLC. See `LICENSE`.

## About Asdale Dynamics, LLC

Asdale Dynamics, LLC (Indiana, formed October 2026) makes beginner-friendly AI
education, books, and tools — open-source apps, local-LLM utilities, MCP/agent
skills, small-business and author tools, life-admin helpers, and healthcare
education aids. This ISBN lookup CLI is one of those tools. Learn more at
[dylanasdale.github.io](https://dylanasdale.github.io).
