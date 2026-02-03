# LEGO Catalog

[![Build catalog PDF](https://github.com/besieger/lego-catalog/actions/workflows/build-pdf.yml/badge.svg)](https://github.com/besieger/lego-catalog/actions/workflows/build-pdf.yml)

A catalog management system for LEGO collections.

## Project Structure

- Scripts for creating and managing the catalog
- Data storage for catalog entries

## Getting Started

To get started with this project, clone the repository and follow the setup instructions.

## Usage

Generate a LaTeX file from the sample JSON data:

```powershell
python src/generate_catalog.py -i data/sample_catalog.json -o catalog.tex
```

This writes `catalog.tex` in the repository root. Compile it with `pdflatex` if you want a PDF.

## License

MIT
