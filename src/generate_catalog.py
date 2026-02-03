#!/usr/bin/env python3
import argparse
import json
import sys


def render_latex(catalog, title="LEGO Catalog"):
    header = r"""\documentclass{article}
\usepackage[utf8]{inputenc}
\usepackage{longtable}
\title{%s}
\begin{document}
\maketitle
\begin{longtable}{p{0.25\textwidth} p{0.7\textwidth}}
""" % title
    rows = []
    for item in catalog:
        name = item.get("name", "")
        desc = item.get("description", "")
        # escape basic LaTeX characters
        desc = desc.replace("&", "\\&").replace("%", "\\%")
        rows.append(f"{name} & {desc} \\\\ \hline")
    footer = r"""\end{longtable}
\end{document}
"""
    return header + "\n".join(rows) + "\n" + footer


def main():
    parser = argparse.ArgumentParser(description="Generate a LaTeX catalog from JSON data")
    parser.add_argument("-i", "--input", default="data/sample_catalog.json", help="Input JSON file")
    parser.add_argument("-o", "--output", default="catalog.tex", help="Output .tex file")
    parser.add_argument("-t", "--title", default="LEGO Catalog", help="Document title")
    args = parser.parse_args()

    try:
        with open(args.input, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        print(f"Failed to read input: {e}", file=sys.stderr)
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
