"""
MkDocs hook to generate mapping documentation dynamically on build/serve.

This hook generates documentation pages from mapping JSON files whenever
mkdocs builds or serves the site, ensuring docs are always up-to-date.
"""

import json
import sys
from pathlib import Path

# Add utils to path to import template resolver
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "utils" / "gen_docs"))
from generate_docs import (
    generate_overview,
    generate_mappings_page,
    generate_globals_section
)


def on_pre_build(config):
    """Generate documentation before mkdocs builds the site."""
    print("Generating mapping documentation from JSON files...")

    base_dir = Path(config['docs_dir']).parent
    mappings_dir = base_dir / "mappings"
    docs_dir = Path(config['docs_dir']) / "mappings"

    ids_list = ["magnetics", "pf_active", "pf_passive", "wall", "tf", "equilibrium", "summary"]

    for ids_name in ids_list:
        # Load mapping files
        mapping_file = mappings_dir / ids_name / "mappings.json"
        globals_file = mappings_dir / ids_name / "globals.json"

        if not mapping_file.exists():
            print(f"  Warning: {mapping_file} not found, skipping {ids_name}")
            continue

        with open(mapping_file) as f:
            mappings = json.load(f)

        globals_data = {}
        if globals_file.exists():
            with open(globals_file) as f:
                globals_data = json.load(f)

        # Create output directory
        output_dir = docs_dir / ids_name
        output_dir.mkdir(parents=True, exist_ok=True)

        # Generate overview (skip if it's manually maintained like pf_active/connections.md)
        overview_file = output_dir / "overview.md"
        if not overview_file.exists() or ids_name not in ["pf_active"]:  # pf_active has manual connections.md
            overview_content = generate_overview(ids_name, mappings, globals_data)
            if globals_data:
                overview_content += "\n" + generate_globals_section(globals_data)

            with open(overview_file, "w") as f:
                f.write(overview_content)

        # Generate mappings page
        mappings_content = generate_mappings_page(ids_name, mappings, globals_data)
        with open(output_dir / "mappings.md", "w") as f:
            f.write(mappings_content)

        print(f"  ✓ Generated {ids_name} documentation")

    # Generate index
    print("  Generating index page...")
    index_lines = []
    index_lines.append("# IMAS Mappings for MAST-U\n")
    index_lines.append("This documentation describes the JSON mappings used to convert MAST-U experimental data into ITER IMAS (Integrated Modelling & Analysis Suite) format.\n")
    index_lines.append("## Available IDS Mappings\n")

    ids_descriptions = {
        "magnetics": "Magnetic diagnostics including flux loops, Mirnov coils, and Rogowski coils",
        "pf_active": "Poloidal field coil system configuration and measurements",
        "pf_passive": "Passive conductor structures and vessel currents",
        "wall": "First wall and limiter geometry",
        "tf": "Toroidal field coil system",
        "equilibrium": "Magnetic equilibrium reconstruction data",
        "summary": "High-level pulse summary and derived quantities"
    }

    for ids_name in ids_list:
        desc = ids_descriptions.get(ids_name, "")
        index_lines.append(f"- **[{ids_name}](mappings/{ids_name}/overview.md)**: {desc}")

    index_lines.append("\n## Documentation Structure\n")
    index_lines.append("Each IDS has two pages:\n")
    index_lines.append("- **Overview**: Description, statistics, and global variables/configuration")
    index_lines.append("- **Mappings**: Detailed table of all IDS path mappings\n")

    index_lines.append("## Mapping Types\n")
    index_lines.append("- **DATA_SOURCE**: Data fetched from UDA (MAST-U data access), GEOMETRY files, or custom functions")
    index_lines.append("- **EXPR**: Computed values using mathematical expressions")
    index_lines.append("- **DIMENSION**: Array dimensions determined dynamically")
    index_lines.append("- **VALUE**: Direct values (literals or template strings with global variables)\n")

    with open(Path(config['docs_dir']) / "index.md", "w") as f:
        f.write("\n".join(index_lines))

    print("  ✓ Generated index page")
    print("✓ Mapping documentation generation complete")
