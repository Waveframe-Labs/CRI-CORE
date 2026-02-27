---
title: "CRI-CORE Run Context Contract"
filetype: "specification"
type: "normative"
domain: "enforcement"
version: "0.2.0"
doi: "TBD-0.2.0"
status: "Active"
created: "2026-02-10"
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

dependencies:
  - "../CRI_CORE_ENFORCEMENT_CONTRACT.md"

anchors:
  - "CRI-CORE-RunContextContract-v0.2.0"
---

# CRI-CORE Run Context Contract

### Normative structural interface for enforcement inputs

------------------------------------------------------------------------

## 1. Purpose

This document defines the **run context contract** supplied to CRI-CORE
enforcement stages.

The run context is a structured input provided by an external
orchestration system.

Its sole purpose is to provide **structural identity and reference
material** required for deterministic enforcement.

This contract defines:

-   allowed top-level fields,
-   required structural guarantees,
-   and identity enforcement extensions aligned with CRI-CORE v0.5.x.

This document does not define semantic meaning, workflow logic,
governance authority, or epistemic interpretation.

------------------------------------------------------------------------

## 2. Authority and Scope

This contract derives authority from the CRI-CORE Enforcement Contract.

It governs inputs provided to:

-   independence stage
-   integrity stage
-   publication stage

It does not modify contract-version-based invariants declared inside
`contract.json`.

Contract-version enforcement remains authoritative and independent of
run context.

------------------------------------------------------------------------

## 3. Structural Nature of Run Context

The run context SHALL be a JSON-serializable mapping.

CRI-CORE SHALL:

-   treat all identifiers as opaque,
-   evaluate only structural presence and equality,
-   perform no semantic inference.

CRI-CORE SHALL NOT:

-   reinterpret identity meaning,
-   resolve external references,
-   weaken or override contract-version invariants.

------------------------------------------------------------------------

## 4. Top-Level Structure

``` json
{
  "identities": { ... },
  "integrity": { ... },
  "publication": { ... }
}
```

All sections are optional at the top level.

A section becomes required only if the corresponding enforcement stage
executes.

------------------------------------------------------------------------

## 5. Identity Context (Independence Stage)

### 5.1 Structure

``` json
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

------------------------------------------------------------------------

### 5.2 Structural Requirements

If the independence stage executes:

-   `identities` MUST be present.
-   `orchestrator` MUST be present.
-   `reviewer` MUST be present.

Each identity MUST contain:

-   `id` (string)
-   `type` (string)

Identity equality is determined solely by structural equality of
`(id, type)`.

------------------------------------------------------------------------

### 5.3 Required Roles Extension

If `identities.required_roles` is present:

-   It MUST be a list of role names.
-   Each listed role MUST be present as a valid identity mapping.
-   No identity may satisfy more than one listed required role.
-   Failure to satisfy declared required roles SHALL cause independence
    failure.

If `required_roles` is absent:

-   CRI-CORE enforces only minimal orchestrator/reviewer separation.

------------------------------------------------------------------------

### 5.4 Self-Approval Rule

If orchestrator and reviewer are structurally equal:

-   Enforcement SHALL fail unless `self_approval_override` is true.
-   Overrides SHALL be recorded as structural exceptions.

------------------------------------------------------------------------

## 6. Integrity Context

### 6.1 Structure

``` json
{
  "integrity": {
    "workflow_execution_ref": "string",
    "run_payload_ref": "string",
    "attestation_ref": "string"
  }
}
```

All fields are optional.

If provided, each MUST be a string.

CRI-CORE treats all values as opaque references.

This section does not weaken contract-version-dependent invariants such
as binding.json or SEAL.json requirements.

------------------------------------------------------------------------

## 7. Publication Context

### 7.1 Structure

``` json
{
  "publication": {
    "repository_ref": "string",
    "commit_ref": "string"
  }
}
```

All fields are optional.

If provided, each MUST be a string.

Values are treated as opaque references.

------------------------------------------------------------------------

## 8. Structural Constraints

CRI-CORE SHALL enforce:

-   structural presence of required identity mappings,
-   strict separation when required_roles is declared,
-   no identity serving multiple required roles,
-   no inference or semantic expansion of references,
-   no override of contract-version enforcement rules.

------------------------------------------------------------------------

## 9. Versioning

This contract is independently versioned.

CRI-CORE SHALL declare which run context contract version it expects.

Multiple versions MAY coexist.

Historical runs SHALL be interpreted under their declared contract
version.

------------------------------------------------------------------------

::: {align="center"}
`<sub>`{=html}© 2026 Waveframe Labs`</sub>`{=html}
:::
