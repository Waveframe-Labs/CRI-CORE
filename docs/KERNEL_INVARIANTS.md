---
title: "CRI-CORE Kernel Invariants"
filetype: "documentation"
type: "specification"
domain: "enforcement"
version: "0.12.0"
doi: "TBD-0.1.0"
status: "Active"
created: "2026-03-11"
updated: "2026-04-01"

author:
  name: "Shawn C. Wright"
  email: "swright@waveframelabs.org"
  orcid: "https://orcid.org/0009-0006-6043-9295"

maintainer:
  name: "Waveframe Labs"
  url: "https://waveframelabs.org"

license: "Apache-2.0"

ai_assisted: "partial"

dependencies:
  - "ENFORCEMENT_STAGE_ORDER.md"
  - "compiled_contract_interface.md"
  - "canonical_proposal_object.md"

anchors:
  - "CRI-CORE-KERNEL-INVARIANTS-v0.12.0"
---

# CRI-CORE Kernel Invariants

This document defines the structural guarantees provided by the CRI-CORE enforcement kernel at the execution boundary.

Kernel invariants describe properties that must hold whenever CRI-CORE produces a commit authorization decision.

These invariants define the conditions under which execution is permitted or denied.

---

## Invariant 1 — Deterministic Stage Order

The enforcement pipeline executes stages in a fixed, deterministic order.

The canonical stage sequence is defined in:

```

docs/ENFORCEMENT_STAGE_ORDER.md

```

Stages are emitted in this order regardless of failure outcomes.

No stage reordering is permitted.

---

## Invariant 2 — Single Commit Authority

A state mutation may only be authorized by the `publication-commit` stage.

The kernel exposes a single execution decision:

```

commit_allowed

```

This value is equal to the pass state of the `publication-commit` stage.

No other stage authorizes execution.

---

## Invariant 3 — Deterministic Contract Binding

A proposal must reference a compiled governance contract via:

```

contract.id
contract.version
contract.hash

```

During enforcement the kernel verifies:

```

proposal.contract.hash == compiled_contract.contract_hash

```

If this check fails:

- the run is rejected  
- execution is blocked  

This ensures that proposals are cryptographically bound to the governance contract used during enforcement.

---

## Invariant 4 — Structural Authority Independence

The independence stage enforces declared authority separation constraints.

If required roles are specified, the kernel rejects proposals where the same identity satisfies multiple incompatible roles.

Authority validation is structural only.

Violation results in execution being blocked.

---

## Invariant 5 — Artifact Integrity Enforcement

The integrity and integrity-finalization stages enforce:

- SHA256 manifest consistency  
- binding artifact consistency  
- SEAL verification (when required by contract version)  

Integrity checks are deterministic.

If integrity verification fails:

- the run is invalid  
- execution is blocked  

---

## Invariant 6 — Deterministic Result Emission

Every enforcement execution returns:

```

[List[StageResult], commit_allowed]

```

The result list includes a result for every canonical stage regardless of earlier failures.

This enables deterministic replay and traceability.

---

## Non-Invariants

CRI-CORE intentionally does not guarantee:

- domain semantic correctness  
- distributed consensus  
- external system enforcement  
- mutation prevention outside kernel invocation  

The kernel enforces structural admissibility of mutation attempts at the execution boundary only.

---

## Summary

CRI-CORE provides deterministic execution control through:

- canonical stage ordering  
- contract-bound enforcement  
- authority separation guarantees  
- cryptographic integrity enforcement  
- explicit commit authorization  

Execution is permitted only when all invariants hold.

---

<div align="center">
  <sub>© 2026 Waveframe Labs — Independent Open-Science Research Entity</sub>
</div>