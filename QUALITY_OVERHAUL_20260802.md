# Quality Overhaul Decisions — 2026-08-02

## COMPUTERLINK-PROFILES-REAUDIT-003 — Enforce ordered, non-overlapping ranges

Status: implemented and verified on 2026-08-02.

Stable ID: `COMPUTERLINK-PROFILES-REAUDIT-003`.

### Implementation scope

This item covers the handwritten semantic range validator in `tools/validate_profiles.py`, its
boundary tests in `tests/test_profile_validation.py`, the validation explanation in `README.md`,
this maintainer record, and `CHANGELOG.md`. The implementation, boundary tests, and README were
already present on the verified `main` source state and remain unchanged by this documentation
update.

The canonical `capability/toyopuc_profiles.json`, its published JSON Schema, generated tables,
profile IDs, area definitions, runtime fixtures, downstream import contract, and schema version are
outside the implementation delta. This validator establishes only the internal ordering validity of
catalog range lists. It does not turn catalog ranges into communication-library pre-send guards or
claim that a listed address is usable on a particular PLC, route, or configuration.

### Target contract

For every direct, prefixed, packed-direct-override, and packed-prefixed-override range list, each
range must contain integer `start` and `end` values with `0 <= start <= end`. Starting with the
second element, `start` must be strictly greater than the immediately preceding `end`. The
handwritten validator therefore rejects descending order, duplicate ranges, partial overlap, full
overlap, and containment. Empty and single-element lists retain their existing behavior.

Validation remains a local maintenance gate. It does not modify the canonical catalog, generated
tables, downstream runtime data, communication frames, address policy, or PLC behavior.

Compatibility impact: the current canonical catalog remains valid and consumers receive identical
profile data. The intentional tightening affects only future invalid catalog edits that previously
could pass handwritten validation despite being out of order or overlapping. Such edits now fail
with a path-and-index-specific `ValueError` before they can be distributed or used to regenerate
reference tables. No consumer migration is required for valid profile data.

### Machine-verifiable acceptance criteria

1. The current canonical `capability/toyopuc_profiles.json` passes both the published schema and the
   handwritten semantic validator without modification.
2. A range whose `start` and `end` are individually valid but whose position is descending relative
   to the preceding range is rejected with the strict-order/non-overlap diagnostic.
3. An exact duplicate of a preceding range is rejected with the same diagnostic.
4. A later range that partially overlaps, fully overlaps, or is contained by the preceding range is
   rejected because its `start` is not greater than the preceding `end`.
5. Consecutive non-overlapping ranges pass when the later `start` is exactly one greater than the
   preceding `end`; this proves the accepted boundary and prevents an unintended gap requirement.
6. The rule is applied through `validate_catalog` to direct, prefixed, packed-direct-override, and
   packed-prefixed-override lists without changing their schema or generated representation.
7. README describes the handwritten rule as strictly ascending and non-overlapping, while retaining
   the distinction between catalog metadata, application-layer checks, and actual PLC acceptance.
8. Canonical JSON, schema, and generated reference-table bytes remain unchanged by this item, and
   the generator freshness check passes.
9. The repository's schema validation, handwritten validation, unit tests, Python syntax/bytecode
   compilation, generated-table check, and distributable-data/package-equivalent checks pass.
10. No live PLC verification is required because neither canonical facts nor any communication path,
    frame, route, address, read/write behavior, or runtime implementation changes.

### Verification evidence

Evidence was recorded on 2026-08-02 from branch `overhaul/reaudit-acceptance-20260802`, based on the
clean `main`/`origin/main` source state `27fb77c36cb3da37d8ed3a9df6e1b84734692a4c`.

- Published-schema validation passed for `schema/toyopuc_profiles.schema.json` and the canonical
  catalog instance.
- Handwritten semantic validation passed for the canonical catalog.
- Generated-table freshness passed for both `tables/toyopuc_profile_parameters.md` and
  `tables/toyopuc_area_ranges.md`.
- Unit discovery ran 8 tests successfully. The five semantic tests cover the canonical catalog,
  descending order, exact duplicate/full overlap, partial overlap, and the accepted adjacent
  boundary. The ordering predicate also rejects containment because every later `start` must exceed
  the preceding `end`.
- Python compilation passed for all files under `tools` and `tests`.
- This repository has no runtime package manifest or public-registry package artifact. Its
  package-equivalent distributable contract is the tracked canonical JSON, published schema, and
  generated tables; schema/semantic validation and generated freshness all passed for those files.
- The canonical JSON SHA-256 remained
  `D9605EEC37CB3330AE7C2825A8B54FD6E9329EAD902E9E290C4782E6C4B29238`. The schema SHA-256 remained
  `58A464218632BB6C11B1C713CF2B97F1FBD89C42887F305D97BBE5B449836A6B`.
- Generator output was unaffected: `toyopuc_profile_parameters.md` remained
  `24AABA61AEB4FB7739719D823FF5A43F7D96A40B7AC376E7AACFCAA201F689E6`, and
  `toyopuc_area_ranges.md` remained
  `955DD3F8A7F20E757A71E46F48EA339FDB74198EEAF679DE2E97B84786D384DB` by SHA-256.
- Live PLC disposition: not required. The accepted change is confined to deterministic local
  maintenance validation of list ordering, and the verified canonical data and all generated/runtime
  representations are unchanged.

### Codex self-review classification

The self-review inspected the implementation diff, validation order, error behavior, all range-list
call sites, boundary tests, README wording, canonical and schema files, generator inputs and outputs,
release/package shape, and compatibility with downstream application-layer range policy.

- Accepted: `REAUDIT-003`, the original missing strict ordering/non-overlap validation. It is fixed by
  comparing every later `start` with the preceding `end`, with deterministic boundary coverage.
- Rejected: none.
- Duplicate: none.
- Deferred: none.
- Remaining accepted findings after correction: none. The implementation checks element shape and
  each range's own bounds before cross-range ordering, reports the exact profile/area/field/index,
  applies to all four supported range-list fields, and does not weaken or expand runtime behavior.

### Acceptance tracking

- [x] Implementation completed in `plc-comm-computerlink-profiles`.
- [x] Tests added or updated for every acceptance criterion and boundary behavior.
- [x] Relevant schema checks, static checks, unit tests, generated checks, and
      package-equivalent distributable-data checks passed.
- [x] Codex self-review completed against the approved contract, actual implementation diff,
      validation order, error behavior, tests, documentation, generator, packaging shape, and
      cross-library range-policy consistency.
- [x] Live-PLC verification was explicitly determined not required, with the reason and release
      disposition recorded above.
- [x] README, maintainer record, changelog, canonical data, schema, and generated reference material
      agree with the implementation.
- [x] Final acceptance criteria were verified and this item is complete.
