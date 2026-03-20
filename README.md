---
title: "CRI-CORE — Deterministic Enforcement Kernel"
filetype: "documentation"
type: "repository-overview"
domain: "enforcement"
version: "0.10.0"
doi: "10.5281/zenodo.19080238"
status: "Active"
created: "2026-02-19"
updated: "2026-03-19"

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

dependencies: []

anchors:
  - "CRI-CORE v0.10.0"
  - "Deterministic Enforcement Kernel"
---

# CRI-CORE

**CRI-CORE v0.10.0 --- Deterministic Enforcement Kernel**

CRI-CORE is a deterministic structural enforcement engine for governed state transitions.

It evaluates a run directory against explicit structural, authority, integrity, binding, seal, and publication constraints.

The kernel does not interpret meaning.

It evaluates structure and invariants only.

---

## Installation

Install from PyPI:

    pip install cricore

Requires Python 3.10+.

---

## Minimal Usage

The supported public entrypoint is:

    from cricore.enforcement.execution import run_enforcement_pipeline

Example:

    from cricore.enforcement.execution import run_enforcement_pipeline

    results, commit_allowed = run_enforcement_pipeline(
        run_path=".",
        expected_contract_version="0.3.0"
    )

The function returns:

    (results: List[StageResult], commit_allowed: bool)

`commit_allowed` is the sole commit authorization signal.

---

## Runtime Input Contracts

CRI-CORE evaluates deterministic run artifacts and explicit mutation requests.

The kernel relies on two structured input contracts:

- Run artifact contract (run directory structure)
- Mutation proposal object (canonical proposal envelope)

Proposal objects are validated against the canonical proposal schema before enforcement.

Compiled governance contracts may be used by external systems to construct proposal objects.

Proposals reference the governing contract using:

contract.id  
contract.version  
contract.hash

During enforcement the kernel verifies that the proposal's contract hash matches the compiled contract artifact used by the run.

The kernel does not interpret governance policy structure directly.  
It verifies deterministic contract identity only.

---

## Core Model

    Exploration (high velocity, non-deterministic)
        →
    Deterministic structural gate (CRI-CORE)
        →
    Governed state mutation

The kernel ensures that only structurally valid and cryptographically
sealed runs are permitted to mutate governed state.

---

## Enforcement Pipeline (v0.10.0)

Canonical stage order:

1. run-structure
2. structure-contract-version-gate
3. structure-contract-hash-gate
4. independence
5. integrity
6. integrity-finalization
7. publication
8. publication-commit

The pipeline is deterministic and ordered.
The contract hash gate verifies that mutation proposals are bound to the exact compiled governance contract used during enforcement.

---

## Contract-Version Behavior

CRI-CORE enforces versioned structural guarantees:

For `contract_version < 0.3.0`:

- Structural validation  
- Independence enforcement  
- Integrity manifest verification  

For `contract_version ≥ 0.3.0`: 

- binding.json required  
- SEAL.json required  
- Strict cryptographic seal validation  
- Immutable artifact boundary enforcement  

Enforcement meaning is isolated per declared contract version.  
Historical runs are validated under their declared version.

---

## Independence Model

The kernel enforces structural role separation:

- Explicit actor identities
- Optional declared role requirements (`required_roles`)
- Strict prohibition on multi-role identity when roles are required
- Explicit override pathway (recorded, never implicit)

The kernel evaluates identity structure only.  
It does not evaluate competence or review quality.

---

## Cryptographic Guarantees

Finalized runs must include:

- Deterministic SHA256 manifest
- Payload archive
- Structural binding artifact
- Deterministic SEAL.json

The seal covers:

- All run files (deterministic ordering)
- Binding artifact
- Manifest hash
- Payload hash

Any mutation changes the seal hash.

The seal provides tamper evidence.  
It is not a signature.

---

## Atomic Commit Semantics

CRI-CORE does not mutate state.

It emits a deterministic authorization decision:

    commit_allowed = publication_commit_stage.passed

The caller decides whether to mutate.

The kernel centralizes the commit decision.  
It does not enforce it outside its invocation boundary.

---

## Runtime Packaging Guarantees

CRI-CORE is distributed as a self-contained runtime.

- Schema artifacts are embedded within the package (`cricore.schema`)
- No dependency on repository-relative paths
- Deterministic behavior across local, CI, and installed environments

All validation logic operates against packaged artifacts, not filesystem assumptions.

---

## What CRI-CORE Does Not Do

CRI-CORE does not:

- Interpret lifecycle semantics
- Judge correctness of domain objects
- Evaluate epistemic sufficiency
- Enforce governance policy meaning
- Perform distributed consensus
- Prevent bypass outside invocation

It is a deterministic structural gate only.

---

## Design Principles

- Deterministic evaluation
- No network calls
- No model calls
- No semantic inference
- Opaque reference handling
- Versioned enforcement meaning
- Strict immutability after finalization

---

## Intended Use

CRI-CORE is designed to sit beneath:

- Workflow engines
- CI pipelines
- Agent execution runtimes
- Domain governance systems

It provides:

- Structural admissibility validation
- Cryptographic immutability guarantees
- Centralized commit authorization

It is domain-agnostic.

---

<div align="center">
  <sub>© 2026 Waveframe Labs — Independent Open-Science Research Entity</sub>
</div>