#!/usr/bin/env python3
"""Validate the canonical TOYOPUC Computer Link profile JSON."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "capability" / "toyopuc_profiles.json"
OPTION_KEYS = {
    "use_upper_u_pc10",
    "use_eb_pc10",
    "use_fr_pc10",
    "use_upper_bit_pc10",
    "use_upper_m_bit_pc10",
}


def _reject_duplicate_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def load_catalog() -> dict[str, Any]:
    return json.loads(CATALOG.read_text(encoding="utf-8"), object_pairs_hook=_reject_duplicate_keys)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def validate_ranges(profile_id: str, area: str, field: str, ranges: list[dict[str, int]]) -> None:
    for index, range_value in enumerate(ranges):
        start = range_value.get("start")
        end = range_value.get("end")
        require(isinstance(start, int) and isinstance(end, int), f"{profile_id}/{area}/{field}[{index}]: bad range")
        require(0 <= start <= end, f"{profile_id}/{area}/{field}[{index}]: start must be <= end")


def validate_catalog(payload: dict[str, Any]) -> None:
    require(payload.get("schema_version") == 1, "schema_version must be 1")
    require(payload.get("scope") == "toyopuc-computerlink", "unexpected scope")

    profiles = payload.get("profiles")
    require(isinstance(profiles, dict) and profiles, "profiles must be a non-empty object")

    for profile_id, profile in profiles.items():
        require(profile_id.startswith("toyopuc:"), f"{profile_id}: invalid vendor prefix")
        require(profile.get("display_name"), f"{profile_id}: display_name is required")

        options = profile.get("addressing_options")
        require(isinstance(options, dict), f"{profile_id}: addressing_options must be an object")
        require(set(options) == OPTION_KEYS, f"{profile_id}: addressing option keys do not match")
        for key, value in options.items():
            require(isinstance(value, bool), f"{profile_id}/{key}: option must be boolean")

        areas = profile.get("areas")
        require(isinstance(areas, list) and areas, f"{profile_id}: areas must be a non-empty array")
        seen_areas: set[str] = set()
        for area in areas:
            area_name = area.get("area")
            require(isinstance(area_name, str) and area_name, f"{profile_id}: area is required")
            require(area_name not in seen_areas, f"{profile_id}: duplicate area {area_name}")
            seen_areas.add(area_name)
            require(isinstance(area.get("supports_packed_word"), bool), f"{profile_id}/{area_name}: packed flag")
            require(isinstance(area.get("address_width"), int) and area["address_width"] > 0, f"{profile_id}/{area_name}: width")
            require(
                isinstance(area.get("suggested_start_step"), int) and area["suggested_start_step"] > 0,
                f"{profile_id}/{area_name}: suggested_start_step",
            )
            for field in ("direct_ranges", "prefixed_ranges"):
                ranges = area.get(field)
                require(isinstance(ranges, list), f"{profile_id}/{area_name}/{field}: must be an array")
                validate_ranges(profile_id, area_name, field, ranges)
            for field in ("packed_direct_ranges_override", "packed_prefixed_ranges_override"):
                if field in area:
                    require(area["supports_packed_word"], f"{profile_id}/{area_name}/{field}: packed flag required")
                    ranges = area[field]
                    require(isinstance(ranges, list), f"{profile_id}/{area_name}/{field}: must be an array")
                    validate_ranges(profile_id, area_name, field, ranges)


def main() -> int:
    validate_catalog(load_catalog())
    print(f"validated {CATALOG.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
