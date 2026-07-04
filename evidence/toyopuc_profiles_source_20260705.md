# TOYOPUC Profile Source Notes 2026-07-05

## Scope

Initial canonicalization of TOYOPUC Computer Link profile IDs, display names,
addressing option flags, and per-area address ranges.

## Source Implementations

| Repository | File | Role |
| --- | --- | --- |
| `plc-comm-computerlink-dotnet` | `src/Toyopuc/ToyopucPlcProfiles.cs` and `ToyopucAddressingOptions.cs` | Primary source for profile definitions. |
| `plc-comm-computerlink-python` | `toyopuc/profiles.py` | Structured extraction source; the file states that it mirrors the .NET profile types. |

## Decision

Adopt the .NET profile model as the canonical behavior and use the Python mirror
to bootstrap the structured JSON. Downstream fixture tests in both
implementation repositories compare their embedded data against
`capability/toyopuc_profiles.json`.

No live PLC communication was performed for this canonicalization step.

