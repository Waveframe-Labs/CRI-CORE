---
title: "CRI-CORE Run Context Contract"
filetype: "specification"
type: "normative"
domain: "enforcement"
version: "0.12.0"
doi: "TBD-0.2.0"
status: "Active"
created: "2026-02-10"
updated: "2026-04-01"

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
  - "../CRI_CORE_ENFORCEMENT_CONTRACT.md"

anchors:
  - "CRI-CORE-RunContextContract-v0.12.0"
---

# CRI-CORE Run Context Contract

## 1. Purpose

This document defines the **run context contract** supplied to CRI-CORE at the execution boundary.

The run context provides structured input used by the kernel to determine whether a proposed mutation is allowed to execute.

It supplies:

- identity structure  
- integrity references  
- publication references  

The run context contributes to the `commit_allowed` decision.

It does not define or interpret domain semantics.

---

## 2. Authority and Scope

This contract derives authority from the CRI-CORE Enforcement Contract.

It governs inputs consumed by:

- independence stage  
- integrity stage  
- publication stage  

It does not override:

- contract-version invariants  
- binding rules  
- seal requirements  

Contract enforcement remains authoritative.

---

## 3. Structural Nature

The run context SHALL be a JSON-serializable mapping.

CRI-CORE SHALL:

- treat all identifiers as opaque  
- evaluate only structural presence and equality  
- perform no semantic interpretation  

CRI-CORE SHALL NOT:

- resolve external systems  
- infer meaning  
- reinterpret identity intent  

The run context is a structural input to the execution decision only.

---

## 4. Top-Level Structure

```json
{
  "identities": { ... },
  "integrity": { ... },
  "publication": { ... }
}
````

All sections are optional.

A section becomes required only if the corresponding enforcement stage executes.

---

## 5. Identity Context (Independence Stage)

### Structure

```json
{
  "identities": {
    "required_roles": ["orchestrator", "reviewer"],
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

### Requirements

If the independence stage executes:

* `identities` MUST be present
* required roles MUST be satisfied
* identities MUST be structurally distinct where required

Identity equality is determined by `(id, type)`.

---

### Enforcement Implication

Violations result in:

* independence stage failure
* execution being blocked (`commit_allowed = false`)

---

## 6. Integrity Context

### Structure

```json
{
  "integrity": {
    "workflow_execution_ref": "string",
    "run_payload_ref": "string",
    "attestation_ref": "string"
  }
}
```

All fields are optional.

Values are treated as opaque references.

---

### Enforcement Implication

If integrity constraints fail:

* integrity stage fails
* execution is blocked

---

## 7. Publication Context

### Structure

```json
{
  "publication": {
    "repository_ref": "string",
    "commit_ref": "string"
  }
}
```

All fields are optional.

Values are treated as opaque references.

---

### Enforcement Implication

If publication requirements fail:

* publication stage fails
* execution is blocked

---

## 8. Structural Constraints

CRI-CORE enforces:

* structural presence of required fields
* identity separation when required
* strict equality-based identity comparison
* no semantic interpretation
* no override of contract invariants

---

## 9. Execution Semantics

The run context contributes to the execution decision:

```
commit_allowed = false  → execution blocked  
commit_allowed = true   → execution permitted  
```

The run context does not independently authorize execution.

It provides structured input evaluated by the enforcement pipeline.

---

## 10. Versioning

This contract is independently versioned.

CRI-CORE SHALL declare compatible versions.

Multiple versions MAY coexist.

Historical runs SHALL be interpreted under their declared version.

---

<div align="center">
  <sub>© 2026 Waveframe Labs</sub>
</div>