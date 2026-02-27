---
title: "CRI-CORE Enforcement Contract"
filetype: "documentation"
type: "specification"
domain: "enforcement"
version: "0.5.0"
status: "Active"
created: "2026-02-27"
updated: "2026-02-27"
license: "Apache-2.0"

author:
  name: "Shawn C. Wright"
  email: "swright@waveframelabs.org"
  orcid: "https://orcid.org/0009-0006-6043-9295"

maintainer:
  name: "Waveframe Labs"
  url: "https://waveframelabs.org"

ai_assisted: "partial"

anchors:
  - "CRI-CORE-ENFORCEMENT-CONTRACT-v0.5.0"
---

# CRI-CORE Enforcement Contract (v0.5.0)

## 1. Scope

CRI-CORE is a deterministic enforcement engine that validates structural and cryptographic invariants for governed run artifacts.

It enforces:

- Run structure requirements
- Contract version gating
- Lifecycle conformity
- Identity independence and role separation
- Cryptographic integrity
- Binding invariants
- Repository publication gating

It does not interpret claim content, evaluate correctness, or enforce domain semantics.

Passing CRI-CORE indicates structural compliance only.

---

## 2. Canonical Enforcement Pipeline

The pipeline executes in the following normative order:

1. run-structure
2. structure-contract-version-gate
3. lifecycle-contract-conformity
4. independence
5. integrity
6. integrity-finalization
7. publication
8. publication-commit

No stage may be skipped.

`publication-commit` defines `commit_allowed`.

---

## 3. Run Artifact Contract

### 3.1 Required Before Finalization

A valid run directory MUST contain:

- `contract.json`
- `report.md`
- `randomness.json`
- `approval.json`
- `validation/` (machine validation outputs)

### 3.2 Required After Finalization

Finalization MUST produce:

- `SHA256SUMS.txt`
- `payload.tar.gz`

If `contract_version >= 0.3.0`, finalization MUST also produce:

- `binding.json`
- `SEAL.json`

---

## 4. Independence Enforcement

If `required_roles` is declared:

- `identities` MUST be present.
- Each required role MUST be satisfied.
- No identity may hold more than one required role.

If identities are missing → FAIL.  
If required_roles is absent → structural pass.

Independence enforcement is structural only.

---

## 5. Integrity Enforcement

### 5.1 Integrity Stage (Non-Mutating)

The integrity stage:

- Validates integrity section presence in run context.
- Verifies `SHA256SUMS.txt` when present.
- Performs no writes.

### 5.2 Integrity-Finalization Stage (Mutating)

Finalization writes:

- `payload.tar.gz`
- `SHA256SUMS.txt`
- `binding.json` (>=0.3.0)
- `SEAL.json` (>=0.3.0)

Finalization MUST NOT execute if prior stages failed.

---

## 6. Binding Invariant (>= 0.3.0)

`binding.json` MUST:

- Hash `contract.json`
- Hash the artifact declared via `claim_ref`
- Hash `approval.json` (if present)
- Produce deterministic `binding_hash`

Binding is structural and cryptographic only.

---

## 7. Seal Invariant (>= 0.3.0)

`SEAL.json` MUST:

- Hash all files recursively under the run directory
- Exclude `SEAL.json`, `payload.tar.gz`, and `SHA256SUMS.txt` from file recursion
- Include `sha256sums_hash` and `payload_hash` when present
- Produce deterministic `seal_hash`

The seal provides tamper-evidence for the full run surface.

---

## 8. Failure Semantics

Enforcement fails if:

- Required artifacts are missing
- Integrity verification fails
- Independence rules are violated
- Binding mismatch occurs
- Seal mismatch occurs
- Stage ordering is violated

Failure blocks `publication-commit`.

---

## 9. Versioning

This contract follows semantic versioning:

- MAJOR — Breaking enforcement changes
- MINOR — Backward-compatible enforcement additions
- PATCH — Editorial or diagnostic updates

Historical runs MUST be interpreted under their declared `contract_version`.

Silent enforcement changes are prohibited.
