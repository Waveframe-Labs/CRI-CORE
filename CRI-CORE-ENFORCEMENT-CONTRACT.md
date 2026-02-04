---
title: "CRI-CORE Enforcement & Run Artifact Contract"
short_title: "CRI-CORE Contract"
filetype: "documentation"
type: "specification"
domain: "methodology"
layer: "enforcement-contract"
version: "0.1.0"
status: "Draft"
created: "2026-02-02"
updated: "2026-02-02"

author:
  name: "Shawn C. Wright"
  orcid: "https://orcid.org/0009-0006-6043-9295"
  email: "swright@waveframelabs.org"

maintainer:
  name: "Waveframe Labs"
  url: "https://waveframelabs.org"

license: "Apache-2.0"

ai_assisted: "partial"
ai_assistance_details: "AI-assisted structural scaffolding and boundary alignment under direct human authorship and final approval."

dependencies:
  - "Aurora Research Initiative (ARI)"
  - "Neurotransparency Doctrine (NTD)"
  - "Neurotransparency Specification (NTS)"
  - "Aurora Workflow Orchestration (AWO)"

anchors:
  - "CRI-CORE-CONTRACT-v0.1.0"
---

# CRI-CORE Enforcement & Run Artifact Contract
### Scaffold document – scope and boundary definition only

## 0. Purpose and Authority

### 0.1 Purpose

This document defines the **enforcement contract and run-artifact contract surface** for **CRI-CORE**.

Its purpose is to:

- specify **what CRI-CORE is allowed to validate and enforce**, and
- define the **required structure and invariants** of CRI-CORE–governed run artifacts.

This document exists to make CRI-CORE:

- deterministic,
- scope-bounded,
- and mechanically auditable.

It establishes the **structural and enforcement contract only**.  
It does not define epistemic rules, disclosure semantics, governance authority, or workflow design.

---

### 0.2 What this document governs

This document governs:

- the **run artifact contract** produced and finalized by CRI-CORE,
- the **structural and invariant checks** CRI-CORE must perform,
- the **independence and attestation enforcement surfaces** implemented by CRI-CORE,
- and the **mechanical guarantees** CRI-CORE provides for integrity and reconstruction support.

All enforcement described in this document is **structural and procedural**, not epistemic.

---

### 0.3 What this document does not govern

This document does not define, modify, or reinterpret:

- epistemic legitimacy criteria,
- disclosure obligations,
- workflow phases or sequencing,
- governance authority or ratification rules,
- review standards,
- or scientific or technical correctness.

Those responsibilities belong to other layers of the Aurora stack.

---

### 0.4 Authority and hierarchy

This document derives its authority exclusively from its position within the Aurora governance stack.

The authoritative hierarchy is:

- **Aurora Research Initiative (ARI)** — institutional authority and governance
- **Neurotransparency Doctrine (NTD)** — epistemic rationale
- **Neurotransparency Specification (NTS)** — normative disclosure requirements
- **Aurora Workflow Orchestration (AWO)** — methodological orchestration
- **CRI-CORE** — deterministic enforcement and validation

This document operates strictly at the **CRI-CORE layer**.

It SHALL NOT introduce requirements that belong to:

- NTD (epistemic justification),
- NTS (disclosure semantics),
- AWO (workflow design),
- or ARI (governance authority).

---

### 0.5 Normative sources

The normative meaning of this document is constrained by, and must remain compatible with:

- the Aurora Research Initiative (ARI) governance framework,
- the Neurotransparency Specification (NTS), in particular:
  - disclosure scope,
  - independence and validation constraints,
  - provenance and integrity requirements,
- the Aurora Workflow Orchestration (AWO) methodology,
- and the CRI-CORE prototype execution and gating workflow.

Where ambiguity exists, ARI governance and NTS normative language are authoritative.

---

### 0.6 Enforcement scope statement

CRI-CORE is defined as a **mechanical enforcement layer**.

Under this contract, CRI-CORE is authorized to:

- verify artifact presence,
- verify structural conformity,
- verify declared invariants,
- verify independence and attestation constraints,
- verify integrity and continuity artifacts,
- and block progression or publication when enforcement conditions fail.

CRI-CORE is explicitly **not authorized** to:

- interpret epistemic meaning,
- evaluate adequacy of disclosure,
- judge correctness or rigor,
- or substitute for human review, governance, or scientific validation.

---

### 0.7 Normative intent

The intent of this contract is to make enforcement:

- deterministic,
- inspectable,
- replayable,
- and non-interpretive.

CRI-CORE exists to enforce **what must exist and what must not be violated**, not to decide **what is true, valid, sufficient, or legitimate**.

## 1. Layer positioning and non-overlap

### 1.1 Intent

CRI-CORE is positioned exclusively as a **deterministic enforcement and validation layer**.

Its role is to:

- execute mechanically checkable constraints,
- validate the presence and structure of governed artifacts,
- validate declared invariants and independence conditions,
- and produce verifiable enforcement outcomes.

CRI-CORE exists to answer one question only:

> **Whether declared structural and procedural requirements are satisfied.**

It does not participate in epistemic judgment, methodological design, or institutional governance.

---

### 1.2 Explicit non-responsibilities

CRI-CORE SHALL NOT perform, implement, or imply any of the following functions:

- epistemic interpretation of claims, reasoning, or conclusions,
- interpretation or definition of disclosure semantics,
- interpretation of epistemic legitimacy,
- workflow design, orchestration logic, or phase semantics,
- governance, ratification, or institutional authority decisions.

In particular:

- CRI-CORE SHALL NOT interpret or expand the meaning of any requirement defined in the Neurotransparency Specification (NTS).
- CRI-CORE SHALL NOT define when disclosures must occur.
- CRI-CORE SHALL NOT define how workflows are structured or sequenced.
- CRI-CORE SHALL NOT define adoption, authority, or compliance consequences.

CRI-CORE may only enforce requirements that are already defined by authoritative upstream layers.

---

### 1.3 Layer responsibility boundary

The Aurora stack assigns distinct, non-overlapping responsibilities to each layer:

