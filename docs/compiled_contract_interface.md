---
title: "CRI-CORE Compiled Contract Interface"
filetype: "documentation"
type: "guidance"
domain: "enforcement"
version: "0.1.0"
doi: "TBD-0.1.0"
status: "Active"
created: "2026-03-09"
updated: "2026-03-09"

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
  - "../schema/contract.schema.json"

anchors:
  - "CRI-CORE-COMPILED-CONTRACT-INTERFACE-v0.1.0"
---

# CRI-CORE Compiled Contract Interface

## Purpose

The compiled contract interface defines the deterministic artifact format consumed by the CRI-CORE kernel during enforcement.

CRI-CORE does **not interpret governance policy directly**. Instead, external systems are responsible for compiling governance definitions into a structured contract artifact. The kernel then evaluates mutation proposals against that compiled artifact.

This separation ensures that:

- governance policy remains external to the kernel
- policy interpretation is deterministic
- enforcement behavior is reproducible
- contracts can be versioned and audited independently

---

## Architectural Role

The compiled contract artifact sits between external governance systems and the CRI-CORE enforcement runtime.

Conceptually:

```text
governance policy
      ↓
contract compiler
      ↓
compiled contract artifact
      ↓
CRI-CORE contract loader
      ↓
enforcement pipeline
````

CRI-CORE therefore consumes **compiled contracts**, not policy definitions.

---

## Design Principles

The compiled contract interface is designed around several constraints.

### Determinism

Contracts must produce identical enforcement behavior across environments. Contract artifacts must therefore contain all structural information required for enforcement.

### Kernel Independence

The kernel must not interpret policy logic dynamically. All policy meaning must already be resolved in the compiled contract artifact.

### Versioned Governance

Contracts must carry explicit identifiers and versions so historical runs can be replayed under the correct governance rules.

### Minimal Surface Area

The compiled contract artifact should contain only the fields required for structural enforcement. It should not contain arbitrary workflow state.

---

## Contract Artifact Role in Enforcement

Within CRI-CORE the contract artifact participates primarily in the **contract version gate** stage.

The contract artifact provides the enforcement pipeline with the structural rules necessary to determine whether a proposed mutation is admissible.

The artifact may influence stages such as:

* authority independence checks
* artifact integrity expectations
* stage transition requirements
* publication conditions

However, the kernel itself does not infer these rules. It simply executes enforcement logic based on the compiled artifact.

---

## Canonical Contract Structure

The compiled contract artifact is expected to contain the following top-level sections.

```text
contract_id
contract_version
authority_requirements
artifact_requirements
stage_requirements
invariants
```

These sections allow the enforcement pipeline to evaluate a mutation proposal deterministically.

---

## Field Definitions

### `contract_id`

A unique identifier for the governance contract.

This identifier distinguishes contracts that may define different enforcement behavior across domains or workflows.

Example intent:

```
finance-raci-policy
```

---

### `contract_version`

A semantic version identifier for the compiled contract artifact.

The kernel uses this value to ensure that mutation proposals reference a compatible contract version.

Example intent:

```
0.3.0
```

---

### `authority_requirements`

Defines structural authority expectations for mutation approval.

This section allows the enforcement pipeline to verify independence conditions such as:

* proposer identity
* reviewer identity
* required authority roles
* separation-of-duties conditions

The kernel evaluates these constraints structurally rather than semantically.

---

### `artifact_requirements`

Defines the artifact structure required for mutation proposals governed by this contract.

This section may include:

* required artifact presence
* artifact binding expectations
* integrity verification rules

These constraints ensure that mutation proposals provide the artifacts necessary for deterministic replay and validation.

---

### `stage_requirements`

Defines stage-level constraints relevant to the enforcement pipeline.

These constraints may specify conditions such as:

* allowed stage transitions
* stage-level artifact requirements
* stage-specific authority checks

The kernel does not interpret workflow semantics. It only validates structural compliance with the compiled contract artifact.

---

### `invariants`

Defines structural invariants that must hold for a proposal governed by this contract.

Invariants may represent conditions such as:

* immutable artifact bindings
* identity independence rules
* deterministic publication expectations

The kernel evaluates these invariants as part of the enforcement pipeline.

---

## Example Contract Artifact (Conceptual)

The following simplified example illustrates the conceptual shape of a compiled contract artifact.

```yaml
contract_id: finance-raci-policy
contract_version: 0.3.0

authority_requirements:
  proposer_role: proposer
  reviewer_roles:
    - responsible
    - accountable

artifact_requirements:
  required_artifacts:
    - proposal
    - approval

stage_requirements:
  allowed_transitions:
    - from: proposed
      to: approved

invariants:
  separation_of_duties: true
```

This example illustrates structure only. Actual contract artifacts may contain additional compiled information necessary for enforcement.

---

## Relationship to the Canonical Proposal Object

The compiled contract artifact complements the canonical proposal object.

```text
proposal object
      ↓
contract artifact
      ↓
enforcement pipeline
```

The proposal describes **what mutation is being requested**.

The contract artifact describes **how that mutation must be evaluated**.

Together these artifacts provide the enforcement runtime with the information necessary to make a deterministic commit decision.

---

## Kernel Responsibility

CRI-CORE is responsible for:

* loading compiled contract artifacts
* validating contract structure
* exposing contract data to enforcement stages
* ensuring contract versions match proposal expectations

CRI-CORE is **not responsible for compiling governance policy**.

That responsibility belongs to external systems.

---

## Scope of v0.1

Version 0.1.0 defines the minimal interface necessary for deterministic contract consumption by the kernel.

Future versions may expand:

* authority modeling
* artifact binding rules
* enforcement stage configuration
* escalation pathways

Any expansion must occur through explicit versioned evolution to preserve reproducibility.

---

## Summary

The compiled contract interface defines the deterministic artifact boundary between governance policy systems and the CRI-CORE enforcement runtime.

By separating policy compilation from kernel enforcement, CRI-CORE maintains a small, auditable, domain-agnostic runtime capable of evaluating governed mutation proposals across diverse workflows.
