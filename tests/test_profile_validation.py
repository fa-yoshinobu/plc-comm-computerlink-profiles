from __future__ import annotations

import copy
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from validate_profiles import load_catalog, validate_catalog, validate_ranges  # noqa: E402


class ProfileSemanticValidationTests(unittest.TestCase):
    def test_canonical_catalog_is_valid(self) -> None:
        validate_catalog(load_catalog())

    def test_reversed_ranges_are_rejected(self) -> None:
        with self.assertRaisesRegex(ValueError, "strictly ordered and non-overlapping"):
            validate_ranges(
                "toyopuc:test",
                "P",
                "prefixed_ranges",
                [{"start": 100, "end": 199}, {"start": 0, "end": 99}],
            )

    def test_duplicate_ranges_are_rejected(self) -> None:
        duplicate = {"start": 0, "end": 99}
        with self.assertRaisesRegex(ValueError, "strictly ordered and non-overlapping"):
            validate_ranges(
                "toyopuc:test",
                "P",
                "prefixed_ranges",
                [duplicate, copy.deepcopy(duplicate)],
            )

    def test_overlapping_ranges_are_rejected(self) -> None:
        with self.assertRaisesRegex(ValueError, "strictly ordered and non-overlapping"):
            validate_ranges(
                "toyopuc:test",
                "P",
                "prefixed_ranges",
                [{"start": 0, "end": 99}, {"start": 50, "end": 149}],
            )

    def test_ordered_non_overlapping_ranges_are_accepted(self) -> None:
        validate_ranges(
            "toyopuc:test",
            "P",
            "prefixed_ranges",
            [{"start": 0, "end": 99}, {"start": 100, "end": 199}],
        )


if __name__ == "__main__":
    unittest.main()
