#!/usr/bin/env python3
"""Convert LEGO sets CSV to JSON format."""

import csv
import json
import sys
from pathlib import Path


def csv_to_json(csv_file, json_file):
    """Convert CSV to JSON, cleaning up empty rows and converting types."""
    rows = []
    with open(csv_file, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Skip empty rows
            if not any(row.values()):
                continue
            
            # Clean up whitespace and convert types
            cleaned = {}
            for k, v in row.items():
                if not v or v.strip() == "":
                    continue
                v = v.strip()
                
                # Convert numeric fields
                if k in ("Pieces", "Age min"):
                    try:
                        cleaned[k] = int(v)
                    except ValueError:
                        cleaned[k] = v
                else:
                    cleaned[k] = v
            
            if cleaned:  # Only add non-empty rows
                rows.append(cleaned)
    
    # Write JSON
    with open(json_file, "w", encoding="utf-8") as f:
        json.dump(rows, f, ensure_ascii=False, indent=2)
    
    print(f"Converted {len(rows)} rows to {json_file}")


if __name__ == "__main__":
    csv_file = sys.argv[1] if len(sys.argv) > 1 else "lego-sets.csv"
    json_file = sys.argv[2] if len(sys.argv) > 2 else "data/catalog.json"
    
    if not Path(csv_file).exists():
        print(f"Error: {csv_file} not found", file=sys.stderr)
        sys.exit(1)
    
    csv_to_json(csv_file, json_file)