- **ARI** defines authority, ratification, and governance.
- **NTD** defines epistemic rationale.
- **NTS** defines normative disclosure and legitimacy constraints.
- **AWO** defines methodological structure and workflow ordering.
- **CRI-CORE** enforces mechanically checkable conditions derived from those definitions.

CRI-CORE SHALL NOT collapse, substitute, or merge these responsibilities.

---

### 1.4 Stack separation invariant (authoritative)

CRI-CORE is bound by the Aurora stack separation invariant:

> No layer may define, reinterpret, or enforce responsibilities that belong to another layer.

This invariant applies in both directions:

- CRI-CORE MUST NOT assume responsibilities of ARI, NTD, NTS, or AWO.
- CRI-CORE MUST treat those layers as externally authoritative inputs.

All enforcement logic implemented by CRI-CORE must be traceable to a requirement originating in:

- ARI governance,
- NTS normative constraints, or
- AWO methodological structure.

---

### 1.5 Relationship to NTS (authoritative source)

CRI-CORE implements enforcement surfaces that correspond to the normative boundaries defined in:

**Neurotransparency Specification (NTS), Section 11 — Relationship to Downstream Systems.**

In accordance with NTS §11:

- NTS defines *what must be disclosed*.
- CRI-CORE determines only *whether required disclosures and related artifacts exist and are structurally valid*.
- CRI-CORE SHALL NOT reinterpret NTS semantics.
- CRI-CORE SHALL NOT weaken, strengthen, or extend NTS requirements.

If an enforcement condition cannot be derived directly from NTS normative language or ARI-ratified governance rules, it is out of scope for CRI-CORE.

---

### 1.6 Prohibition on semantic expansion

CRI-CORE SHALL NOT introduce:

- additional disclosure categories,
- additional epistemic roles,
- additional legitimacy criteria,
- or additional validation semantics

beyond those explicitly defined by NTS and adopted by ARI.

Any enforcement behavior that would require semantic interpretation of:

- disclosure adequacy,
- epistemic sufficiency,
- or claim legitimacy

is explicitly prohibited at the CRI-CORE layer.

---

### 1.7 Enforcement boundary summary

CRI-CORE enforces:

- structure,
- declared invariants,
- independence constraints,
- provenance and integrity anchors,
- and gating conditions defined by upstream layers.

CRI-CORE does not decide:

- what must be disclosed,
- when disclosures must be produced,
- how workflows must be designed,
- or whether a claim is epistemically legitimate.

This boundary is mandatory and non-negotiable.
## 2. Contract types enforced by CRI-CORE

### 2.1 Intent

This section enumerates the **categories of contracts** that CRI-CORE is permitted to validate and enforce.

CRI-CORE is restricted to validating **explicit, externally-defined contract surfaces**.
It SHALL NOT introduce new contract types, reinterpret contract meaning, or derive implicit obligations.

Only the contract categories listed in this section are in scope.

---

### 2.2 Enforceable contract categories

CRI-CORE MAY validate and enforce the following contract categories only.

#### 2.2.1 AWO artifact contracts (by reference)

CRI-CORE MAY validate contracts defined by the Aurora Workflow Orchestration (AWO) method layer.

These contracts include the canonical AWO artifact contracts and their satisfaction conditions.

Important constraints:

- AWO contracts are **not defined in this document**.
- CRI-CORE SHALL treat AWO contracts as **external authoritative definitions**.
- CRI-CORE SHALL reference the AWO contract index as the sole authoritative source for:
  - contract identifiers,
  - required artifacts,
  - and structural satisfaction conditions.

CRI-CORE SHALL NOT:

- redefine AWO contracts,
- modify contract semantics,
- add additional contract conditions,
- or infer new contract categories beyond those listed in the AWO contract index.

Authoritative source:
- AWO Contract Index

---

#### 2.2.2 CRI run artifact contract

CRI-CORE enforces a dedicated **CRI run artifact contract** that governs the structure, integrity, and traceability of an executed CRI-CORE run.

This contract:

- defines the required structure and contents of a CRI-CORE execution record,
- defines the minimum integrity and provenance guarantees for a run,
- and defines the auditable boundary of an enforcement event.

The CRI run artifact contract is defined **normatively and exclusively** in:

- **Section 3 of this document**

CRI-CORE SHALL NOT treat any other run structure, execution output, or workflow side effect as a contract unless it is explicitly defined by that section.

Authoritative source:
- This document, Section 3

---

### 2.3 Contract scope boundary

CRI-CORE contract enforcement is limited to:

- AWO artifact contracts (by external reference), and
- the CRI run artifact contract defined in this document.

Any of the following are explicitly out of scope as enforceable contract types:

- epistemic legitimacy contracts,
- disclosure semantics contracts,
- workflow design contracts,
- governance or ratification contracts,
- or institutional compliance contracts.

---

### 2.4 Authoritative source alignment

For each enforced contract category, CRI-CORE MUST be able to trace the contract definition to one of the following authoritative sources:

- the AWO Contract Index, or
- this document (Section 3).

If a contract definition cannot be traced to one of these two sources, it SHALL NOT be enforced by CRI-CORE.

## 3. CRI run artifact contract (normative)

### 3.1 Intent

This section defines the **normative contract** for a single CRI-CORE–governed execution run.

The contract specifies the **minimum required structure, files, and invariants** that MUST exist for a run to be considered:

- structurally valid,
- independently auditable,
- integrity-preserving,
- and suitable for downstream enforcement and publication.

This contract governs **only the run artifact produced by CRI-CORE execution**.  
It does not govern AWO artifacts themselves.

This section is the **sole authoritative definition** of the CRI run artifact contract.

---

### 3.2 Contract scope

The CRI run artifact contract applies to:

- each discrete execution of a CRI-CORE workflow,
- as materialized in a single run directory,
- produced by the CRI execution workflow.

The contract is evaluated per run.

---

### 3.3 Run identifier and run directory

Each run MUST have a unique run identifier (`RUN_ID`).

