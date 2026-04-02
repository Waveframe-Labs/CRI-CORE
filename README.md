---
title: "CRI-CORE — Deterministic Enforcement Kernel"
filetype: "documentation"
type: "repository-overview"
domain: "enforcement"
version: "0.12.0"
doi: "10.5281/zenodo.19080238"
status: "Active"
created: "2026-02-19"
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

dependencies: []

anchors:
  - "CRI-CORE v0.12.0"
  - "Deterministic Enforcement Kernel"
  - "Execution Boundary Enforcement"
---
# CRI-CORE

**CRI-CORE v0.12.0 — Deterministic Enforcement Kernel**

**Concept DOI:** https://doi.org/10.5281/zenodo.19080238

CRI-CORE is a deterministic enforcement kernel that controls whether system actions are allowed to execute.

It operates at the execution boundary — the exact point where a system attempts to mutate state.

Instead of detecting or auditing issues after execution, CRI-CORE determines:

- whether an action is allowed to occur  
- or whether it is prevented entirely  

The kernel evaluates structural, authority, integrity, binding, and publication constraints over a sealed run artifact.

It does not interpret meaning.  
It evaluates deterministic structure and invariants only.

This makes CRI-CORE a control point, not a validation layer.

---

## What It Does

CRI-CORE sits directly at the **execution boundary** — the point where a system attempts to act.

It evaluates a run artifact representing a proposed state mutation and returns a single decision:

- allow execution  
- block execution  

No warnings.  
No after-the-fact auditing.  

Execution either happens — or it does not.

---

## Installation

Install from PyPI:

    pip install cricore

Requires Python 3.10+.

---

## Minimal Usage

CRI-CORE is typically integrated as an execution gate.

    from cricore.interface.governed_execute import governed_execute

    def execute_fn(proposal):
        return perform_mutation(proposal)

    result = governed_execute(
        proposal=proposal,
        policy=policy,
        execute_fn=execute_fn,
    )

    if result["commit_allowed"]:
        # execution occurred inside governed path
        pass
    else:
        # execution prevented
        handle_block(result["summary"])

---

### Kernel-Level API

The kernel API is also available directly:

    from cricore import evaluate

    result = evaluate(
        run_path=".",
        run_context={
            "identities": {},
            "integrity": {},
            "publication": {},
        },
    )

Returns:

    result.commit_allowed   # bool
    result.failed_stages    # List[str]
    result.summary          # str

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

The kernel does not interpret governance policy semantics.

It verifies only deterministic contract identity and structural alignment between proposal and compiled contract artifacts.

run_context supplies execution-time identity, integrity references, and publication context.

It is treated as declarative input and is not resolved or validated against external systems.

---

## Core Model

    Exploration (high velocity, non-deterministic)
        →
    Deterministic enforcement gate (CRI-CORE)
        →
    Governed state mutation

The kernel ensures that only structurally valid and cryptographically sealed runs are permitted to mutate governed state.

---

## Run Lifecycle

CRI-CORE operates on sealed run artifacts:

generate → finalize → evaluate → (optionally) commit

Once finalized, a run is immutable.

Any modification invalidates the seal and will cause enforcement failure.

---

## Enforcement Pipeline (v0.12.0)

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
- claim_ref required  
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

The caller is expected to route execution through this decision.

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

It is a deterministic structural enforcement gate only.

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
- Centralized execution authorization

It is domain-agnostic.

---

## Citation

If you use CRI-CORE in your work, please cite the concept DOI:

CRI-CORE — Deterministic Enforcement Kernel  
Wright, Shawn C.; Waveframe Labs (2026)  
https://doi.org/10.5281/zenodo.19080238

### BibTeX

```bibtex
@software{cricore_concept_2026,
  title   = {CRI-CORE: Deterministic Enforcement Kernel},
  author  = {Wright, Shawn C. and Waveframe Labs},
  year    = {2026},
  doi     = {10.5281/zenodo.19080238},
  url     = {https://doi.org/10.5281/zenodo.19080238}
}
```

---

<div align="center">
  <sub>© 2026 Waveframe Labs — Independent Open-Science Research Entity</sub>
</div>