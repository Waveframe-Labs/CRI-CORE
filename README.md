---
title: "CRI-CORE — Deterministic Enforcement Kernel"
filetype: "documentation"
type: "repository-overview"
domain: "enforcement"
version: "0.5.0"
doi: "TBD"
status: "Active"
created: "2026-02-19"
updated: "2026-02-27"

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
  - "CRI-CORE v0.5.0"
  - "Deterministic Enforcement Kernel"
---

# CRI-CORE

**CRI-CORE v0.5.0 --- Deterministic Enforcement Kernel**

CRI-CORE is a deterministic enforcement engine for structural run
admissibility and atomic commit gating.

It evaluates a run directory against explicit structural, authority,
integrity, binding, sealing, and publication constraints and returns a
single authoritative mutation decision.

The kernel does not interpret meaning.\
It evaluates structure and invariants only.

------------------------------------------------------------------------

## Core Model

    Exploration (high velocity, non-deterministic)
        →
    Deterministic structural gate (CRI-CORE)
        →
    Governed state mutation

The kernel ensures that only structurally valid and cryptographically
sealed runs are permitted to mutate governed state.

------------------------------------------------------------------------

## Enforcement Pipeline (v0.5.0)

The canonical stage order:

1.  run-structure\
2.  structure-contract-version-gate\
3.  independence\
4.  integrity (verification)\
5.  integrity-finalization\
6.  publication\
7.  publication-commit

The pipeline returns:

    (results: List[StageResult], commit_allowed: bool)

`commit_allowed` is the sole commit authorization signal.

------------------------------------------------------------------------

## Contract-Version Behavior

CRI-CORE enforces versioned structural guarantees:

-   For `contract_version < 0.3.0`
    -   structural + independence + integrity manifest enforcement
-   For `contract_version ≥ 0.3.0`
    -   binding.json required\
    -   SEAL.json required\
    -   strict cryptographic seal validation\
    -   immutable artifact boundary enforcement

Enforcement meaning is isolated per declared contract version.\
Historical runs are validated under their declared version.

------------------------------------------------------------------------

## Independence Model

The kernel enforces structural role separation:

-   Explicit orchestrator identity
-   Explicit reviewer identity
-   Optional declared role requirements (`required_roles`)
-   Strict prohibition on multi-role identity when roles are required
-   Explicit override pathway (recorded, never implicit)

The kernel evaluates identity structure only.\
It does not evaluate competence or review quality.

------------------------------------------------------------------------

## Cryptographic Guarantees (v0.5.0)

Finalized runs must include:

-   Deterministic SHA256 manifest
-   Payload archive
-   Structural binding artifact
-   Deterministic SEAL.json

The seal covers:

-   All run files (deterministic ordering)
-   Binding artifact
-   Transition / rejection logs (when present)
-   Manifest hash
-   Payload hash

Any mutation changes the seal hash.

The seal is tamper-evidence.\
It is not a signature.

------------------------------------------------------------------------

## Atomic Commit Semantics

CRI-CORE does not mutate state.

It emits a deterministic authorization decision:

    commit_allowed = publication_commit_stage.passed

The caller decides whether to mutate.

The kernel centralizes the commit decision.\
It does not enforce it outside its invocation boundary.

------------------------------------------------------------------------

## What CRI-CORE Does Not Do

CRI-CORE does not:

-   Interpret lifecycle semantics
-   Judge correctness of claims
-   Evaluate epistemic sufficiency
-   Enforce governance policy
-   Define disclosure meaning
-   Perform distributed consensus
-   Prevent bypass outside invocation

It is a deterministic structural gate only.

------------------------------------------------------------------------

## Design Principles

-   Deterministic evaluation
-   No network calls
-   No model calls
-   No semantic inference
-   Opaque reference handling
-   Versioned enforcement meaning
-   Strict immutability after finalization

------------------------------------------------------------------------

## Intended Use

CRI-CORE is designed to sit beneath:

-   Workflow engines
-   CI pipelines
-   Agent execution runtimes
-   Domain governance systems

It provides:

-   Structural admissibility validation
-   Cryptographic immutability guarantees
-   Centralized commit authorization

It is domain-agnostic.

------------------------------------------------------------------------

## Status

v0.5.0 represents hardened structural enforcement with:

-   Binding enforcement
-   Seal enforcement
-   Strict role separation
-   Version-isolated invariants

The interface is considered stable within the 0.x series but may evolve
before 1.0.
