#!/usr/bin/env python3
"""
Generate mkdocs documentation from IMAS mapping JSON files.

This script reads the mapping and globals JSON files and generates
comprehensive markdown documentation for each IDS.
"""

import json
import re
from pathlib import Path
from typing import Any, Dict
import sys

# Import the template resolver
sys.path.insert(0, str(Path(__file__).parent))
from simple_template_resolver import resolve_config_recursively


def identify_map_type(value: Any) -> str:
    """Identify the type of mapping from the value."""
    if isinstance(value, dict):
        if "MAP_TYPE" in value:
            return value["MAP_TYPE"]
        return "Object"
    else:
        # Template strings and literal values are both just "VALUE"
        return "VALUE"


def substitute_path_indices(path: str, index: int = 0) -> str:
    """Replace [#] in paths with actual index."""
    return re.sub(r'\[#\]', f'[{index}]', path)


def generate_mapping_table(mappings: Dict[str, Any], globals_data: Dict[str, Any]) -> str:
    """Generate an HTML table for mappings with path as header row."""
    lines = []
    lines.append('<div class="mappings-table">')

    for path, config in mappings.items():
        if path.startswith("_"):
            continue  # Skip internal paths

        map_type = identify_map_type(config)
        has_index = '[#]' in path
        num_indices = path.count('[#]')

        # Start table for this mapping
        lines.append('<table class="mapping-entry">')
        lines.append('  <thead>')
        lines.append(f'    <tr><th colspan="2"><code>{path}</code></th></tr>')
        lines.append('  </thead>')
        lines.append('  <tbody>')
        lines.append(f'    <tr><td class="label">Type</td><td><span class="type-badge type-{map_type.lower()}">{map_type}</span></td></tr>')

        # Format configuration details
        if isinstance(config, dict):
            if "MAP_TYPE" in config:
                if "DATA_SOURCE" in config:
                    lines.append(f'    <tr><td class="label">Data Source</td><td><code>{config["DATA_SOURCE"]}</code></td></tr>')
                if "ARGS" in config:
                    args_formatted = "<br>".join([f"<code>{k}</code>: <code>{v}</code>" for k, v in config["ARGS"].items()])
                    lines.append(f'    <tr><td class="label">Arguments</td><td>{args_formatted}</td></tr>')
                if "EXPR" in config:
                    lines.append(f'    <tr><td class="label">Expression</td><td><code>{config["EXPR"]}</code></td></tr>')
                if "PARAMETERS" in config:
                    params_formatted = "<br>".join([f"<code>{k}</code>: <code>{v}</code>" for k, v in config["PARAMETERS"].items()])
                    lines.append(f'    <tr><td class="label">Parameters</td><td>{params_formatted}</td></tr>')
                if "SCALE" in config:
                    lines.append(f'    <tr><td class="label">Scale</td><td><code>{config["SCALE"]}</code></td></tr>')
                if "SLICE" in config:
                    lines.append(f'    <tr><td class="label">Slice</td><td><code>{config["SLICE"]}</code></td></tr>')
                if "DIM_PROBE" in config:
                    lines.append(f'    <tr><td class="label">Dimension Probe</td><td><code>{config["DIM_PROBE"]}</code></td></tr>')
            else:
                # Generic object
                config_str = json.dumps(config, indent=2)
                lines.append(f'    <tr><td class="label">Value</td><td><pre>{config_str}</pre></td></tr>')
        elif isinstance(config, str):
            lines.append(f'    <tr><td class="label">Value</td><td><code>{config}</code></td></tr>')
        else:
            lines.append(f'    <tr><td class="label">Value</td><td><code>{config}</code></td></tr>')

        # Add expandable example section if path has [#]
        if has_index:
            example_path = substitute_path_indices(path, 0)
            resolved_config = resolve_config_recursively(config, globals_data)

            # Generate label based on number of indices
            if num_indices == 1:
                example_label = "Example with [0]"
            elif num_indices == 2:
                example_label = "Example with [0][0]"
            else:
                example_label = f"Example with {'[0]' * num_indices}"

            lines.append('    <tr><td colspan="2" class="example-section">')
            lines.append('      <details>')
            lines.append(f'        <summary>{example_label}</summary>')
            lines.append('        <div class="example-content">')
            lines.append(f'          <div class="example-path"><strong>Path:</strong> <code>{example_path}</code></div>')

            # Show resolved config
            if isinstance(resolved_config, dict) and "MAP_TYPE" in resolved_config:
                if "DATA_SOURCE" in resolved_config:
                    lines.append(f'          <div><strong>Data Source:</strong> <code>{resolved_config["DATA_SOURCE"]}</code></div>')
                if "ARGS" in resolved_config:
                    lines.append('          <div><strong>Arguments:</strong><br>')
                    for k, v in resolved_config["ARGS"].items():
                        lines.append(f'            <code>{k}</code>: <code>{v}</code><br>')
                    lines.append('          </div>')
                if "EXPR" in resolved_config:
                    lines.append(f'          <div><strong>Expression:</strong> <code>{resolved_config["EXPR"]}</code></div>')
                if "PARAMETERS" in resolved_config:
                    lines.append('          <div><strong>Parameters:</strong><br>')
                    for k, v in resolved_config["PARAMETERS"].items():
                        lines.append(f'            <code>{k}</code>: <code>{v}</code><br>')
                    lines.append('          </div>')
                if "SCALE" in resolved_config:
                    lines.append(f'          <div><strong>Scale:</strong> <code>{resolved_config["SCALE"]}</code></div>')
                if "SLICE" in resolved_config:
                    lines.append(f'          <div><strong>Slice:</strong> <code>{resolved_config["SLICE"]}</code></div>')
            elif isinstance(resolved_config, str):
                lines.append(f'          <div><strong>Value:</strong> <code>{resolved_config}</code></div>')
            else:
                lines.append(f'          <div><strong>Value:</strong> <code>{resolved_config}</code></div>')

            lines.append('        </div>')
            lines.append('      </details>')
            lines.append('    </td></tr>')

        lines.append('  </tbody>')
        lines.append('</table>')
        lines.append('')

    lines.append('</div>')
    return "\n".join(lines)


