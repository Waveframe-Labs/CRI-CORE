---
title: "CRI-CORE Enforcement Contract"
filetype: "documentation"
type: "specification"
domain: "enforcement"
version: "0.12.0"
status: "Active"
created: "2026-02-27"
updated: "2026-04-01"
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
  - "CRI-CORE-ENFORCEMENT-CONTRACT-v0.12.0"
  - "Execution Boundary Enforcement Contract"
---

# CRI-CORE Enforcement Contract (v0.12.0)

## 1. Scope

CRI-CORE is a deterministic enforcement kernel that determines whether a proposed state mutation is allowed to execute.

It operates at the execution boundary.

The kernel evaluates structural, authority, integrity, binding, and publication constraints over a run artifact and produces a single outcome:

- execution allowed  
- execution blocked  

CRI-CORE enforces:

- Run structure requirements  
- Contract version gating  
- Contract identity binding  
- Identity independence and role separation  
- Cryptographic integrity and finalization  
- Publication gating  
- Commit authorization  

CRI-CORE does not:

- Interpret claim content  
- Evaluate correctness or truth  
- Enforce domain semantics  
- Resolve external system state  
- Perform lifecycle orchestration  

Passing CRI-CORE indicates that execution is structurally admissible.

Failing CRI-CORE prevents execution.

---

## 2. Enforcement Model

CRI-CORE is not a validation layer.

It is an execution control mechanism.

The kernel does not produce advisory output.

It produces a deterministic authorization decision:

```

commit_allowed ∈ {true, false}

```

If `commit_allowed = false`, the mutation MUST NOT execute.

The kernel does not enforce execution externally.

It defines the boundary at which execution is permitted or denied.

---

## 3. Canonical Enforcement Pipeline

The pipeline executes in the following deterministic order:

1. run-structure  
2. structure-contract-version-gate  
3. structure-contract-hash-gate  
4. independence  
5. integrity  
6. integrity-finalization  
7. publication  
8. publication-commit  

The stage order is fixed.

`publication-commit` defines the execution decision:

```

commit_allowed = publication_commit_stage.passed

```

No subsequent stage may override this decision.

---

## 4. Contract Binding Enforcement

CRI-CORE enforces deterministic binding between a mutation proposal and the compiled governance contract used during enforcement.

A proposal MUST reference the governing contract using:

```

contract.id
contract.version
contract.hash

```

During enforcement:

```

proposal.contract.hash == compiled_contract.contract_hash

```

If this condition fails:

- the run is rejected  
- execution is blocked  

This ensures that a proposal cannot be evaluated under a different contract than the one it was created against.

The kernel verifies contract identity only.

It does not interpret governance policy structure.

---

## 5. Run Artifact Contract

### 5.1 Required Before Finalization

A valid run directory MUST contain:

- `contract.json`  
- `report.md`  
- `randomness.json`  
- `approval.json`  
- `validation/`  

These artifacts define the proposed mutation context prior to sealing.

---

### 5.2 Required After Finalization

Finalization MUST produce:

- `SHA256SUMS.txt`  
- `payload.tar.gz`  

If `contract_version >= 0.3.0`, finalization MUST also produce:

- `binding.json`  
- `SEAL.json`  

A finalized run is immutable.

Any modification invalidates enforcement.

---

## 6. Independence Enforcement

If `required_roles` is declared:

- `identities` MUST be present  
- Each required role MUST be satisfied  
- No identity may satisfy more than one required role  

Violations result in:

- enforcement failure  
- execution blocked  

If `required_roles` is absent:

- independence passes structurally  

Independence is enforced at the level of identity structure only.

---

## 7. Integrity Enforcement

### 7.1 Integrity Stage (Non-Mutating)

The integrity stage:

- Verifies presence of integrity context  
- Validates `SHA256SUMS.txt` if present  
- Performs no writes  

---

### 7.2 Integrity-Finalization Stage (Mutating)

Finalization produces:

- `payload.tar.gz`  
- `SHA256SUMS.txt`  
- `binding.json` (>= 0.3.0)  
- `SEAL.json` (>= 0.3.0)  

Finalization MUST NOT execute if any prior stage has failed.

---

## 8. Binding Invariant (>= 0.3.0)

`binding.json` MUST:

- Hash `contract.json`  
- Hash the artifact declared via `claim_ref`  
- Hash `approval.json` (if present)  
- Produce deterministic `binding_hash`  

If `claim_ref` is declared:

- the referenced artifact MUST exist  
- its hash MUST be included  

Binding failure results in execution being blocked.

---

## 9. Seal Invariant (>= 0.3.0)

`SEAL.json` MUST:

- Hash all files recursively under the run directory  
- Exclude:
  - `SEAL.json`  
  - `payload.tar.gz`  
  - `SHA256SUMS.txt`  

- Include:
  - `sha256sums_hash`  
  - `payload_hash`  

- Produce deterministic `seal_hash`  

Any mismatch invalidates the run and blocks execution.

The seal provides tamper evidence over the entire run surface.

---

## 10. Failure Semantics

Enforcement fails if any stage fails.

Failure conditions include:

- Missing required artifacts  
- Contract binding mismatch  
- Independence violations  
- Integrity verification failure  
- Binding invariant violation  
- Seal invariant violation  
- Stage ordering violation  

If enforcement fails:

```

commit_allowed = false

```

Execution MUST NOT occur.

---

## 11. Versioning

This contract follows semantic versioning:

- MAJOR — Breaking enforcement behavior  
- MINOR — Backward-compatible enforcement additions  
- PATCH — Editorial or diagnostic updates  

Each run is evaluated under its declared `contract_version`.

Enforcement behavior is version-isolated.

Silent changes to enforcement semantics are prohibited.

---

<div align="center">
  <sub>© 2026 Waveframe Labs — Independent Open-Science Research Entity</sub>
</div>
