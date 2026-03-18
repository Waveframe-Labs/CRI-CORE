---
title: "CRI-CORE Changelog"
filetype: "documentation"
type: "log"
domain: "enforcement"
version: "0.9.0"
doi: "TBD-0.9.0"
status: "Active"
created: "2026-02-19"
updated: "2026-03-17"

author:
  name: "Shawn C. Wright"
  email: "swright@waveframelabs.org"
  orcid: "https://orcid.org/0009-0006-6043-9295"

maintainer:
  name: "Waveframe Labs"
  url: "https://waveframelabs.org"

license: "Apache-2.0"

copyright:
  holder: "Waveframe Labs"
  year: "2026"

ai_assisted: "partial"

anchors:
  - "CRI-CORE-CHANGELOG-v0.9.0"
---
# Changelog

All notable changes to CRI-CORE are documented here.

This project follows semantic versioning (0.x pre-stable).

---

## [0.9.0] - 2026-03-17

### Added
- Explicit contract hash enforcement stage (`structure-contract-hash-gate`)
- Dedicated contract hash gate test suite
- Clear separation between run declaration (`contract.json`) and compiled contract artifact (`compiled_contract.json`)

### Changed
- Enforcement pipeline now explicitly includes deterministic contract binding stage
- Stage ordering documentation updated to reflect full canonical pipeline
- Improved failure reporting for contract binding violations

### Fixed
- Alignment between enforcement pipeline stage count and test expectations
- Structural validation consistency across run fixtures

### Notes
- This release clarifies the enforcement boundary between proposal construction and runtime evaluation.
- Deterministic contract binding is now explicitly enforced as a first-class stage in the pipeline.

---

## [0.8.0] - 2026-03-11

### Added
- Deterministic contract identity binding between proposals and compiled contract artifacts
- New enforcement stage: `structure-contract-hash-gate`
- Contract hash validation during enforcement

### Changed
- Enforcement pipeline expanded to include contract identity verification
- Proposal schema now requires:
  - `contract.hash`
- Compiled contract schema now requires:
  - `contract_hash`

### Documentation
- Kernel invariants specification expanded
- Enforcement contract specification updated
- Compiled contract interface documentation updated
- Canonical stage order documentation updated

### Security
- Prevents contract substitution between proposal creation and enforcement
- Ensures proposals are bound to the exact compiled contract evaluated at runtime

### Breaking Changes
- Proposal schema requires `contract.hash`
- Compiled contract schema requires `contract_hash`
- External tooling must align with updated schemas

### Compatibility
- Compatible with existing run artifact structures
- Changes affect proposal and compiled contract schemas only

---

## [0.7.0] - 2026-03-10

### Added
- Canonical proposal object schema (`schema/proposal.schema.json`)
- Proposal validation fixtures (`tests/fixtures/proposals`)
- Proposal schema validation test suite
- Compiled contract interface specification (`docs/compiled_contract_interface.md`)
- Compiled contract artifact schema (`schema/contract.schema.json`)
- Contract validation fixtures (`tests/fixtures/contracts`)
- Contract schema validation test suite

### Changed
- Hardening of runtime interface around proposal → enforcement → commit decision
- Kernel input surfaces now explicitly structured around proposal objects and run artifacts

### Notes
- Deterministic input validation introduced for proposals and compiled contract artifacts
- Contract artifact schema is intended for external compiler tooling and not interpreted directly by CRI-CORE runtime

---

## [0.6.0] – 2026-03-02

### Added
- First public PyPI distribution of CRI-CORE
- Runtime version exposure via `cricore.__version__`
- Hardened packaging metadata (classifiers, keywords, project URLs)

### Changed
- Version bump to establish public release baseline

### Compatibility
- No changes to enforcement pipeline interface
- No changes to stage semantics
- Backwards compatible with v0.5.0 contract behavior

---

## [0.5.0] – 2026-02-27

### Added
- Structural binding enforcement (`binding.json` required for contract_version ≥ 0.3.0)
- Recursive SEAL verification
- Version-gated invariant enforcement
- Non-mutating binding and seal verification logic
- Tamper test coverage for binding and seal mismatch

### Changed
- Integrity stage enforces binding + seal for ≥ 0.3.0
- finalize_run_integrity expanded artifact surface

### Compatibility
- Backwards compatible with contract_version < 0.3.0
- No enforcement pipeline interface break

---

## [0.4.1] - 2026-02-19

This release formalizes CRI-CORE as a deterministic enforcement pipeline for structural run admissibility and atomic commit gating.

### Core Capabilities
- Deterministic, ordered enforcement pipeline
- Explicit stage identifiers
- Typed failure classes
- Structural run validation
- Contract version gating
- Independence enforcement
- Cryptographic integrity verification (SHA256)
- Integrity finalization gating
- Publication validation
- Atomic commit authorization via `commit_allowed`

### Architectural Boundary
CRI-CORE:
- Does not mutate domain objects
- Does not interpret lifecycle semantics
- Does not enforce distributed consensus

### Intended Scope (v0.x)
- Stable enforcement interface
- Deterministic stage ordering
- Explicit commit semantics

---

## [0.1.0]

- Initial enforcement pipeline
- Deterministic commit gating
- Run artifact contract