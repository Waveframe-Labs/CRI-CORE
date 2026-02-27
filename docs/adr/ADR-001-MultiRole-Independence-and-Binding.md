---
title: "ADR-001: Multi-Role Independence Model and Run Artifact Binding"
filetype: "adr"
type: "normative"
domain: "enforcement"
version: "0.1.0"
doi: "TBD-0.1.0"
status: "Active"
created: "2026-02-26"
updated: "2026-02-26"

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
ai_assistance_details: "AI-assisted drafting of architectural decision record capturing the transition from single-reviewer independence enforcement to a generalized multi-role structural model, and the introduction of contract-claim-log hash binding within the run artifact."

dependencies:
  - "../RUN_CONTEXT_CONTRACT.md"
  - "../../src/cricore/enforcement/independence.py"
  - "../../src/cricore/run/structure.py"
  - "../../src/cricore/enforcement/integrity.py"

anchors:
  - "CRICORE-MultiRoleBinding-v0.1.0"
---

# ADR-001: Multi-Role Independence Model and Run Artifact Binding

## 1. Context

During domain mapping for a SOX-aligned financial use case, a structural limitation was identified in the current independence enforcement stage.

As implemented in v0.4.1:

- Independence enforcement supports only:
  - `orchestrator`
  - `reviewer`
  - Optional `self_approval_override`
- Enforcement checks only structural equality of `(id, type)` between orchestrator and reviewer.
- No support exists for:
  - Multiple required approval roles
  - Distinct identity enforcement across multiple actors
  - Conflict-of-interest flags
  - Threshold-driven approval surfaces
  - Binding of claim and contract artifacts into a unified integrity chain

This limitation prevents CRI-CORE from structurally enforcing multi-actor separation-of-duties scenarios while remaining domain-agnostic.

The limitation was discovered during finance-domain mapping and is not domain-specific. It represents a general enforcement capability gap.

---

## 2. Decision Summary

CRI-CORE SHALL evolve from a two-identity independence model to a generalized **multi-role structural independence model**.

CRI-CORE SHALL also introduce **contract + claim + log hash binding** as part of the run artifact integrity surface.

These changes are structural and domain-agnostic.

This ADR authorizes a breaking change to the run context interface (pre-1.0).

---

## 3. Multi-Role Identity Model

### 3.1 Replace Orchestrator/Reviewer Model

The existing identity model:

```json
{
  "identities": {
    "orchestrator": {...},
    "reviewer": {...},
    "self_approval_override": false
  }
}
````

SHALL be replaced with:

```json
{
  "identities": {
    "actors": [
      {
        "id": "string",
        "type": "string",
        "role": "string"
      }
    ],
    "required_roles": ["string"],
    "conflict_flags": {
      "actor_id": false
    }
  }
}
```

### 3.2 Enforcement Rules (Structural Only)

The independence stage SHALL:

* Verify presence of all `required_roles`.
* Ensure each required role is satisfied by exactly one actor.
* Ensure all required-role actors are distinct by `(id, type)`.
* Ensure no actor fulfills mutually exclusive roles (structural rule only).
* Fail if any required-role actor has a `conflict_flags[actor_id] == true`.
* Treat all identifiers as opaque.
* Perform no semantic interpretation of roles.

### 3.3 Non-Goals

CRI-CORE SHALL NOT:

* Interpret financial semantics.
* Interpret workflow semantics.
* Infer organizational meaning.
* Validate sufficiency of roles.
* Define what constitutes “adequate governance.”

All role meaning remains upstream.

---

## 4. Contract + Claim + Log Hash Binding

### 4.1 Problem

Current integrity enforcement validates:

* Structural presence
* Manifest integrity
* Optional finalization

However, it does not:

* Bind the claim artifact hash to the contract hash.
* Bind both to the final run log hash.
* Produce a single structural binding object tying all enforcement inputs together.

This weakens replay guarantees.

---

### 4.2 Decision

CRI-CORE SHALL introduce a binding artifact within the run directory:

Example:

```json
{
  "contract_hash": "sha256",
  "claim_hash": "sha256",
  "log_hash": "sha256",
  "binding_hash": "sha256(contract_hash + claim_hash + log_hash)"
}
```

The integrity stage SHALL:

* Verify presence of binding artifact.
* Verify each referenced artifact hash.
* Verify deterministic recomputation of `binding_hash`.

All hash values SHALL be treated as opaque strings.

No semantic interpretation of claim or contract content is permitted.

---

## 5. Backward Compatibility

This change introduces a breaking modification to the run context contract.

Given CRI-CORE is pre-1.0 (v0.4.1), backward compatibility is not required.

Run context contract SHALL increment version upon implementation.

---

## 6. Architectural Rationale

This evolution:

* Preserves domain agnosticism.
* Strengthens structural enforcement.
* Enables multi-actor separation-of-duties enforcement.
* Enables regulated-domain demonstrations without domain logic in kernel.
* Strengthens audit defensibility via binding chain.

This change increases enforcement generality without introducing semantic coupling.

---

## 7. Status

Draft — pending implementation of:

* Multi-role independence stage
* Binding artifact generation
* Binding verification in integrity stage
* Updated run context contract version

```

---

<div align="center">
  <sub>© 2025 Waveframe Labs — Independent Open-Science Research Entity • Governed under the Aurora Research Initiative (ARI)</sub>
</div>