def generate_globals_section(globals_data: Dict[str, Any]) -> str:
    """Generate markdown for globals configuration."""
    lines = []
    lines.append("## Global Variables\n")

    if "DESCRIPTION" in globals_data:
        lines.append(f"_{globals_data['DESCRIPTION']}_\n")

    # Group globals by type
    simple_vars = {}
    complex_vars = {}
    arrays = {}

    for key, value in globals_data.items():
        if key == "DESCRIPTION":
            continue
        elif isinstance(value, list):
            arrays[key] = value
        elif isinstance(value, dict):
            complex_vars[key] = value
        else:
            simple_vars[key] = value

    # Simple variables
    if simple_vars:
        lines.append("### Configuration Variables\n")
        lines.append("| Variable | Value |")
        lines.append("|----------|-------|")
        for key, value in simple_vars.items():
            lines.append(f"| `{key}` | `{value}` |")
        lines.append("")

    # Complex variables (mappings, etc.)
    if complex_vars:
        lines.append("### Lookup Tables\n")
        for key, value in complex_vars.items():
            lines.append(f"#### `{key}`\n")
            lines.append("```json")
            lines.append(json.dumps(value, indent=2))
            lines.append("```\n")

    # Arrays (probe lists, etc.)
    if arrays:
        lines.append("### Data Arrays\n")
        for key, value in arrays.items():
            lines.append(f"#### `{key}` ({len(value)} items)\n")
            if len(value) <= 10:
                lines.append("```json")
                lines.append(json.dumps(value, indent=2))
                lines.append("```\n")
            else:
                lines.append("<details>")
                lines.append(f"<summary>Show all {len(value)} items</summary>\n")
                lines.append("```json")
                lines.append(json.dumps(value, indent=2))
                lines.append("```\n")
                lines.append("</details>\n")

    return "\n".join(lines)