A run MUST be materialized at:
```
runs/<RUN_ID>/
```
the run directory MUST declare the CRI-CORE contract version under which the run was executed.

The run directory MUST contain a contract declaration file at:
```  
runs/<RUN_ID>/contract.json
```  
This file MUST declare the exact enforcement contract version governing the run.

The run identifier:

- MUST be recorded in the execution environment,
- MUST be persisted to disk during execution,
- MUST be stable for the lifetime of the run.

The run directory is the **root contract surface** for the remainder of this section.

---

### 3.4 Required subdirectories and files

A CRI run directory MUST contain the following structural elements.

The presence of additional files or directories is permitted, but SHALL NOT replace or override the required surfaces defined below.

At minimum, the run directory MUST contain:

- a machine-generated run report
- machine validation outputs
- randomness / determinism metadata
- an approval record
- integrity manifests
- attestation material (after finalization)

---

### 3.5 Machine-generated reports and summaries

The run directory MUST contain a machine-generated run report.

At minimum:
```
runs/<RUN_ID>/report.md
```
The report MUST:

- be produced automatically by the execution pipeline,
- summarize the executed workflow and produced artifacts,
- be suitable for human audit review,
- and remain immutable after finalization.

If additional machine summaries are produced (for example, gate-specific summaries), they MUST be stored within the run directory and referenced by the report.

---

### 3.6 Randomness / determinism metadata

The run directory MUST contain a randomness metadata file:
```
runs/<RUN_ID>/randomness.json
```
This file MUST minimally declare:

- the run identifier,
- whether execution is deterministic,
- and any declared seed value (or explicit null).

The file MUST be created by the execution pipeline.

This metadata establishes the reproducibility and non-determinism disclosure surface for the run.

---

### 3.7 Invariant validation outputs

The run directory MUST contain the outputs of CRI-CORE invariant validation.

These outputs MUST:

- be produced by automated validation tooling,
- represent the structural and governance invariant checks applied to the run,
and be persisted inside the run directory, example:
```
runs/<RUN_ID>/validation
```

At least one invariant validation phase MUST occur before finalization.

The specific invariant schemas and validation logic are out of scope for this contract.
Only the existence and persistence of the validation outputs are governed here.

---

### 3.8 Approval record

The run directory MUST contain a human approval record:
```
runs/<RUN_ID>/approval.json
```
The approval record MUST include, at minimum:

- the run identifier,
- the approving human actor,
- the approval timestamp in RFC 3339 UTC format,
- and a reference to the workflow execution context.

The approval record MUST be created only after all required validation gates have completed.

A run SHALL NOT be considered finalized without this approval record.

---

### 3.9 Attestation material

After successful approval and finalization, the run MUST include attestation material.

Attestation material MUST be stored under:
```
governance/attestations/<RUN_ID>/
```  
The run directory MUST reference the attestation location.
Example:
```
runs/<RUN_ID>/attestation.ref
```  

At minimum, attestation material MUST include:

- a human-readable attestation statement,
- cryptographic signature material,
- and any associated certificates required to verify the signatures.

The attestation material MUST be produced by the CRI-CORE finalization process.

Attestation material is not part of the run directory and SHALL be treated as a separate governance surface that is cryptographically bound to the run artifact via references and signatures.

Attestation material MUST declare:

- the signature algorithm,
- the public verification key or certificate reference,
- and the verification procedure or standard used.
  
---

### 3.10 Integrity manifest

The run directory MUST contain a deterministic integrity manifest:
```
runs/<RUN_ID>/SHA256SUMS.txt
```
The manifest MUST:

- list cryptographic hashes of all files within the run directory,
- be generated using a deterministic file ordering,
- and be generated after all run files are present.

The integrity manifest establishes the integrity boundary of the run artifact.

The integrity manifest applies only to the contents of runs/<RUN_ID>/.
Attestation material and governance surfaces are excluded from this manifest and are verified through their own signature and attestation mechanisms.

---

### 3.11 Publication and commit requirements

A finalized run MUST be committed to the governing repository.

The commit MUST include:

the complete run directory: [runs/<RUN_ID>/]
and the corresponding attestation material: [governance/attestations/<RUN_ID>/]
A run SHALL NOT be considered published unless:

- it is committed to the repository,
- and its commit is traceable to the execution context recorded in the approval record.

---

### 3.12 Finalization immutability

After finalization:

- files within `runs/<RUN_ID>/` MUST NOT be modified,
- attestation material for the run MUST NOT be modified,
- and integrity manifests MUST NOT be regenerated.

Any subsequent change to a run requires creation of a new run with a new run identifier.

---

### 3.13 Contract invariants

A CRI run artifact is contract-satisfying if and only if:

- a valid run directory exists,
- all required files and directories defined in this section exist,
- an approval record exists,
- invariant validation outputs exist,
- integrity manifests exist,
- attestation material exists,
- and the run has been committed to the governing repository.

Failure of any required element SHALL render the run non-compliant with this contract.

The contract declaration file exists and matches the contract version used by the enforcement engine.

---

### 3.14 Authoritative sources

The normative structure and behavior defined in this section derive exclusively from:

- the CRI prototype execution workflow, and
- the run folder structure produced by that workflow.

No other documents define or extend the CRI run artifact contract.

## 4. Deterministic enforcement behavior and gate semantics

### 4.1 Intent

This section defines the **deterministic enforcement behavior** that CRI-CORE is permitted to perform over governed executions.

It specifies:

- what CRI-CORE enforces,
- when enforcement is evaluated,
- and which decisions are explicitly delegated to human approval.

This section defines **execution-time and publication-time behavior only**.

It does not introduce new contracts.
It operationalizes the contracts defined in:

- the AWO contract index, and
- the CRI run artifact contract (Section 3).

---

### 4.2 Enforcement scope

CRI-CORE MAY enforce only the following categories of constraints:

- structural presence of required artifacts,
- contract satisfaction of governed artifacts,
- declared invariant checks,
- role and independence constraints,
- integrity and immutability guarantees,
- and publication gating requirements.

