"""Minimal jsonschema stub for offline environments."""
from __future__ import annotations
from typing import Any


def validate(instance: Any, schema: dict) -> None:
    """Very small subset validator handling only 'required' and object properties."""
    required = schema.get("required", [])
    for key in required:
        if key not in instance:
            raise ValueError(f"Missing required key: {key}")
    # Nested validations for known objects
    for prop, subschema in schema.get("properties", {}).items():
        if prop in instance and isinstance(instance[prop], dict) and subschema.get("type") == "object":
            validate(instance[prop], subschema)
        if prop in instance and isinstance(instance[prop], list) and subschema.get("type") == "array":
            item_schema = subschema.get("items", {})
            for item in instance[prop]:
                if isinstance(item, dict):
                    validate(item, item_schema)
