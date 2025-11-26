# Documentation

This directory contains the documentation source files for the IMAS MASTU mappings.

## Dynamic Documentation Generation

The mapping documentation (index.md, overview.md, mappings.md) is **generated dynamically** from the JSON mapping files when mkdocs builds the site. These files are not committed to git.

### Local Development

To serve the documentation locally:

```bash
pip install -e ".[docs]"
mkdocs serve
```

The mkdocs hook (`docs/hooks/gen_mapping_docs.py`) will automatically generate the documentation pages from your mapping JSON files.

### Static Files

The following files are maintained manually and should be committed:
- `docs/stylesheets/extra.css` - Custom styling
- `docs/mappings/pf_active/connections.md` - PF Active circuit connection diagrams
- `docs/hooks/gen_mapping_docs.py` - Documentation generation hook
- Any other manually created documentation files

### GitHub Pages Deployment

Documentation is automatically deployed to GitHub Pages when changes are pushed to the `main` branch via the `.github/workflows/docs.yml` workflow.

## Structure

- **index.md** (generated) - Homepage with list of all IDS mappings
- **mappings/{ids_name}/overview.md** (generated) - Overview with statistics and global variables
- **mappings/{ids_name}/mappings.md** (generated) - Detailed mapping tables
- **mappings/{ids_name}/connections.md** (manual) - Additional manually maintained pages
