---
title: "CRI-CORE Changelog"
filetype: "documentation"
type: "log"
domain: "enforcement"
version: "0.8.0"
doi: "TBD-0.8.0"
status: "Active"
created: "2026-02-19"
updated: "2026-03-11"

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
  - "CRI-CORE-CHANGELOG-v0.8.0"
---

# Changelog

All notable changes to CRI-CORE are documented here.

This project follows semantic versioning (0.x pre-stable).
---

## [0.8.0] – 2026-03-11

### Added
- Deterministic compiled contract binding via `structure-contract-hash-gate`.
- Proposal contract hash requirement (`contract.hash`) in the canonical proposal schema.
- `contract_hash` field in compiled contract schema.
- Enforcement stage verifying proposal → compiled contract integrity binding.

### Changed
- Canonical enforcement pipeline now includes the contract hash gate:

  1. run-structure  
  2. structure-contract-version-gate  
  3. structure-contract-hash-gate  
  4. independence  
  5. integrity  
  6. integrity-finalization  
  7. publication  
  8. publication-commit  

- Stage registry (`stage_ids.py`) updated to include `structure-contract-hash-gate`.
- Pipeline execution test updated to reflect the 8-stage pipeline.
- Contract and proposal fixtures updated to include required hash fields.

### Security
- Proposals are now cryptographically bound to the compiled governance contract used by the run.
- Prevents contract substitution and governance drift between proposal submission and enforcement evaluation.

### Compatibility
- Breaking change for proposal and contract schemas:
  - Proposals must now include `contract.hash`.
  - Compiled contracts must include `contract_hash`.
- Existing fixtures and schemas have been updated accordingly.
- 
---

## [0.7.1] – 2026-03-10

### Fixed
- Resolved specification/runtime drift in the canonical enforcement pipeline definition.
- Removed non-executed `lifecycle-contract-conformity` stage from canonical stage identifiers.
- Aligned enforcement contract documentation with the actual 7-stage runtime pipeline.
- Updated canonical stage order documentation to match runtime behavior.
- Corrected stale test commentary referencing an 8-stage pipeline.
- Clarified compiled contract interface as an external governance artifact rather than a direct CRI-CORE runtime input.

### Changed
- Canonical enforcement pipeline definition is now explicitly:

  1. run-structure  
  2. structure-contract-version-gate  
  3. independence  
  4. integrity  
  5. integrity-finalization  
  6. publication  
  7. publication-commit  

- Documentation now accurately reflects the deterministic runtime behavior of the CRI-CORE kernel.

### Compatibility
- No changes to the runtime enforcement pipeline implementation.
- No changes to enforcement semantics.
- Fully backwards compatible with v0.7.0 artifacts and contract behavior.

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
- These changes introduce deterministic input validation for governance proposals and compiled contract artifacts.
- The contract artifact schema is intended for use by external contract compiler tooling and is not interpreted directly by the CRI-CORE enforcement runtime.

---

## [0.6.0] – 2026-03-02

### Added
- First public PyPI distribution of CRI-CORE
- Explicit runtime version exposure via `cricore.__version__`
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