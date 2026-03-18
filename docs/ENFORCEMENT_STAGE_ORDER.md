---
title: "CRI-CORE Canonical Enforcement Stage Order"
filetype: "documentation"
type: "specification"
domain: "enforcement"
version: "0.3.0"
status: "Active"
created: "2026-02-19"
updated: "2026-03-17"
license: "Apache-2.0"
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
  Enforces deterministic binding between the proposal and the compiled contract artifact.

  The proposal-declared `contract.hash` MUST exactly match the `contract_hash`
  of the compiled contract artifact present in the run.

  This stage guarantees that:
  - the proposal is bound to the exact contract evaluated by CRI-CORE
  - contract substitution or mutation between proposal construction and enforcement is not possible

  Failure results in immediate rejection of the proposal as structurally invalid.

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

- All stages are emitted in order.
- No stage may be skipped.
- Later stages MAY execute but MUST NOT override failure states of prior stages.
- `publication-commit` is the sole commit gate.
- `commit_allowed` is defined as the pass state of `publication-commit`.

Stage identifiers are defined in:

`cricore/enforcement/stage_ids.py`

This ordering is considered part of the CRI-CORE enforcement contract surface.