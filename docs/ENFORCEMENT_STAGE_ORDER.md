---
title: "CRI-CORE Canonical Enforcement Stage Order"
filetype: "documentation"
type: "specification"
domain: "enforcement"
version: "0.2.2"
doi: "TBD-0.2.2"
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

dependencies:
  - "../execution.py"
  - "../stage_ids.py"

anchors:
  - "CRI-CORE-CANONICAL-STAGE-ORDER-v0.2.2"
---

# Canonical Enforcement Stage Order

The CRI-CORE enforcement pipeline executes the following stages in fixed, normative order:

1. run-structure
2. structure-contract-version-gate
3. structure-contract-hash-gate
4. independence
5. integrity
6. integrity-finalization
7. publication
8. publication-commit

## Stage Semantics (Normative Summary)

- **run-structure**  
  Validates structural conformity of the run artifact against the declared contract.

- **structure-contract-version-gate**  
  Enforces expected contract version alignment.

- **structure-contract-hash-gate**  
  Verifies that the contract hash declared in the proposal matches the hash of the compiled contract artifact used by the run.  
  This stage establishes deterministic binding between the proposal and the compiled governance contract.

- **independence**  
  Enforces structural role separation and override constraints.

- **integrity**  
  Performs non-mutating verification of:
  - SHA256SUMS (when present)
  - binding.json (required for contract_version ≥ 0.3.0)
  - SEAL.json (required for contract_version ≥ 0.3.0)

- **integrity-finalization**  
  Materializes deterministic integrity artifacts (mutating stage).

- **publication**  
  Validates publication references and structural publication invariants.

- **publication-commit**  
  The sole commit gate.

## Normative Guarantees

- All canonical stages are emitted in deterministic order.
- Later stages may return non-passing results if prior invariants fail.
- `publication-commit` is the sole commit gate.
- `commit_allowed` is defined as the pass state of `publication-commit`.

Stage identifiers are defined in:

`cricore/enforcement/stage_ids.py`

This ordering is considered part of the CRI-CORE enforcement contract surface.