#!/usr/bin/env python3
"""Validate the published JSON Schema and a TOYOPUC profile catalog instance."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from jsonschema import validators


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SCHEMA = ROOT / "schema" / "toyopuc_profiles.schema.json"
DEFAULT_INSTANCE = ROOT / "capability" / "toyopuc_profiles.json"


def _reject_duplicate_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=_reject_duplicate_keys)


def _json_path(parts: Any) -> str:
    path = "$"
    for part in parts:
        path += f"[{part}]" if isinstance(part, int) else f".{part}"
    return path


def validate_schema_and_instance(schema: dict[str, Any], instance: dict[str, Any]) -> None:
    validator_class = validators.validator_for(schema)
    validator_class.check_schema(schema)
    errors = sorted(validator_class(schema).iter_errors(instance), key=lambda error: list(error.absolute_path))
    if errors:
        details = "; ".join(f"{_json_path(error.absolute_path)}: {error.message}" for error in errors)
        raise ValueError(f"catalog does not match published schema: {details}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--schema", type=Path, default=DEFAULT_SCHEMA)
    parser.add_argument("--instance", type=Path, default=DEFAULT_INSTANCE)
    args = parser.parse_args()

    validate_schema_and_instance(load_json(args.schema), load_json(args.instance))
    print(f"validated schema {args.schema.relative_to(ROOT)}")
    print(f"validated instance {args.instance.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
