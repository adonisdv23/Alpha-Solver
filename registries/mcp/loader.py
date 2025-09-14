from __future__ import annotations

"""MCP registry loader and helpers."""

import copy
import json
import os
from pathlib import Path
from typing import Any, Dict, List, Tuple, Union

import yaml
try:  # pragma: no cover - prefer real jsonschema
    from jsonschema import Draft7Validator, ValidationError
except Exception:  # pragma: no cover - fallback to stub
    from jsonschema import validate  # type: ignore

    class ValidationError(Exception):
        """Raised on registry validation failures."""

        def __init__(self, message: str):
            super().__init__(message)
            self.message = message

    class _Err:
        def __init__(self, message: str):
            self.message = message

    class Draft7Validator:  # minimal stub
        def __init__(self, schema: Dict[str, Any]):
            self.schema = schema

        def iter_errors(self, instance: Dict[str, Any]):
            try:
                validate(instance, self.schema)
                return []
            except Exception as exc:  # pylint: disable=broad-except
                return [_Err(str(exc))]

# ---------------------------------------------------------------------------
# Schema definition
# ---------------------------------------------------------------------------

TOOL_SCHEMA: Dict[str, Any] = {
    "type": "object",
    "required": ["name", "type", "entry"],
    "additionalProperties": False,
    "properties": {
        "name": {"type": "string", "pattern": r"^[a-z0-9]+(-[a-z0-9]+)*$"},
        "type": {"type": "string", "enum": ["http", "script", "remote"]},
        "entry": {"type": "string"},
        "timeout_ms": {"type": "integer", "minimum": 0, "default": 15000},
        "enabled": {"type": "boolean", "default": True},
        "retry": {
            "type": "object",
            "required": ["max_retries", "base_ms", "factor", "jitter"],
            "additionalProperties": False,
            "properties": {
                "max_retries": {"type": "integer", "minimum": 0, "maximum": 2},
                "base_ms": {"type": "integer", "minimum": 0},
                "factor": {"type": "number"},
                "jitter": {"type": "number"},
            },
        },
        "secrets": {
            "type": "object",
            "additionalProperties": {"type": "string"},
        },
    },
}

REGISTRY_SCHEMA: Dict[str, Any] = {
    "type": "object",
    "required": ["tool"],
    "additionalProperties": False,
    "properties": {
        "version": {"type": "string"},
        "tool": {"type": "array", "items": TOOL_SCHEMA},
    },
}


class SecretStr(str):
    """String subclass that redacts its value in representations."""

    def __repr__(self) -> str:  # pragma: no cover - trivial
        return "****"

    __str__ = __repr__


Registry = Dict[str, Any]


def _apply_defaults(registry: Registry) -> None:
    for tool in registry.get("tool", []):
        tool.setdefault("timeout_ms", 15000)
        tool.setdefault("enabled", True)


def validate_registry(obj: Registry) -> Tuple[bool, List[str]]:
    """Validate the registry object against the schema."""
    validator = Draft7Validator(REGISTRY_SCHEMA)
    errors = [e.message for e in validator.iter_errors(obj)]
    if not errors:
        # ensure unique tool names
        names = [t["name"] for t in obj.get("tool", [])]
        seen = set()
        duplicates = [n for n in names if n in seen or seen.add(n)]
        if duplicates:
            errors.append(f"duplicate tool names: {', '.join(sorted(set(duplicates)))}")
    return (len(errors) == 0, errors)


def load_registry(path_or_obj: Union[str, Path, Registry], *, resolve_env: bool = True) -> Registry:
    """Load and validate a registry from a path or pre-parsed object."""
    if isinstance(path_or_obj, (str, Path)):
        path = Path(path_or_obj)
        if not path.exists():
            raise FileNotFoundError(str(path))
        suffix = path.suffix.lower()
        with path.open("r", encoding="utf-8") as fh:
            if suffix == ".json":
                obj = json.load(fh)
            elif suffix in {".yaml", ".yml"}:
                obj = yaml.safe_load(fh)
            else:
                raise ValueError(f"unsupported registry format: {suffix}")
    else:
        obj = copy.deepcopy(path_or_obj)

    ok, errs = validate_registry(obj)
    if not ok:
        raise ValidationError("; ".join(errs))

    _apply_defaults(obj)

    if resolve_env:
        for tool in obj.get("tool", []):
            secrets = tool.get("secrets", {})
            resolved: Dict[str, Any] = {}
            for key in secrets:
                value = os.environ.get(key)
                if value is not None:
                    resolved[key] = SecretStr(value)
                else:
                    resolved[key] = None
            if resolved:
                tool["secrets"] = resolved

    return obj


def list_tools(registry: Registry) -> List[str]:
    """Return a list of enabled tool names."""
    return [t["name"] for t in registry.get("tool", []) if t.get("enabled", True)]


def get_tool(registry: Registry, name: str) -> Dict[str, Any] | None:
    """Return a deep copy of the named tool if enabled, else ``None``."""
    for tool in registry.get("tool", []):
        if tool.get("name") == name and tool.get("enabled", True):
            return copy.deepcopy(tool)
    return None

