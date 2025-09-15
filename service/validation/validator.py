import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List

SCHEMA_PATH = Path(__file__).parent / "schemas" / "request_schema.json"


@dataclass
class FieldError:
    """Structured validation error."""

    code: str
    field: str
    reason: str


class ValidationError(Exception):
    """Raised when request payload fails validation."""

    def __init__(self, errors: List[FieldError]):
        super().__init__("invalid request")
        self.errors = [e.__dict__ for e in errors]


def _load_schema() -> Dict[str, Any]:
    with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


SCHEMA = _load_schema()


def _validate(schema: Dict[str, Any], data: Any, path: str = "") -> List[FieldError]:
    errors: List[FieldError] = []
    t = schema.get("type")
    field = path.rstrip(".") or "<root>"
    if t == "object":
        if not isinstance(data, dict):
            return [FieldError("invalid_type", field, "expected object")]
        props = schema.get("properties", {})
        if not schema.get("additionalProperties", True):
            for key in data:
                if key not in props:
                    errors.append(FieldError("unknown_field", f"{field}.{key}" if field != "<root>" else key, "additional property not allowed"))
        for req in schema.get("required", []):
            if req not in data:
                errors.append(FieldError("missing_field", f"{field}.{req}" if field != "<root>" else req, "field required"))
        for key, subschema in props.items():
            if key in data:
                errors.extend(_validate(subschema, data[key], f"{field}.{key}" if field != "<root>" else f"{key}"))
    elif t == "string":
        if not isinstance(data, str):
            errors.append(FieldError("invalid_type", field, "expected string"))
        else:
            min_len = schema.get("minLength")
            if min_len is not None and len(data) < min_len:
                errors.append(FieldError("too_short", field, f"min length {min_len}"))
            max_len = schema.get("maxLength")
            if max_len is not None and len(data) > max_len:
                errors.append(FieldError("too_long", field, f"max length {max_len}"))
            enum = schema.get("enum")
            if enum is not None and data not in enum:
                errors.append(FieldError("invalid_value", field, f"expected one of {enum}"))
    elif t == "number":
        if not isinstance(data, (int, float)):
            errors.append(FieldError("invalid_type", field, "expected number"))
        else:
            minimum = schema.get("minimum")
            if minimum is not None and data < minimum:
                errors.append(FieldError("too_small", field, f"minimum {minimum}"))
            maximum = schema.get("maximum")
                
            if maximum is not None and data > maximum:
                errors.append(FieldError("too_large", field, f"maximum {maximum}"))
    elif t == "array":
        if not isinstance(data, list):
            errors.append(FieldError("invalid_type", field, "expected array"))
        else:
            item_schema = schema.get("items", {})
            for idx, item in enumerate(data):
                errors.extend(_validate(item_schema, item, f"{field}[{idx}]"))
    return errors


def validate_request(payload: Dict[str, Any]) -> None:
    """Validate *payload* against the request schema.

    Args:
        payload: Incoming request body.

    Raises:
        ValidationError: If the payload does not conform to the schema.
    """

    errors = _validate(SCHEMA, payload)
    if errors:
        raise ValidationError(errors)


__all__ = ["validate_request", "ValidationError"]
