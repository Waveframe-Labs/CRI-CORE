---
title: "CRI-CORE Compiled Contract Interface"
filetype: "documentation"
type: "guidance"
domain: "enforcement"
version: "0.1.1"
doi: "TBD-0.1.1"
status: "Active"
created: "2026-03-10"
updated: "2026-03-10"

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
  - "CRI-CORE-COMPILED-CONTRACT-INTERFACE-v0.1.1"
---

# CRI-CORE Compiled Contract Interface

## Purpose

The compiled contract interface defines a **deterministic artifact format used by governance systems external to CRI-CORE**.

CRI-CORE does **not interpret governance policy directly**. Instead, external systems may compile governance definitions into structured contract artifacts. These artifacts may then be used by external tooling or future integration layers to construct mutation proposals and enforcement inputs.

This separation ensures that:

- governance policy remains external to the kernel
- policy interpretation is deterministic
- contracts can be versioned and audited independently
- the kernel remains small and domain-agnostic

---

## Architectural Role

Compiled contracts belong to the **external governance layer**, not the CRI-CORE runtime itself.

Conceptually:

```

governance policy
↓
contract compiler
↓
compiled contract artifact
↓
external workflow / adapter
↓
proposal object
↓
CRI-CORE enforcement runtime

```

CRI-CORE therefore consumes **mutation proposals**, not policy definitions.

Compiled contracts may influence how proposals are constructed, but the kernel does not directly interpret governance policy artifacts.

---

## Design Principles

The compiled contract interface is designed around several constraints.

### Determinism

Contracts must produce identical governance behavior across environments. Contract artifacts must therefore contain all structural information required for governance interpretation.

### Kernel Independence

CRI-CORE must remain independent from governance policy logic. The kernel enforces structural invariants only.

### Versioned Governance

Contracts must carry explicit identifiers and versions so historical runs can be replayed under the correct governance rules.

### Minimal Kernel Surface

The kernel should not load or interpret arbitrary governance configuration artifacts. Governance compilation occurs outside the runtime boundary.

---

## Relationship to CRI-CORE Enforcement

Within CRI-CORE, the **only contract artifact consumed directly** is the run declaration file:

```

contract.json

```

This artifact provides:

- `contract_version`
- run-level metadata

The kernel uses this information primarily for:

- **contract version gating**
- integrity and sealing rules tied to version thresholds

All other governance interpretation occurs outside the kernel.

---

## Canonical Contract Structure (External)

Compiled contracts may contain sections such as:

```

contract_id
contract_version
authority_requirements
artifact_requirements
stage_requirements
invariants

```

These sections define governance constraints used by external systems that generate mutation proposals.

The CRI-CORE runtime does not directly interpret these fields in v0.x.

---

## Field Definitions

### `contract_id`

A unique identifier for the governance contract.

Example intent:

```

finance-raci-policy

```

---

### `contract_version`

A semantic version identifier for the compiled contract artifact.

This version may influence structural enforcement rules applied by the kernel.

Example:

```

0.3.0

````

---

### `authority_requirements`

Defines structural authority expectations such as:

- proposer identity
- reviewer identities
- role separation expectations

These constraints are typically enforced by external workflow systems that construct mutation proposals.

---

### `artifact_requirements`

Defines artifact expectations for proposals governed by this contract.

Examples may include:

- required proposal artifacts
- approval artifacts
- integrity bindings

These rules are resolved before proposals reach the CRI-CORE runtime.

---

### `stage_requirements`

Defines stage-level governance constraints used by external systems.

Examples may include:

- allowed transitions
- workflow state expectations
- stage-specific review requirements

These constraints are not interpreted directly by CRI-CORE.

---

### `invariants`

Defines structural invariants required by governance policy.

Examples may include:

- separation of duties
- artifact immutability expectations
- publication requirements

External systems may enforce these constraints before invoking CRI-CORE.

---

## Example Contract Artifact (Conceptual)

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
````

This example illustrates conceptual governance structure.
CRI-CORE does not directly interpret these fields.

---

## Relationship to the Canonical Proposal Object

The proposal object defines the **mutation request envelope** evaluated by CRI-CORE.

Compiled contracts influence how proposals are constructed but are not themselves the enforcement input.

```
governance contract
      ↓
proposal construction
      ↓
proposal object
      ↓
CRI-CORE enforcement runtime
```

---

## Kernel Responsibility

CRI-CORE is responsible for:

* validating proposal structure
* enforcing structural independence
* verifying cryptographic integrity
* validating publication constraints
* producing a deterministic commit decision

CRI-CORE is **not responsible for interpreting governance policy artifacts**.

---

## Scope of v0.1

Version 0.1.1 defines a conceptual interface for governance contract artifacts used by external systems.

Future integration layers may expand the relationship between compiled contracts and the CRI-CORE runtime.

Such expansions must occur through explicit versioned evolution to preserve reproducibility.

---

## Summary

The compiled contract interface defines a governance artifact boundary external to the CRI-CORE runtime.

By keeping governance compilation outside the kernel, CRI-CORE remains a small, deterministic, domain-agnostic enforcement engine focused solely on structural admissibility and commit authorization.