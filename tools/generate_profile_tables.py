#!/usr/bin/env python3
"""Generate Markdown comparison tables from the canonical TOYOPUC JSON."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "capability" / "toyopuc_profiles.json"
TABLE_DIR = ROOT / "tables"
OPTION_KEYS = [
    "use_upper_u_pc10",
    "use_eb_pc10",
    "use_fr_pc10",
    "use_upper_bit_pc10",
    "use_upper_m_bit_pc10",
]


def load_catalog() -> dict[str, Any]:
    return json.loads(CATALOG.read_text(encoding="utf-8"))


def cell(value: object) -> str:
    text = "" if value is None else str(value)
    text = text.replace("|", "\\|")
    return text if text in {"", "-"} else f"`{text}`"


def markdown_table(headers: list[str], rows: list[list[object]]) -> str:
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(cell(value) for value in row) + " |")
    return "\n".join(lines)


def yes_no(value: bool) -> str:
    return "yes" if value else "no"


def format_range(range_value: dict[str, int], width: int) -> str:
    return f"{range_value['start']:0{width}X}..{range_value['end']:0{width}X}"


def format_ranges(ranges: list[dict[str, int]], width: int) -> str:
    return ", ".join(format_range(range_value, width) for range_value in ranges) if ranges else "-"


def profile_table(payload: dict[str, Any]) -> str:
    rows: list[list[object]] = []
    for profile_id, profile in payload["profiles"].items():
        options = profile["addressing_options"]
        rows.append(
            [
                profile_id,
                profile["display_name"],
                len(profile["areas"]),
                *[yes_no(options[key]) for key in OPTION_KEYS],
            ]
        )
    body = markdown_table(
        ["Profile ID", "Display name", "Areas", *OPTION_KEYS],
        rows,
    )
    return (
        "# TOYOPUC Computer Link Profile Parameters\n\n"
        "Generated from `capability/toyopuc_profiles.json`.\n\n"
        f"{body}\n"
    )


def area_table(payload: dict[str, Any]) -> str:
    rows: list[list[object]] = []
    for profile_id, profile in payload["profiles"].items():
        for area in profile["areas"]:
            width = area["address_width"]
            rows.append(
                [
                    profile_id,
                    area["area"],
                    format_ranges(area["direct_ranges"], width),
                    format_ranges(area["prefixed_ranges"], width),
                    yes_no(area["supports_packed_word"]),
                    width,
                    f"0x{area['suggested_start_step']:X}",
                    format_ranges(area.get("packed_direct_ranges_override", []), max(1, width - 1)),
                    format_ranges(area.get("packed_prefixed_ranges_override", []), max(1, width - 1)),
                ]
            )
    body = markdown_table(
        [
            "Profile ID",
            "Area",
            "Direct ranges",
            "Prefixed ranges",
            "Packed word",
            "Width",
            "Step",
            "Packed direct override",
            "Packed prefixed override",
        ],
        rows,
    )
    return (
        "# TOYOPUC Computer Link Area Ranges\n\n"
        "Generated from `capability/toyopuc_profiles.json`.\n\n"
        "A `-` value means that access form is not available for that area.\n\n"
        f"{body}\n"
    )


def write_or_check(path: Path, content: str, check: bool) -> bool:
    if check:
        current = path.read_text(encoding="utf-8") if path.exists() else None
        if current != content:
            print(f"stale generated table: {path.relative_to(ROOT)}")
            return False
        print(f"fresh generated table: {path.relative_to(ROOT)}")
        return True
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8", newline="\n")
    print(f"wrote {path.relative_to(ROOT)}")
    return True


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="fail if generated tables are stale")
    args = parser.parse_args()

    payload = load_catalog()
    outputs = {
        TABLE_DIR / "toyopuc_profile_parameters.md": profile_table(payload),
        TABLE_DIR / "toyopuc_area_ranges.md": area_table(payload),
    }
    ok = all(write_or_check(path, content, args.check) for path, content in outputs.items())
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())