CRI-CORE SHALL NOT enforce:

- epistemic correctness,
- semantic interpretation of claims,
- disclosure sufficiency or meaning,
- workflow authoring rules,
- or governance policy.

---

### 4.3 Deterministic execution boundary

All CRI-CORE enforcement behavior MUST be:

- machine-evaluable,
- reproducible from the same inputs,
- and free of discretionary interpretation.

Enforcement outcomes MUST depend solely on:

- run artifacts,
- declared contracts,
- and declared validation rules.

No human judgment is permitted inside enforcement logic.

---

### 4.4 Mandatory enforcement stages

A CRI-CORE governed execution MUST support the following enforcement stages.

The exact implementation MAY vary, but the logical stages are mandatory.

---

#### 4.4.1 Execution validation stage

During execution, CRI-CORE MUST:

- execute the declared workflow,
- record run outputs,
- and materialize the run directory defined in Section 3.

This stage establishes the run artifact surface.

---

#### 4.4.2 Structural invariant validation stage

After execution, CRI-CORE MUST perform automated validation of declared invariants.

At minimum, this stage MUST verify:

- required artifact presence,
- required structural files for the run contract,
- and declared invariant checks.

Validation results MUST be persisted into the run directory.

---

#### 4.4.3 Independence and role separation validation stage

CRI-CORE MUST validate independence constraints for the run.

At minimum, this stage MUST evaluate:

- the declared orchestrator identity,
- the declared reviewer identity,
- and whether self-approval has occurred.

If self-approval occurs:

- it MUST be detected,
- and it MUST be explicitly flagged.

If self-approval is not explicitly permitted, enforcement MUST fail.

This stage enforces structural independence only.
It does not evaluate reviewer competence or review quality.

---

#### 4.4.4 Human approval gate

CRI-CORE MUST require an explicit human approval action prior to finalization.

The approval MUST:

- occur after all automated validation stages,
- be attributable to a human actor,
- and be persisted as the approval record defined in Section 3.

CRI-CORE SHALL NOT synthesize approval.

The approval record MUST refer to the exact run artifact state that will be finalized and attested.
No modification of run files SHALL occur between approval and finalization.  

---

#### 4.4.5 Finalization and attestation stage

After approval, CRI-CORE MUST:

- generate integrity manifests,
- generate attestation material,
- and bind the attestation to the finalized run payload.

Finalization MUST occur after all run files are present.

---

#### 4.4.6 Publication and commit stage

CRI-CORE MUST ensure that:

- the finalized run directory,
- and its attestation material

are committed to the governing repository.

If the publication step fails, the run SHALL NOT be considered finalized.

---

### 4.5 Enforcement failure semantics

If any mandatory enforcement stage fails:

- the run MUST NOT be finalized,
- the run MUST NOT be published,
- and attestation material MUST NOT be produced.

Failure does not invalidate previously published runs.

---

### 4.6 Immutability enforcement

After finalization:

- CRI-CORE MUST treat the run directory as immutable,
- and MUST NOT regenerate integrity manifests or attestations.

Any modification to finalized run material constitutes a contract violation.

---

### 4.7 Enforcement result surface

Enforcement results MUST be recorded as machine-readable outputs and persisted into the run artifact.

At minimum, results MUST allow an independent party to determine:

- which stages passed,
- which stages failed,
- and which actor approved the run.

---

### 4.8 Authoritative sources

The enforcement behavior defined in this section is derived exclusively from:

- the CRI prototype workflow, and
- the CRI run artifact contract defined in Section 3.

No other documents define CRI-CORE enforcement behavior.
## 5. Independence and validation enforcement

### 5.1 Intent

This section defines how CRI-CORE enforces **independence and non-circular validation** for governed runs.

The purpose of this enforcement is to ensure that:

- the agent that orchestrates a run is not the same agent that validates or approves it,
- validation is not self-referential,
- and any permitted exception is explicitly declared, recorded, and auditable.

This section operationalizes the independence requirements defined by NTS.
It does not redefine epistemic roles or validation semantics.

---

### 5.2 Orchestrator vs reviewer distinction

For every governed run, CRI-CORE MUST identify at minimum:

- the **orchestrator** — the actor responsible for initiating and executing the run, and
- the **reviewer** — the actor responsible for approving the run during the human audit gate.

These identities MUST be captured as machine-readable fields within the run context and used during enforcement.

CRI-CORE MUST treat these roles as structurally distinct validation roles, regardless of whether they refer to the same underlying person.

Orchestrator and reviewer identities MUST be represented as structured identifiers containing at minimum:

- a stable identifier string
- an identity type (for example: human, service, workflow, organization)

The exact identity resolution semantics are out of scope, but structural equality of the identifier fields SHALL be used for independence checks.

---

### 5.3 Mandatory independence check

CRI-CORE MUST evaluate, during the independence validation stage, whether:
```
orchestrator == reviewer
```
If the identities match, the run SHALL be classified as a self-approval attempt.

This evaluation is structural and identity-based only.
CRI-CORE SHALL NOT attempt to infer intent, quality of review, or degree of scrutiny.

---

### 5.4 Self-approval prohibition

By default, CRI-CORE MUST prohibit self-approval.

If the orchestrator and reviewer are identical and no explicit override is present, enforcement MUST fail and the run MUST NOT proceed to finalization.

This prohibition enforces the non-circular validation requirement.

---

### 5.5 Explicit override pathway

CRI-CORE MAY permit a controlled override of the self-approval prohibition only if:

- an explicit override flag is provided at workflow invocation time, and
- the override is evaluated by enforcement logic before approval is accepted.

When an override is used:

- the run MUST be marked as self-approved,
- the override MUST be explicitly recorded in the independence validation output,
- and the run MUST remain distinguishable from independently approved runs.

Overrides do not weaken the independence rule.
They create a formally declared exception that is preserved for audit.

---

### 5.6 Logging of independence outcomes

For every run, CRI-CORE MUST produce a machine-readable independence validation record.

At minimum, this record MUST contain:

- the orchestrator identity,
- the reviewer identity,
- whether self-approval was detected,
- whether an override was used,
- and the final independence outcome (pass or fail).

The independence record MUST be persisted into the run’s governance log surface and committed alongside the finalized run artifacts.

---

### 5.7 Validation boundary

CRI-CORE enforces independence and non-circular validation only at the structural and identity level.

CRI-CORE SHALL NOT evaluate:

- the correctness of the review,
- the competence of the reviewer,
- the sufficiency of epistemic scrutiny,
- or the content of validation judgments.

Those concerns remain outside CRI-CORE’s enforcement scope.

---

### 5.8 Authoritative sources

The requirements in this section are derived exclusively from:

- Neurotransparency Specification (NTS), Section 9 — Independence & Validation Constraints, and
- the gate-2 independence enforcement logic defined in the CRI prototype workflow.

## 6. Provenance and integrity enforcement

### 6.1 Intent

This section defines the **mechanical provenance and integrity guarantees** enforced by CRI-CORE
for governed runs.

The purpose of this enforcement is to ensure that:

- run artifacts are cryptographically and structurally bound to their execution context,
- provenance anchors are present and stable,
- integrity can be independently verified after publication,
- and historical continuity is preserved across revisions.

CRI-CORE enforces provenance and integrity **as structural and cryptographic properties only**.
It does not interpret epistemic meaning.

---

### 6.2 Required provenance anchors

For every governed run, CRI-CORE MUST require the following provenance anchors to exist within the run surface:

- a stable **run identifier** and corresponding run directory,
- a machine-generated **run report** or equivalent execution summary,
- explicit linkage to the governing workflow execution (workflow run URL or equivalent),
- an **approval record** identifying the approving actor and approval time,
- references to all artifacts included in the finalized run payload.

These anchors MUST be sufficient to allow an independent party to determine:

- which run produced the artifacts,
- under which workflow execution,
- and under which approval event.

---

### 6.3 Required integrity artifacts

For every finalized run, CRI-CORE MUST produce and persist the following integrity artifacts:

- a deterministic file-level hash manifest for the run directory (e.g. `SHA256SUMS.txt`),
- a finalized payload archive of the run directory,
- a cryptographic signature for the finalized payload,
- a cryptographic signature for the run attestation material.

The finalized payload archive MUST be located at:
```  
runs/<RUN_ID>/payload.tar.gz
```  
and MUST contain an exact byte-for-byte archive of the run directory contents.

The hash manifest MUST be generated deterministically over the full run directory contents.

The finalized payload and attestation material MUST be signed using an external signing mechanism
suitable for independent verification.

The signing and verification algorithms used MUST be explicitly recorded in the attestation material.

---

### 6.4 Attestation material

For every governed run, CRI-CORE MUST generate attestation material that binds together:

- the run identifier,
- the approval record,
- the integrity manifest,
- and the workflow execution context.

The attestation material MUST be stored in a stable, run-scoped attestation location and MUST be
included in the final publication payload.

---

### 6.5 Randomness and determinism metadata

CRI-CORE MUST require the presence of explicit metadata describing execution determinism, including:

- whether the run was deterministic or non-deterministic,
- and any declared randomness or seed information if available.

This metadata is required even when determinism cannot be guaranteed.

Its purpose is to preserve reconstructibility expectations, not to enforce replay.

---

### 6.6 Invariant validation outputs

CRI-CORE MUST persist machine-readable outputs for all invariant and structural validation checks
performed during the run.

These outputs MUST be stored within the run directory and included in the integrity manifest.

Invariant results MUST be preserved exactly as produced and MUST NOT be recomputed or rewritten
during finalization.

---

### 6.7 Revision and continuity constraints

When a governed run is finalized:

- the run directory MUST be committed immutably as a historical record,
- all integrity artifacts and attestation material MUST be committed alongside the run,
- and any subsequent revisions MUST produce a new run with a new run identifier.

CRI-CORE MUST NOT permit in-place modification of finalized run artifacts.

Continuity is preserved by additive runs and explicit linkage, not by mutation.

---

### 6.8 Publication and commit binding

CRI-CORE MUST bind provenance and integrity to publication by requiring that:

- the finalized run directory,
- the integrity manifest,
- and the attestation material

are committed together in a single publication action.

The commit itself constitutes part of the provenance surface and MUST remain discoverable.

---

### 6.9 Explicit exclusions

CRI-CORE SHALL NOT:

- perform epistemic interpretation of provenance content,
- evaluate the meaning or quality of recorded cognition,
- define content-level provenance semantics,
- or assess whether recorded provenance satisfies doctrinal or disclosure intent.

CRI-CORE enforces only the presence, integrity, and continuity of provenance structures.

---

### 6.10 Authoritative sources

The requirements in this section are derived exclusively from:

- Neurotransparency Specification (NTS), Section 7 — Provenance & Integrity Requirements, and
the hashing, attestation, signing, and publication steps defined in the CRI prototype workflow.

## 7. Reconstruction support guarantees

### 7.1 Intent

This section defines the minimum reconstruction support that CRI-CORE MUST guarantee
through the preservation, publication, and linkage of run artifacts.

The purpose of these guarantees is to ensure that an independent party can
reconstruct — in principle — how a governed run produced and finalized its
artifacts, without requiring access to private systems, internal cognition, or
execution-time environments.

CRI-CORE guarantees reconstruction support through durable artifact structure,
stable references, and preserved machine outputs.

CRI-CORE does not guarantee computational replay.

---

### 7.2 Run artifact accessibility requirements

For every finalized run, CRI-CORE MUST ensure that:

- the complete run directory is published as part of the governed repository state,
- a finalized run payload archive is published and retained,
- and all integrity and attestation artifacts associated with the run are published
  and discoverable.

All run artifacts required for reconstruction MUST be accessible without requiring:

- access to private infrastructure,
- access to ephemeral execution environments,
- or privileged system credentials beyond repository access.

---

### 7.3 Linkage between run artifacts and governed artifacts

CRI-CORE MUST preserve explicit linkage between:

- the run identifier and the governed artifacts produced or finalized by the run, and
- the governed artifacts and the run directory that produced them.

At minimum, the run surface MUST allow a reviewer to determine:

- which run produced a given governed artifact, and
- which governed artifacts are included in a given run.

Linkage MAY be implemented through:

- inclusion manifests,
- run reports,
- release or approval records,
- or explicit references embedded in governed artifacts.

CRI-CORE does not define the semantic meaning of the governed artifacts.
It enforces only the existence and stability of linkage.

---

### 7.4 Reference stability guarantees

CRI-CORE MUST guarantee that references required for reconstruction remain stable
over time.

Specifically:

- run identifiers MUST remain unique and persistent,
- run directory paths MUST remain stable after publication,
- integrity manifests and attestation material MUST remain addressable at fixed,
  run-scoped locations,
- and references embedded in run reports and approval records MUST continue to
  resolve to their original targets.

CRI-CORE MUST NOT rewrite, relocate, or collapse historical run references.

If repository reorganization occurs, backward reference stability MUST be preserved
through explicit redirection or aliasing mechanisms.

---

### 7.5 Explicit exclusions

CRI-CORE SHALL NOT:

- attempt to replay or regenerate cognition,
- attempt to reproduce internal model states,
- require access to proprietary or transient execution environments,
- require disclosure of prompts, intermediate conversations, or internal model
  reasoning,
- or require capture of any internal cognitive representations.

Reconstruction under CRI-CORE is strictly structural and procedural.

---

### 7.6 Authoritative sources

The requirements in this section are derived exclusively from:

- Neurotransparency Specification (NTS), Section 8 — Reconstruction & Re-evaluation Requirements, and
- the published run payload structure produced by the CRI prototype workflow.
## 8. Failure classes

### 8.1 Intent

This section defines the structural and enforcement failure classes that CRI-CORE
MUST detect, surface, and enforce.

Failure classes defined here apply only to:

- artifact structure,
- contract compliance,
- enforcement invariants, and
- mechanical validation outcomes.

CRI-CORE does not classify, detect, or report failures of epistemic quality,
scientific validity, or semantic correctness.

---

### 8.2 Missing required artifacts

A failure MUST be raised when any artifact required by the CRI run artifact contract
(Section 3) is absent at the time a gate requires its presence.

This includes, but is not limited to:

- missing required run subdirectories,
- missing required reports or summaries,
- missing randomness or determinism metadata,
- missing invariant validation outputs,
- missing approval records,
- missing attestation material, and
- missing integrity manifests.

---

### 8.3 Invariant violations

A failure MUST be raised when any invariant defined by:

- the CRI run artifact contract (Section 3), or
- enforcement rules implemented by CRI-CORE

is violated.

This includes:

- malformed run identifiers,
- structural non-conformance of the run directory,
- invalid or incomplete invariant validation outputs,
- and violations of required ordering or gating dependencies.

---

### 8.4 Failed independence checks

A failure MUST be raised when independence and non-circular validation requirements
cannot be satisfied.

This includes:

- the orchestrator and reviewer being identical when self-approval is not explicitly
  permitted,
- missing reviewer identity,
- missing or invalid independence validation outputs,
- and failed gate-2 independence enforcement.

---

### 8.5 Failed integrity checks

A failure MUST be raised when integrity guarantees cannot be established.

This includes:

- missing or malformed integrity manifests,
- failure to generate deterministic file hashes,
- hash mismatches between recorded and observed artifacts,
- missing or unverifiable signatures,
- and failed signature verification steps.

---

### 8.6 Missing or invalid approvals

A failure MUST be raised when required human or environment-gated approvals are:

- missing,
- malformed,
- incomplete,
- or recorded after finalization steps.

This includes:

- missing approval records,
- missing approval identities,
- missing approval timestamps,
- and approvals that do not correspond to the finalized run state.

---

### 8.7 Invalid or incomplete attestation material

A failure MUST be raised when required attestation material is:

- missing,
- structurally invalid,
- incomplete,
- or cannot be verified using the prescribed verification procedure.

This includes:

- missing attestation documents,
- missing or malformed signature files,
- missing certificates,
- and failed verification of attested artifacts.

---

### 8.8 Explicit exclusion

CRI-CORE SHALL NOT classify any of the following as failures:

- semantic errors in artifacts,
- scientific or experimental errors,
- epistemic quality deficiencies,
- methodological soundness issues,
- or correctness of conclusions.

Such determinations remain explicitly outside the scope of CRI-CORE.

---

### 8.9 Authoritative sources

The requirements in this section are derived exclusively from:

- Neurotransparency Specification (NTS), Section 10 — Failure Modes and Enforcement Boundaries, and
the failure and halt behavior implemented in the CRI prototype gate logic.

## 9. Boundary with AWO

### 9.1 Intent

This section defines the strict interface boundary between Aurora Workflow Orchestration (AWO)
and CRI-CORE.

The purpose of this boundary is to ensure that:

- AWO remains the sole authority for workflow structure and execution ordering, and
- CRI-CORE remains a deterministic validation and enforcement layer operating only on
  declared artifacts and declared metadata.

CRI-CORE SHALL consume outputs of AWO.
CRI-CORE SHALL NOT participate in workflow design, orchestration, or semantic interpretation.

---

### 9.2 Artifacts consumed by CRI-CORE from AWO

CRI-CORE MAY consume only the following categories of artifacts produced by AWO executions:

- AWO execution artifacts recorded under the governed run directory
  (for example: execution logs, reports, summaries, and invariant results),
- machine-generated summaries and reports produced during the AWO run,
- declared run-level metadata produced by the orchestration layer,
- declared scope, execution, and review artifacts referenced by the run.

CRI-CORE SHALL treat all AWO-produced artifacts as opaque payloads whose internal
meaning is not interpreted.

CRI-CORE SHALL rely only on their presence, structure, identity, and declared linkage.

---

### 9.3 Metadata assumed as inputs

CRI-CORE MAY assume as inputs only metadata that is explicitly declared by AWO outputs,
including:

- the run identifier,
- declared orchestrator identity,
- declared workflow file or workflow reference,
- declared scope and review summaries (if present),
- declared artifact references produced by the run.

CRI-CORE SHALL NOT derive or infer metadata that is not explicitly present in the run
artifacts or their associated metadata records.

---

### 9.4 Prohibition on inferring workflow intent or semantics

CRI-CORE SHALL NOT:

- infer the intent of a workflow,
- interpret the purpose of any step or phase,
- infer epistemic meaning of any artifact,
- infer disclosure semantics,
- infer validation semantics beyond declared structural contracts,
- or reconstruct workflow logic.

CRI-CORE enforcement is limited strictly to:

- contract presence,
- structural conformity,
- declared identity and role assertions,
- declared linkage relationships,
- and declared approval and attestation records.

Any interpretation of workflow meaning, methodological purpose, or epistemic role
remains exclusively within AWO and downstream governance layers.

---

### 9.5 Authoritative sources

The requirements in this section are derived exclusively from:

- the Aurora Workflow Orchestration (AWO) specification, and
the AWO run orchestration outputs used as inputs to CRI-CORE validation and enforcement.

## 10. Boundary with NTS

### 10.1 Intent

This section defines the strict relationship between CRI-CORE and the
Neurotransparency Specification (NTS).

CRI-CORE operates as a deterministic enforcement and validation layer with
respect to NTS-defined requirements.

NTS defines epistemic and disclosure requirements.

CRI-CORE enforces only the mechanical and structural realizability of those
requirements.

---

### 10.2 Relationship to NTS requirements

CRI-CORE SHALL verify, for all governed runs and governed artifacts, the
following classes of properties derived from NTS:

- presence of all required disclosure-related artifacts and records,
- structural conformity of those artifacts to their declared contracts,
- declared linkage between disclosures and the artifacts they qualify,
- continuity of disclosure material across revisions and releases, and
- preservation of required references and anchors needed for reconstruction.

CRI-CORE enforcement is limited to verifying that required disclosures:

- exist,
- are structurally valid,
- are correctly linked,
- and remain available and stable across governed transitions.

---

### 10.3 Non-interpretation of epistemic meaning or adequacy

CRI-CORE SHALL NOT evaluate:

- the epistemic sufficiency of any disclosure,
- the correctness, completeness, or clarity of any explanation,
- the adequacy of any attribution, evidence reference, or reasoning trace,
- or the scientific, methodological, or philosophical quality of any content.

All determinations of epistemic meaning, adequacy, or legitimacy remain the
exclusive responsibility of NTS and the governance layers that adopt it.

CRI-CORE operates only on declared structure and declared continuity.

---

### 10.4 Explicit prohibition on semantic re-encoding

CRI-CORE MUST NOT:

- redefine any concept introduced by NTS,
- introduce alternative interpretations of NTS terminology,
- embed NTS semantics into validation logic beyond structural requirements,
- or translate NTS requirements into new normative meanings.

CRI-CORE validation logic SHALL be traceable to explicit structural and
continuity constraints derived from NTS, without semantic reinterpretation.

NTS remains the sole normative authority on disclosure semantics and epistemic
requirements.

---

### 10.5 Authoritative sources

The requirements in this section are derived exclusively from:

- Neurotransparency Specification (NTS) §§5–10, and
- Neurotransparency Specification (NTS) §11.

## 11. Boundary with ARI governance

### 11.1 Intent

This section defines the authority boundary between CRI-CORE and the
Aurora Research Initiative (ARI) governance layer.

CRI-CORE is a deterministic enforcement and validation system.

ARI is the institutional governance authority.

CRI-CORE operates strictly in service of ARI governance and possesses no
independent governance authority.

---

### 11.2 Relationship between CRI-CORE and ARI

ARI defines:

- governance authority,
- policy and specification adoption,
- ratification and change control,
- institutional legitimacy,
- and dispute resolution.

CRI-CORE:

- produces enforcement outputs and validation results,
- records execution evidence and constraint outcomes,
- and preserves mechanically verifiable traces required by governance.

CRI-CORE SHALL NOT function as a governance body.

---

### 11.3 Governance logs and approvals

CRI-CORE SHALL reference governance-controlled artifacts, including but not
limited to:

- governance log entries,
- approval records,
- attestation and independence records,
- and versioned governance metadata.

CRI-CORE MAY:

- verify the existence of required governance log files,
- verify their structural validity,
- verify their linkage to the governed run or artifact,
- and verify their continuity across revisions.

CRI-CORE SHALL treat all governance logs and approvals as externally
authoritative inputs.

CRI-CORE SHALL NOT generate, edit, or reinterpret governance decisions.

---

### 11.4 Consumption of enforcement outputs by ARI governance

Enforcement outputs produced by CRI-CORE MAY be consumed by ARI governance
processes as objective technical evidence, including:

- pass or fail status of defined enforcement gates,
- invariant validation results,
- independence and non-circularity check results,
- integrity and continuity verification results,
- and attestation and signature verification outcomes.

CRI-CORE outputs MAY be used by ARI governance to support:

- ratification decisions,
- remediation actions,
- release approvals,
- and compliance determinations.

CRI-CORE outputs SHALL be treated as technical signals, not as governance
judgments.

---

### 11.5 Prohibition on ratification, adjudication, and dispute resolution

CRI-CORE MUST NOT:

- ratify specifications, artifacts, or releases,
- approve or reject governance proposals,
- adjudicate compliance disputes,
- interpret policy intent,
- resolve conflicts between specifications,
- or override governance decisions.

All such authority resides exclusively with ARI governance.

CRI-CORE enforcement outcomes SHALL NOT be interpreted as institutional
approval, rejection, or certification.

---

### 11.6 Authority separation invariant

The following invariant SHALL hold:

- ARI governs meaning, authority, and legitimacy.
- CRI-CORE governs only mechanical enforcement of declared constraints.

Any system behavior in which CRI-CORE influences governance outcomes beyond
providing enforcement evidence SHALL be considered a violation of this
boundary.