def generate_overview(ids_name: str, mappings: Dict[str, Any], globals_data: Dict[str, Any]) -> str:
    """Generate overview content for an IDS."""
    lines = []
    lines.append(f"# {ids_name.upper()} IDS Overview\n")
    lines.append(f"This page documents the MAST-U to IMAS mapping for the **{ids_name}** IDS.\n")

    # Stats
    num_mappings = len([k for k in mappings.keys() if not k.startswith("_")])
    num_data_sources = len([v for v in mappings.values() if isinstance(v, dict) and v.get("MAP_TYPE") == "DATA_SOURCE"])
    num_expressions = len([v for v in mappings.values() if isinstance(v, dict) and v.get("MAP_TYPE") == "EXPR"])

    lines.append("## Mapping Statistics\n")
    lines.append(f"- **Total mapped paths**: {num_mappings}")
    lines.append(f"- **Data source mappings**: {num_data_sources}")
    lines.append(f"- **Computed expressions**: {num_expressions}")
    lines.append("")

    # Homogeneous time
    if "ids_properties/homogeneous_time" in mappings:
        ht_value = mappings["ids_properties/homogeneous_time"]
        ht_desc = "This IDS uses a single global time base." if ht_value == 1 else "This IDS uses independent time bases for each signal."
        lines.append(f"## Time Base\n")
        lines.append(f"{ht_desc} (`homogeneous_time = {ht_value}`)\n")

    return "\n".join(lines)


def generate_mappings_page(ids_name: str, mappings: Dict[str, Any], globals_data: Dict[str, Any]) -> str:
    """Generate the mappings detail page."""
    lines = []
    lines.append(f"# {ids_name.upper()} Mappings\n")
    lines.append("This page shows the detailed mapping configuration from MAST-U data to IMAS IDS paths.\n")

    # Add legend with type badges
    lines.append("## Mapping Types\n")
    lines.append('<div style="margin-bottom: 20px;">')
    lines.append('  <div style="margin: 8px 0;"><span class="type-badge type-data_source">DATA_SOURCE</span> Data fetched from external source (UDA, GEOMETRY, CUSTOM)</div>')
    lines.append('  <div style="margin: 8px 0;"><span class="type-badge type-expr">EXPR</span> Computed value using mathematical expression</div>')
    lines.append('  <div style="margin: 8px 0;"><span class="type-badge type-dimension">DIMENSION</span> Array dimension determined dynamically</div>')
    lines.append('  <div style="margin: 8px 0;"><span class="type-badge type-value">VALUE</span> Direct value (literal or template string)</div>')
    lines.append('</div>\n')

    lines.append("## All Mappings\n")
    lines.append("For paths containing array indices `[#]`, expandable examples show resolved values with all indices set to `[0]`. Click the example sections to view the fully resolved configuration.\n")
    lines.append(generate_mapping_table(mappings, globals_data))
    lines.append("")

    return "\n".join(lines)


def main():
    """Main entry point."""
    base_dir = Path(__file__).parent.parent.parent
    mappings_dir = base_dir / "mappings"
    docs_dir = base_dir / "docs" / "mappings"

    ids_list = ["magnetics", "pf_active", "pf_passive", "wall", "tf", "equilibrium", "summary"]

    for ids_name in ids_list:
        print(f"Generating documentation for {ids_name}...")

        # Load mapping files
        mapping_file = mappings_dir / ids_name / "mappings.json"
        globals_file = mappings_dir / ids_name / "globals.json"

        if not mapping_file.exists():
            print(f"  Warning: {mapping_file} not found, skipping")
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

        # Generate overview
        overview_content = generate_overview(ids_name, mappings, globals_data)
        if globals_data:
            overview_content += "\n" + generate_globals_section(globals_data)

        with open(output_dir / "overview.md", "w") as f:
            f.write(overview_content)

        # Generate mappings page
        mappings_content = generate_mappings_page(ids_name, mappings, globals_data)
        with open(output_dir / "mappings.md", "w") as f:
            f.write(mappings_content)

        print(f"  ✓ Generated {ids_name} documentation")

    # Generate index
    print("Generating index page...")
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

    with open(docs_dir.parent / "index.md", "w") as f:
        f.write("\n".join(index_lines))

    print("✓ Generated index page")
    print("\nDone! Documentation generated successfully.")
    print("Run 'mkdocs serve' to view the documentation.")


if __name__ == "__main__":
    main()
