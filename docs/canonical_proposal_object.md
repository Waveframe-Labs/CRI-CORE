---
title: "CRI-CORE Canonical Proposal Object"
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
  - "../schema/proposal.schema.json"

anchors:
  - "CRI-CORE-CANONICAL-PROPOSAL-OBJECT-v0.1.0"
---

# CRI-CORE Canonical Proposal Object

## Purpose

The Canonical Proposal Object defines the standard mutation request
envelope evaluated by the CRI-CORE enforcement pipeline.

Its role is to provide a stable and explicit input contract between an
external proposing system and the kernel. Rather than allowing
domain-specific runners or applications to pass loosely structured
inputs into CRI-CORE, the proposal object establishes a common structure
for describing:

-   who is proposing a mutation
-   which contract governs the mutation
-   what state change is being requested
-   which artifacts are bound to the request
-   what execution context is relevant for structural enforcement

This object is not a domain model. It is an enforcement-facing proposal
envelope.

------------------------------------------------------------------------

## Architectural Role

The Canonical Proposal Object sits at the boundary between external
workflow logic and deterministic kernel evaluation.

Conceptually:

external actor / agent / workflow ↓ canonical proposal object ↓ CRI-CORE
enforcement pipeline ↓ commit_allowed = true \| false

This boundary is important because it allows CRI-CORE to remain
domain-agnostic.

The kernel does not need to understand financial semantics, research
semantics, or business workflow semantics. It only needs a structurally
valid mutation proposal that declares the required enforcement inputs in
a consistent form.

------------------------------------------------------------------------

## Design Goals

The Canonical Proposal Object is intended to satisfy five goals.

Version 0.1.0 uses explicit field closure. Unless a field is declared in
the schema, it is not part of the canonical proposal object.

### 1. Stable Enforcement Input

The object provides a repeatable, versionable input structure for the
kernel. This allows runners, demos, and downstream systems to target a
defined proposal format rather than relying on ad hoc payload
construction.

### 2. Domain Agnosticism

The object describes requested mutation structure without embedding
domain-specific meaning into the kernel. A finance workflow, a governed
claim workflow, and a future agentic workflow should all be able to
express mutation requests through the same envelope.

### 3. Auditability

The object must support deterministic replay and post hoc inspection.
Proposal identifiers, timestamps, contract references, and artifact
bindings all contribute to a verifiable execution record.

### 4. Integrity Binding

The object must clearly identify which artifacts are part of the
evaluated proposal. This ensures that structural validation and later
integrity checks can refer to an explicit artifact set rather than an
implied one.

Artifacts are required and the artifact set must contain at least one
entry. Each artifact must be uniquely defined by its path and SHA-256
digest. Duplicate artifact entries are not permitted.

### 5. Contract-Driven Evolution

The proposal object should evolve through explicit schema versioning
rather than silent structural drift. Changes to the object shape must be
visible and reviewable.

------------------------------------------------------------------------

## Canonical Structure

The current v0.1 structure is defined by `schema/proposal.schema.json`.

At a conceptual level, the object contains the following top-level
sections:

-   `proposal_id`
-   `timestamp`
-   `actor`
-   `contract`
-   `requested_mutation`
-   `artifacts`
-   `run_context` (optional)

These sections are described below.

------------------------------------------------------------------------

## Field Definitions

## `proposal_id`

A unique identifier for the mutation request.

This field exists to support traceability, artifact correlation, replay,
and logging. It should identify a specific proposal instance rather than
a general workflow type.

Example intent:

prop-2026-03-05-001

------------------------------------------------------------------------

## `timestamp`

An RFC3339 UTC timestamp representing when the proposal was created.

The timestamp must be expressed in the following format:

YYYY-MM-DDTHH:MM:SSZ

Example:

2026-03-05T15:42:00Z

Time zone offsets and fractional seconds are not permitted in v0.1.0 in order to preserve deterministic replay and ordering guarantees across enforcement environments.

------------------------------------------------------------------------

## `actor`

The `actor` section identifies the entity initiating the proposal.

In v0.1, this section includes:

-   `id`
-   `type`
-   `declared_role` (optional)

The kernel uses this section to reason about structural identity, not
competence or authority quality.

Supported actor types currently include:

-   `ai_system`
-   `human`
-   `workflow`
-   `service`

The actor section should answer the question:

Who is proposing the mutation?

------------------------------------------------------------------------

## `contract`

The `contract` section identifies the governing contract under which the
proposal should be evaluated.

In v0.1, this section includes:

-   `id`
-   `version`

This field is essential because CRI-CORE already enforces
contract-version-sensitive behavior. Different contract versions may
imply different structural requirements, artifact requirements, or
enforcement invariants.

The contract section should answer the question:

Which declared governance contract governs this proposal?

------------------------------------------------------------------------

## `requested_mutation`

The `requested_mutation` section describes the state change being
requested.

In v0.1, this section includes:

-   `domain`
-   `resource`
-   `action`
-   `stage` (optional)

This field allows external systems to declare mutation intent in a
structured way without requiring the kernel to interpret domain meaning.
The presence of these fields does not imply that CRI-CORE defines
lifecycle semantics; it only standardizes how mutation intent is
presented for enforcement.

The requested mutation section should answer the question:

What change is being requested?

------------------------------------------------------------------------

## `artifacts`

The `artifacts` section lists the files bound to the proposal.

Each artifact entry includes:

-   `path`
-   `sha256`

Artifacts are required and the artifact set must contain at least one
entry. Each artifact must be uniquely defined by its path and SHA-256
digest.

The artifacts section should answer the question:

Which concrete artifacts are part of the evaluated proposal?

------------------------------------------------------------------------

## `run_context`

The `run_context` section is optional in v0.1.

Its purpose is to carry execution-context details relevant to structural
responsibility enforcement. In the current draft, this includes fields
such as:

-   `orchestrator`
-   `reviewers`

If reviewers are declared, the list must contain at least one identity
and each reviewer identifier must be unique.

The run context section should answer the question:

What execution context is relevant to evaluating this proposal
structurally?

Any run_context field admitted into the schema must be justified by a
deterministic enforcement need. Convenience data, observational
metadata, or domain workflow state should remain outside the canonical
proposal object unless required for kernel evaluation.

------------------------------------------------------------------------

## Example Shape

proposal_id: "prop-2026-03-05-001" timestamp: "2026-03-05T15:42:00Z"

actor: id: "ai-budget-agent" type: "ai_system" declared_role: "proposer"

contract: id: "finance-raci-policy" version: "0.3.0"

requested_mutation: domain: "finance" resource: "budget-allocation"
action: "reallocate" stage: "proposal"

artifacts: - path: "proposal.json" sha256:
"aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"

run_context: orchestrator: "finance-manager" reviewers: - "cfo" -
"compliance-officer"

------------------------------------------------------------------------

## Summary

The Canonical Proposal Object establishes a stable, domain-agnostic,
auditable input contract for CRI-CORE.

Its purpose is not to make the kernel smarter. Its purpose is to make
the mutation boundary more explicit, more portable, and more enforceable
across workflows.

This specification is the first formal step in making CRI-CORE's
mutation boundary explicit, versioned, and reusable across governed
workflows.
