# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [Unreleased]

## [1.0.5] - 2026-08-07

- Release: Prepared the approved tooling/documentation patch release `1.0.5`.
- Tooling: Expanded schema self-validation, canonical-catalog validation, negative fixtures, and handwritten range validation tests.
- Docs: Updated maintainer validation evidence. The canonical profile JSON, published JSON Schema contract, and generated reference-table data are unchanged from `v1.0.4`.

### Fixed

- Tooling: CI now validates the published JSON Schema itself and the canonical profile catalog
  against it, with a maintained negative fixture proving that undeclared profile fields fail.
- Tooling: Handwritten profile validation now rejects reversed, duplicate, and overlapping range
  lists while leaving the canonical profile JSON and generated reference tables unchanged.

## [1.0.4] - 2026-07-29

- Release: Added a validated tag/manual workflow that creates a draft GitHub Release with this version's changelog section prepended to generated notes.

### BREAKING

- Data: Removed obsolete command upper-bit flags and derived response routes from the schema, canonical profiles, generated reference tables, and validation tools. Implementations must use structural command/response classification.

## [1.0.3] - 2026-07-13

### Fixed

- Tooling: Reject duplicate JSON object keys during profile validation.

## [1.0.2] - 2026-07-06

### Changed

- Docs: Restyled generated profile-reference tables to match the shared SLMP manual style, including generated headers, purpose text, verified-model status, plain table cells, cell-reading appendices, user-readable addressing labels, and transposed area-range matrices.

## [1.0.1] - 2026-07-05

### Changed

- Data: Shortened TOYOPUC profile display names by removing the trailing `mode` wording from mode labels.

## [1.0.0] - 2026-07-05

### Added

- Data: Added the initial canonical TOYOPUC Computer Link profile catalog.