---

### 11.7 Authoritative sources

The requirements in this section are derived exclusively from:

- the Aurora Research Initiative (ARI) governance framework.

## 12. Versioning and change control

### 12.1 Intent

This section defines how the CRI-CORE enforcement contract defined in this
document evolves over time, and how changes to enforcement requirements,
invariants, and validation surfaces are governed.

The objective is to preserve the stability of enforcement meaning for all
previously governed runs and artifacts.

---

### 12.2 Versioned enforcement contract

This document SHALL be versioned as a normative enforcement contract.

Each published version of this document defines a fixed and authoritative
set of enforcement rules, invariants, and required artifacts for CRI-CORE.

CRI-CORE executions SHALL declare the exact contract version under which
enforcement was performed.

---

### 12.3 Semantic meaning of breaking vs non-breaking changes

A change SHALL be classified as a **breaking change** if it:

- alters required run artifact structure,
- alters required files or directories,
- changes the meaning or outcome of an invariant,
- changes independence or validation constraints,
- changes integrity or provenance enforcement behavior,
- or changes failure classification semantics.

A change SHALL be classified as a **non-breaking change** if it:

- adds optional enforcement checks,
- adds optional metadata fields,
- clarifies documentation without changing enforcement behavior,
- improves diagnostics, reporting, or tooling without changing pass/fail logic.

---

### 12.4 Versioning scheme

This enforcement contract SHALL follow semantic versioning:
```
MAJOR.MINOR.PATCH
```
Where:

- **MAJOR** increments indicate breaking enforcement changes,
- **MINOR** increments indicate backward-compatible enforcement additions,
- **PATCH** increments indicate editorial or corrective updates that do not
  alter enforcement meaning.

---

### 12.5 Explicit publication requirement

Every version of this enforcement contract SHALL be:

- explicitly published,
- uniquely versioned,
- and preserved as an immutable artifact.

Silent modification of enforcement requirements is prohibited.

CRI-CORE SHALL NOT apply unpublished or unversioned enforcement rules.

---

### 12.6 Preservation of historical enforcement meaning

Once a version of this contract is published:

- its enforcement semantics SHALL remain fixed,
- its failure classes SHALL remain fixed,
- and its validation meaning SHALL remain fixed.

Past runs and artifacts SHALL be interpreted only under the version of the
contract that governed their execution.

Later versions SHALL NOT retroactively reinterpret, reclassify, or invalidate
historical enforcement outcomes.

---

### 12.7 Backward compatibility and coexistence

Multiple enforcement contract versions MAY coexist.

CRI-CORE SHALL support validation and verification of historical runs using
their original declared contract version.

Upgrading to a newer contract version SHALL be an explicit action.

---

### 12.8 Change documentation

Every change to this enforcement contract SHALL be accompanied by a change
record describing:

- the affected sections,
- the rationale for the change,
- the compatibility classification (breaking or non-breaking),
- and the version increment applied.

---

### 12.9 Prohibition on semantic drift

Tooling changes, refactors, or implementation changes within CRI-CORE SHALL
NOT introduce behavioral drift relative to the published contract.

If enforcement behavior changes, the contract MUST be revised and re-published
under a new version.

---

### 12.10 Authoritative sources

The requirements in this section are derived from:

- ARI document governance and publication rules,
- NTS §12 (Versioning & Change Control).

## 13. Non-goals (hard boundary section)

### 13.1 Intent

This section explicitly freezes the scope of CRI-CORE.

The purpose of this section is to prevent functional creep, semantic drift,
and layer collapse within the Aurora stack.

Anything not explicitly authorized by this document SHALL be treated as
out of scope for CRI-CORE.

---

### 13.2 Hard non-goals

CRI-CORE SHALL NOT perform, attempt, or imply any of the following functions.

#### 13.2.1 No claim validation

CRI-CORE does not validate the truth, plausibility, soundness, or defensibility
of claims contained in any artifact.

---

#### 13.2.2 No epistemic evaluation

CRI-CORE does not evaluate:

- reasoning quality,
- methodological rigor,
- evidentiary sufficiency,
- interpretive correctness,
- or scientific merit.

Epistemic judgment is explicitly outside the enforcement layer.

---

#### 13.2.3 No AI disclosure semantics

CRI-CORE does not define, reinterpret, extend, or qualify:

- AI disclosure meaning,
- cognitive influence categories,
- attribution semantics,
- epistemic weight classifications,
- or reconstruction sufficiency.

All such semantics are governed exclusively by NTS.

---

#### 13.2.4 No workflow prescription

CRI-CORE does not:

- define workflow stages,
- impose sequencing rules,
- design orchestration logic,
- or prescribe research or operational processes.

Workflow ordering and orchestration belong exclusively to AWO.

---

#### 13.2.5 No governance authority

CRI-CORE does not:

- ratify documents,
- adjudicate disputes,
- approve policies,
- determine institutional legitimacy,
- or resolve governance outcomes.

Governance authority belongs exclusively to ARI.

---

#### 13.2.6 No authorship or responsibility assignment

CRI-CORE does not assign:

- authorship,
- intellectual ownership,
- credit,
- accountability,
- or legal or institutional responsibility.

CRI-CORE only verifies declared structures and artifacts.

---

#### 13.2.7 No correctness or quality certification

CRI-CORE does not certify, endorse, or imply:

- correctness,
- quality,
- reproducibility,
- robustness,
- safety,
- trustworthiness,
- or scientific validity.

Passing CRI-CORE enforcement indicates only that required structures,
invariants, and governance constraints were satisfied.

---

### 13.3 Prohibition on boundary expansion

CRI-CORE SHALL NOT be extended, configured, or repurposed to perform any of
the non-goal functions listed in this section.

Any feature, rule, or integration that would cause CRI-CORE to cross these
boundaries MUST be rejected or relocated to the appropriate Aurora layer.

---

### 13.4 Authoritative sources

The requirements in this section are derived from:

- the Aurora stack separation invariant,
- the limitations and non-goals sections of the Neurotransparency Specification (NTS).
