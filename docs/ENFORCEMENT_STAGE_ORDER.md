---
title: "CRI-CORE Canonical Enforcement Stage Order"
filetype: "documentation"
type: "specification"
domain: "enforcement"
version: "0.12.0"
status: "Active"
created: "2026-02-19"
updated: "2026-04-01"
license: "Apache-2.0"
---

# Canonical Enforcement Stage Order

The CRI-CORE enforcement pipeline executes the following stages in fixed, deterministic order:

1. run-structure  
2. structure-contract-version-gate  
3. structure-contract-hash-gate  
4. independence  
5. integrity  
6. integrity-finalization  
7. publication  
8. publication-commit  

This ordering defines the execution boundary evaluation sequence.

Each stage contributes to determining whether a proposed mutation is allowed to execute.

---

## Stage Semantics (Normative)

### run-structure  
Establishes structural admissibility of the run artifact.

Failure results in execution being blocked.

---

### structure-contract-version-gate  
Ensures compatibility between the run artifact and the expected contract version.

Failure results in execution being blocked.

---

### structure-contract-hash-gate  
Enforces deterministic binding between the proposal and the compiled contract artifact.

The proposal-declared `contract.hash` MUST match the compiled contract hash.

This guarantees that:

- the proposal is evaluated under the exact contract it was created against  
- contract substitution is not possible  

Failure results in execution being blocked.

---

### independence  
Enforces structural role separation and authority constraints.

If required roles are declared:

- identities must be present  
- roles must be satisfied  
- identities must not overlap  

Failure results in execution being blocked.

---

### integrity  
Performs non-mutating verification of:

- SHA256SUMS  
- binding.json (if required)  
- SEAL.json (if required)  

Failure results in execution being blocked.

---

### integrity-finalization  
Materializes deterministic integrity artifacts:

- payload archive  
- SHA256 manifest  
- binding artifact (>= 0.3.0)  
- SEAL (>= 0.3.0)  

This stage executes only if prior stages pass.

---

### publication  
Validates structural publication requirements.

Failure results in execution being blocked.

---

### publication-commit  
The sole execution authorization gate.

This stage determines:

```
commit_allowed = publication_commit_stage.passed
```


If this stage fails:

- execution MUST NOT occur  

No other stage may authorize execution.

---

## Normative Guarantees

- All stages are executed in deterministic order  
- No stage may be skipped  
- Failure in any stage propagates to `publication-commit`  
- Later stages MUST NOT override prior failures  
- `publication-commit` is the sole execution decision surface  

---

## Execution Semantics

CRI-CORE does not perform execution.

It determines whether execution is permitted.

`commit_allowed = true → execution may occur`
`commit_allowed = false → execution must not occur`


---

Stage identifiers are defined in:

`cricore/enforcement/stage_ids.py`

This stage order is part of the CRI-CORE enforcement contract surface.

---

<div align="center">
  <sub>© 2026 Waveframe Labs — Independent Open-Science Research Entity</sub>
</div>