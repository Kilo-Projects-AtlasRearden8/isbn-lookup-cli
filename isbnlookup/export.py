"""CSV export for lookup results."""

import csv

FIELDNAMES = ["isbn", "title", "author", "edition", "source"]


def write_csv(records, path):
    """Write lookup result records to a CSV file at ``path``."""
    with open(path, "w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDNAMES)
        writer.writeheader()
        for record in records:
            writer.writerow({field: record.get(field, "") for field in FIELDNAMES})
