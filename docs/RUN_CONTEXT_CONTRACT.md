---
title: "CRI-CORE Run Context Contract"
filetype: "specification"
type: "normative"
domain: "enforcement"
version: "0.1.0"
doi: "TBD-0.1.0"
status: "Active"
created: "2026-02-10"
updated: "2026-02-10"

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
ai_assistance_details: "AI-assisted drafting of a minimal structural ABI for the CRI-CORE run_context interface derived directly from the CRI-CORE Enforcement & Run Artifact Contract, under human authorship and final approval."

dependencies:
  - "../CRI_CORE_ENFORCEMENT_CONTRACT.md"

anchors:
  - "CRI-CORE-RunContextContract-v0.1.0"
---

# CRI-CORE Run Context Contract
### Normative interface for enforcement-stage inputs

---

## 1. Purpose

This document defines the **run context contract** passed into CRI-CORE enforcement stages.

The run context is an explicit, structured input surface supplied by the orchestration layer
(e.g. AWO execution or an equivalent system).

Its sole purpose is to provide **structural identity and provenance references**
required for mechanical enforcement.

This document defines:

- what fields may be supplied to CRI-CORE, and
- what structural guarantees those fields must satisfy.

This document does not define:

- epistemic meaning,
- workflow semantics,
- disclosure semantics,
- governance authority,
- or validation intent.

---

## 2. Authority and scope

This contract derives its authority exclusively from:

- the CRI-CORE Enforcement & Run Artifact Contract

This contract applies only to:

- inputs provided to the following CRI-CORE enforcement stages:

- independence stage
- integrity & provenance stage
- publication stage

---

## 3. Structural nature of the run context

The run context is a structured data object provided to CRI-CORE at enforcement time.

CRI-CORE SHALL:

- treat all run context fields as opaque identifiers and references, and
- evaluate only structural presence and equality relationships.

CRI-CORE SHALL NOT:

- infer semantics,
- reinterpret identifiers,
- resolve identity meaning,
- or derive additional context.

---

## 4. Top-level run context object

The run context object SHALL be a JSON-serializable mapping with the following top-level fields:

```json
{
  "identities": { ... },
  "integrity": { ... },
  "publication": { ... }
}
```

All top-level sections are OPTIONAL.

A section is required only when the corresponding enforcement stage is executed.

---

## 5. Identity context (independence stage)

### 5.1 Purpose

The identity context provides the structural identity material required for
independence and non-circular validation enforcement.

### 5.2 Structure

```json
{
  "identities": {
    "orchestrator": {
      "id": "string",
      "type": "string"
    },
    "reviewer": {
      "id": "string",
      "type": "string"
    },
    "self_approval_override": false
  }
}
```

---

### 5.3 Field definitions

#### identities.orchestrator

- REQUIRED for independence enforcement.
- Structure:

```
id   : string
type : string
```

The `id` field MUST be a stable identifier string.

The `type` field MUST declare the structural identity category
(for example: `human`, `service`, `workflow`, `organization`).

CRI-CORE SHALL treat the `(id, type)` pair as an opaque identifier.

---

#### identities.reviewer

Same structure and requirements as `identities.orchestrator`.

---

#### identities.self_approval_override

- OPTIONAL.
- Boolean.
- Defaults to false if omitted.

This field declares an explicit override of the self-approval prohibition.

CRI-CORE SHALL only evaluate the presence and boolean value of this field.

---

## 6. Integrity and provenance context

### 6.1 Purpose

The integrity context provides references required for integrity and provenance
enforcement.

This contract does not define artifact formats, hashing mechanisms, or signature
schemes.

---

### 6.2 Structure

```json
{
  "integrity": {
    "workflow_execution_ref": "string",
    "run_payload_ref": "string",
    "attestation_ref": "string"
  }
}
```

---

### 6.3 Field definitions

#### integrity.workflow_execution_ref

- OPTIONAL.
- String.

A stable reference to the workflow execution instance that produced the run.

CRI-CORE SHALL treat this value as an opaque reference.

---

#### integrity.run_payload_ref

- OPTIONAL.
- String.

A stable reference to the finalized run payload archive.

CRI-CORE SHALL treat this value as an opaque reference.

---

#### integrity.attestation_ref

- OPTIONAL.
- String.

A stable reference to the attestation material associated with the run.

CRI-CORE SHALL treat this value as an opaque reference.

---

## 7. Publication context

### 7.1 Purpose

The publication context provides references required for publication and commit
binding enforcement.

This contract does not define repository semantics or publication policy.

---

### 7.2 Structure

```json
{
  "publication": {
    "repository_ref": "string",
    "commit_ref": "string"
  }
}
```

---

### 7.3 Field definitions

#### publication.repository_ref

- OPTIONAL.
- String.

A stable reference to the governing repository.

CRI-CORE SHALL treat this value as an opaque reference.

---

#### publication.commit_ref

- OPTIONAL.
- String.

A stable reference to the commit that published the run artifact and its
associated governance material.

CRI-CORE SHALL treat this value as an opaque reference.

---

## 8. Structural constraints

CRI-CORE SHALL apply the following structural constraints only:

- identity equality is evaluated solely by structural equality of `(id, type)`
- missing required sections SHALL cause the corresponding enforcement stage to fail
- no inference, normalization, or resolution of references is permitted

---

## 9. Explicit non-goals

This contract SHALL NOT define:

- what constitutes a valid reviewer,
- what constitutes a valid workflow,
- what constitutes sufficient provenance,
- what constitutes a valid publication,
- or what constitutes adequate independence.

All such semantics belong to upstream layers.

---

## 10. Versioning

This run context contract is versioned independently.

CRI-CORE enforcement logic SHALL declare which version of this contract it expects.

Backward compatibility and coexistence follow the CRI-CORE enforcement contract
versioning rules.

---

<div align="center">
  <sub>© 2026 Waveframe Labs — Independent Open-Science Research Entity</sub>
</div>  
