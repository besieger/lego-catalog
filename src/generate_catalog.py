#!/usr/bin/env python3
import argparse
import csv
import json
import sys


def render_latex(catalog, title="LEGO Catalog"):
    """Generate LaTeX document from catalog data."""
    header = r"""\documentclass{article}
\usepackage[utf8]{inputenc}
\usepackage[margin=0.5in]{geometry}
\usepackage{longtable}
\usepackage{booktabs}
\usepackage{xcolor}
\usepackage{colortbl}

\title{%s}
\author{Generated automatically}
\date{\today}

\begin{document}
\maketitle

\section*{Summary}
Total Sets: %d \\
Ready to go: %d \\
Partially complete: %d \\
In the aether: %d

\section*{Inventory}

\begin{longtable}{|p{1cm}|p{3cm}|p{1.5cm}|p{1cm}|p{1.2cm}|p{2cm}|}
\hline
\textbf{Set \#} & \textbf{Name} & \textbf{Theme} & \textbf{Pieces} & \textbf{Age} & \textbf{State} \\
\hline
\endhead
\hline
\endfoot
""" % (title, len(catalog), 
       sum(1 for x in catalog if x.get("State") == "Ready to go"),
       sum(1 for x in catalog if x.get("State") == "Partially complete"),
       sum(1 for x in catalog if x.get("State") == "In the aether"))
    
    rows = []
    for item in catalog:
        set_num = item.get("Set Number", "").strip() or "---"
        name = item.get("Name", "").strip() or "Unknown"
        theme = item.get("IP", "").strip() or item.get("Theme", "---")
        pieces = item.get("Pieces", "")
        age = item.get("Age min", "")
        state = item.get("State", "").strip() or "Unknown"
        
        # Escape LaTeX special characters
        name = name.replace("&", r"\&").replace("%", r"\%").replace("#", r"\#")
        theme = theme.replace("&", r"\&").replace("%", r"\%")
        state = state.replace("&", r"\&")
        
        # Color code state
        state_color = {
            "Ready to go": r"\cellcolor[gray]{0.9}",
            "Partially complete": r"\cellcolor[gray]{0.7}",
            "In the aether": r"\cellcolor[gray]{0.5}\textcolor{white}"
        }.get(state, "")
        
        state_text = f"{state_color}{state}" if state_color else state
        
        rows.append(f"{set_num} & {name} & {theme} & {pieces} & {age} & {state_text} \\\\")
    
    footer = r"""
\end{longtable}

\end{document}
"""
    return header + "\n".join(rows) + "\n" + footer


def main():
    parser = argparse.ArgumentParser(description="Generate a LaTeX catalog from CSV or JSON data")
    parser.add_argument("-i", "--input", default="lego-sets.csv", 
                        help="Input CSV or JSON file")
    parser.add_argument("-o", "--output", default="catalog.tex", 
                        help="Output .tex file")
    parser.add_argument("-t", "--title", default="LEGO Catalog", 
                        help="Document title")
    parser.add_argument("--convert-csv", action="store_true",
                        help="Convert CSV to JSON first (implies --input is CSV)")
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
