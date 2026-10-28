#!/usr/bin/env python3
"""ISBN lookup CLI.

Look up a book's title, author, and edition by ISBN. Local first: online
sources (Open Library, Google Books) with an offline CSV database fallback.
No accounts or API keys required.
"""

import argparse
import os
import sys

from isbnlookup.database import OfflineBookDatabase
from isbnlookup.export import write_csv
from isbnlookup.lookup import LookupEngine


def build_parser():
    parser = argparse.ArgumentParser(
        prog="isbn_lookup_cli",
        description="Look up book title, author, and edition by ISBN.",
    )
    parser.add_argument("isbn", help="ISBN-10 or ISBN-13 (hyphens/spaces OK)")
    parser.add_argument(
        "--export",
        metavar="CSV",
        help="write the lookup result to a CSV file",
    )
    parser.add_argument(
        "--offline",
        action="store_true",
        help="skip online sources; use the offline database only",
    )
    parser.add_argument(
        "--db",
        default="offline_books.csv",
        help="offline CSV database path (default: offline_books.csv)",
    )
    return parser


def main(argv=None):
    args = build_parser().parse_args(argv)

    database = None
    if args.db and os.path.exists(args.db):
        database = OfflineBookDatabase(args.db)

    engine = LookupEngine(database=database, offline=args.offline)
    result = engine.lookup(args.isbn)

    if result.get("error"):
        print(
            f"error: {result['error']} (isbn: {result.get('isbn')})",
            file=sys.stderr,
        )
        return 1

    print(f"ISBN:    {result['isbn']}")
    print(f"Title:   {result['title']}")
    print(f"Author:  {result['author']}")
    print(f"Edition: {result['edition']}")
    print(f"Source:  {result['source']}")

    if args.export:
        write_csv([result], args.export)
        print(f"exported: {args.export}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
