#!/usr/bin/env python3
"""
Schema Validator for Daily Raw Data
Validates JSON data against daily_raw_schema.json

Usage:
    python validate_schema.py <json_file>
    python validate_schema.py --stdin < <data.json>
"""

import sys
import json
import jsonschema
from pathlib import Path

SCHEMA_PATH = Path(__file__).parent / "daily_raw_schema.json"


def load_schema():
    with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def validate(data: dict, schema: dict) -> tuple[bool, list[str]]:
    """Validate data against schema. Returns (is_valid, errors)."""
    errors = []
    try:
        jsonschema.validate(instance=data, schema=schema)
        return True, []
    except jsonschema.ValidationError as e:
        return False, [e.message]
    except jsonschema.SchemaError as e:
        return False, [f"Schema error: {e.message}"]


def main():
    schema = load_schema()
    
    if len(sys.argv) > 1 and sys.argv[1] == "--stdin":
        data = json.load(sys.stdin)
    elif len(sys.argv) > 1:
        with open(sys.argv[1], "r", encoding="utf-8") as f:
            data = json.load(f)
    else:
        print(f"Usage: {sys.argv[0]} <json_file>")
        print(f"   or: {sys.argv[0]} --stdin")
        sys.exit(1)
    
    is_valid, errors = validate(data, schema)
    
    if is_valid:
        print("✅ Validation passed")
        sys.exit(0)
    else:
        print("❌ Validation failed:")
        for err in errors:
            print(f"   - {err}")
        sys.exit(1)


if __name__ == "__main__":
    main()
