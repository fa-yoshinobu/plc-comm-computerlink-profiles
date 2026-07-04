[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

# TOYOPUC Computer Link Profiles

Canonical TOYOPUC Computer Link profile data shared by the
`plc-comm-computerlink-*` libraries.

The canonical profile definitions are [toyopuc_profiles.json](capability/toyopuc_profiles.json).
Downstream libraries should import a fixed tag from this repository and keep
fixture tests that compare their embedded data against the canonical JSON.

## Profile Data

The catalog defines canonical PLC profile IDs, short `display_name` values,
addressing option flags, and per-area direct/prefixed address ranges.

Ranges are catalog data for profile selection, UI address pickers, and
application-layer checks. The actual PLC model, link route, project settings,
and run/write permission can still reject a request.

## Supported PLC Profiles

- `toyopuc:generic`
- `toyopuc:plus:standard`
- `toyopuc:plus:extended`
- `toyopuc:nano-10gx:native`
- `toyopuc:nano-10gx:compatible`
- `toyopuc:pc10g:standard-pc3jg`
- `toyopuc:pc10g:pc10`
- `toyopuc:pc3jx:pc3-separate`
- `toyopuc:pc3jx:plus-expansion`
- `toyopuc:pc3jg:pc3jg`
- `toyopuc:pc3jg:pc3-separate`

## Documentation

| Page | Use it for |
| --- | --- |
| [Profile parameters](tables/toyopuc_profile_parameters.md) | Compare display names and addressing option flags. |
| [Area ranges](tables/toyopuc_area_ranges.md) | Compare direct and prefixed area ranges across profiles. |
| [Evidence](evidence/) | Review source notes used to adopt profile data. |

## Generate

Do not edit generated table files by hand.

```powershell
python tools/validate_profiles.py
python tools/generate_profile_tables.py
```

Use `--check` in CI to fail when generated tables are stale.

```powershell
python tools/generate_profile_tables.py --check
```

## Downstream Use

Implementation repositories should import a fixed tag and keep fixture tests
that compare their embedded profile data against this repository.

If a JSON schema changes, increment `schema_version` and keep the old tag
available until all downstream libraries have migrated.

## License

| Item | Value |
| --- | --- |
| License | [MIT](LICENSE) |
| Canonical data tag | `v1.0.0` or later |

