# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [Unreleased]

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
