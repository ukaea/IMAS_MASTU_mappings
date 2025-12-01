#!/usr/bin/env python3
"""
Simple Inja-like template resolver for resolving templates in mapping configs.

This module provides functions to resolve template expressions and nested
bracket notation in IMAS mapping configurations.
"""

import re
from typing import Any, Dict


def resolve_expression(expr: str, globals_data: Dict[str, Any]) -> str:
    """Resolve a single expression, handling nested brackets."""
    expr = expr.strip()

    # Simple variable lookup
    if expr in globals_data:
        value = globals_data[expr]
        if isinstance(value, (str, int, float)):
            return str(value)

    # Handle ARRAY[N].FIELD syntax (e.g., FLUX_LOOPS[0].TYPE)
    array_dot_match = re.match(r'(\w+)\[(\d+)\]\.(\w+)', expr)
    if array_dot_match:
        array_name, idx, field = array_dot_match.groups()
        if array_name in globals_data:
            array = globals_data[array_name]
            if isinstance(array, list) and int(idx) < len(array):
                item = array[int(idx)]
                if isinstance(item, dict) and field in item:
                    return str(item[field])

    # Handle MAP[KEY].suffix where KEY might have brackets (e.g., FL_POSITION_MAP[FLUX_LOOPS[0].TYPE].r)
    map_suffix_complex_match = re.match(r'(\w+)\[(.+)\]\.(.+)$', expr)
    if map_suffix_complex_match:
        map_name, key_expr, suffix = map_suffix_complex_match.groups()
        if map_name in globals_data and isinstance(globals_data[map_name], dict):
            # Recursively resolve the key expression first
            resolved_key = resolve_expression(key_expr, globals_data)
            if resolved_key in globals_data[map_name]:
                return str(globals_data[map_name][resolved_key]) + '.' + suffix

    # Handle MAP[KEY] where KEY might have brackets (e.g., FL_POSITION_MAP[FLUX_LOOPS[0].TYPE])
    map_complex_match = re.match(r'(\w+)\[(.+)\]$', expr)
    if map_complex_match:
        map_name, key_expr = map_complex_match.groups()
        if map_name in globals_data and isinstance(globals_data[map_name], dict):
            # Recursively resolve the key expression first
            resolved_key = resolve_expression(key_expr, globals_data)
            if resolved_key in globals_data[map_name]:
                return str(globals_data[map_name][resolved_key])

    return expr  # Return unchanged


def resolve_templates_iteratively(text: str, globals_data: Dict[str, Any], max_iterations: int = 20) -> str:
    """
    Resolve templates by repeated substitution until nothing changes.
    Resolves from innermost to outermost by doing multiple passes.
    """
    if not isinstance(text, str):
        return text

    result = text

    for iteration in range(max_iterations):
        old_result = result

        # Step 1: Replace all [#N] with [0]
        result = re.sub(r'\[#\d+\]', '[0]', result)
        result = re.sub(r'\[indices\.\d+\]', '[0]', result)

        # Step 2: Replace #N with 0 in arithmetic expressions
        result = re.sub(r'#\d+', '0', result)

        # Step 3: Find and replace {{ }} templates
        # Process innermost templates first (templates without nested {{ }})
        def replace_template(match):
            expr = match.group(1).strip()

            # Try to evaluate as arithmetic expression if it contains operators
            if any(op in expr for op in ['+', '-', '*', '/', '%']):
                try:
                    # Safe evaluation of simple arithmetic
                    evaluated = eval(expr, {"__builtins__": {}}, {})
                    return str(evaluated)
                except:
                    pass

            # Otherwise resolve as variable/expression
            resolved = resolve_expression(expr, globals_data)
            return resolved

        result = re.sub(r'\{\{\s*([^{}]+?)\s*\}\}', replace_template, result)

        # Step 4: Also try to resolve bracket notation outside of templates
        # This handles cases where templates were resolved but left bracket notation
        # e.g., "FL_POSITION_MAP[FLUX].r" (no {{ }})
        if '[' in result and ']' in result and '{{' not in result:
            # Try resolving the entire string as an expression
            resolved = resolve_expression(result, globals_data)
            if resolved != result:
                result = resolved

        # If nothing changed, we're done
        if result == old_result:
            break

    return result


def resolve_config_recursively(config: Any, globals_data: Dict[str, Any]) -> Any:
    """Recursively resolve all templates in a config structure."""
    if isinstance(config, str):
        return resolve_templates_iteratively(config, globals_data)
    elif isinstance(config, dict):
        return {k: resolve_config_recursively(v, globals_data) for k, v in config.items()}
    elif isinstance(config, list):
        return [resolve_config_recursively(item, globals_data) for item in config]
    else:
        return config
