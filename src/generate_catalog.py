#!/usr/bin/env python3
import argparse
import csv
import json
import sys


def render_latex(catalog, title="LEGO Catalog"):
    """Generate LaTeX document from catalog data."""
    # Filter: only "Ready to go" and sets with number or name
    filtered = [
        item for item in catalog
        if item.get("State", "").strip() == "Ready to go"
        and (item.get("Set Number", "").strip() or item.get("Name", "").strip())
    ]
    
    header = r"""\documentclass{article}
\usepackage[utf8]{inputenc}
\usepackage[margin=0.75in]{geometry}
\usepackage{xcolor}

\title{%s}
\author{LEGO Collection Catalog}
\date{\today}

\pagestyle{empty}

\begin{document}
\maketitle
\thispagestyle{empty}

\newpage
""" % title
    
    pages = []
    for item in filtered:
        set_num = item.get("Set Number", "").strip() or "---"
        name = item.get("Name", "").strip() or "Unknown"
        age = item.get("Age min", "").strip() or "---"
        pieces = item.get("Pieces", "").strip() or "---"
        ip = item.get("IP", "").strip() or "---"
        missing = item.get("Missing Pieces", "").strip() or "None"
        notes = item.get("Notes", "").strip() or "---"
        
        # Escape LaTeX special characters
        name = name.replace("&", r"\&").replace("%", r"\%").replace("#", r"\#")
        ip = ip.replace("&", r"\&")
        missing = missing.replace("&", r"\&")
        notes = notes.replace("&", r"\&")
        
        page = f"""
\\begin{{center}}
{{\\Huge \\textbf{{{name}}}}}

{{\\small Set \\#{set_num}}}
\\end{{center}}

\\vspace{{2em}}

{{\\large Age {age}+ \\quad {pieces} pieces}}

\\vspace{{2em}}

\\textbf{{Theme:}} {ip} \\\\[0.5em]
\\textbf{{Missing Pieces:}} {missing} \\\\[0.5em]
\\textbf{{Notes:}} {notes}

\\vfill

\\newpage
"""
        pages.append(page)
    
    footer = r"""\end{document}
"""
    return header + "".join(pages) + footer


def main():
    parser = argparse.ArgumentParser(description="Generate a LaTeX catalog from CSV or JSON data")
    parser.add_argument("-i", "--input", default="lego-sets.csv", 
                        help="Input CSV or JSON file")
    parser.add_argument("-o", "--output", default="catalog.tex", 
                        help="Output .tex file")
    parser.add_argument("-t", "--title", default="LEGO Catalog", 
                        help="Document title")
    args = parser.parse_args()

    # Load data
    if args.input.endswith(".csv"):
        # Parse CSV directly
        data = []
        try:
            with open(args.input, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if any(row.values()):  # Skip empty rows
                        data.append(row)
        except Exception as e:
            print(f"Failed to read CSV: {e}", file=sys.stderr)
            sys.exit(2)
    else:
        # Parse JSON
        try:
            with open(args.input, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception as e:
            print(f"Failed to read JSON: {e}", file=sys.stderr)
            sys.exit(2)

    tex = render_latex(data, args.title)

    try:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(tex)
    except Exception as e:
        print(f"Failed to write output: {e}", file=sys.stderr)
        sys.exit(3)

    print(f"Wrote {args.output}")


if __name__ == "__main__":
    main()
