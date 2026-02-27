# Changelog

All notable changes to CRI-CORE are documented here.

This project follows semantic versioning (0.x pre-stable).

---

## [0.5.0] – 2026-02-27

### Added
- Structural binding enforcement (binding.json required for contract_version >= 0.3.0)
- Recursive SEAL verification
- Version-gated invariant enforcement
- Non-mutating binding and seal verification logic
- Tamper test coverage for binding + seal mismatch

### Changed
- Integrity stage now enforces binding + seal for >= 0.3.0
- finalize_run_integrity expanded artifact surface (binding + seal materialization)

### Compatibility
- Backwards compatible with contract_version < 0.3.0
- No enforcement pipeline interface break

---

## [0.4.1] - 2026-02-19

This release formalizes CRI-CORE as a deterministic enforcement pipeline for structural run admissibility and atomic commit gating.

## Core Capabilities

- Deterministic, ordered enforcement pipeline
- Explicit stage identifiers
- Typed failure classes
- Structural run validation
- Contract version gating
- Independence (authority boundary) enforcement
- Cryptographic integrity verification (SHA256 manifest validation)
- Integrity finalization gating
- Publication context validation
- Atomic commit authorization via centralized commit_allowed

## Architectural Boundary

CRI-CORE v0.4.1:

- Does not mutate domain objects
- Does not interpret lifecycle semantics
- Does not enforce distributed consensus
- Does not prevent external bypass outside its invocation boundary

It authorizes mutation attempts deterministically when invoked, based on structural, authority, integrity, and publication constraints.

## Intended Scope (v0.x)

This release establishes:

- A stable enforcement interface (run_enforcement_pipeline)
- Explicit commit semantics
- Deterministic stage ordering

Future releases may expand enforcement scope, environmental constraints, and non-bypassability guarantees.

---

## [0.1.0]

- Enforcement pipeline (structure, independence, integrity, publication)
- Deterministic commit gating
- Run artifact contract