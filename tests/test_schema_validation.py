from __future__ import annotations

import copy
import sys
import unittest
from pathlib import Path

from jsonschema.exceptions import SchemaError


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from validate_schema import load_json, validate_schema_and_instance  # noqa: E402


class PublishedSchemaTests(unittest.TestCase):
    def setUp(self) -> None:
        self.schema = load_json(ROOT / "schema" / "toyopuc_profiles.schema.json")

    def test_published_schema_accepts_canonical_catalog(self) -> None:
        catalog = load_json(ROOT / "capability" / "toyopuc_profiles.json")

        validate_schema_and_instance(self.schema, catalog)

    def test_unknown_profile_property_fixture_is_rejected_with_path(self) -> None:
        fixture = load_json(ROOT / "tests" / "fixtures" / "invalid_unknown_profile_property.json")

        with self.assertRaisesRegex(ValueError, r"\$\.profiles\.toyopuc:negative-fixture") as raised:
            validate_schema_and_instance(self.schema, fixture)

        self.assertIn("unknown_contract_field", str(raised.exception))

    def test_invalid_schema_is_rejected_before_instance_validation(self) -> None:
        invalid_schema = copy.deepcopy(self.schema)
        invalid_schema["type"] = 7

        with self.assertRaises(SchemaError):
            validate_schema_and_instance(invalid_schema, {})


if __name__ == "__main__":
    unittest.main()
