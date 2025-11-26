# Documentation Generator

This directory contains tools for generating mkdocs documentation from IMAS mapping JSON files.

## generate_docs.py

The main documentation generator script that creates markdown/HTML documentation from mapping and globals JSON files.

### Usage

```bash
python utils/gen_docs/generate_docs.py
```

This will:
1. Read all mapping files from `mappings/*/mappings.json`
2. Read all globals files from `mappings/*/globals.json`
3. Generate overview and mappings pages for each IDS
4. Create an index page with links to all IDS documentation

### Output

Documentation is generated in `docs/`:
- `docs/index.md` - Main index page
- `docs/mappings/{ids_name}/overview.md` - IDS overview with stats and globals
- `docs/mappings/{ids_name}/mappings.md` - Detailed mapping tables (HTML)

**Note**: The generator will NOT overwrite manually created files like `connections.md`.

### Supported IDS

- magnetics
- pf_active
- pf_passive
- wall
- tf
- equilibrium
- summary

## Features

### HTML Tables
Mappings are displayed using HTML tables with the IDS path as the header row, making it easy to read long paths. Each mapping entry shows:
- Type badge (color-coded)
- Data source
- Arguments
- Expressions/parameters
- Scale factors
- Slices

### CSS Styling
Custom styles in `docs/stylesheets/extra.css` provide:
- Color-coded type badges
- Clean table formatting
- Responsive layout
- Proper code formatting

### Overview Pages
Auto-generated overview pages include:
- Mapping statistics
- Time base information
- Global variables with collapsible sections for large arrays
- Lookup tables

## gen_table_manual.py

Legacy HTML table generator (deprecated). Use `generate_docs.py` instead.

## Viewing Documentation

After generating the docs:

```bash
mkdocs serve
```

Then open http://127.0.0.1:8000 in your browser.
