---
title: "CRI-CORE — Deterministic Enforcement Kernel"
filetype: "documentation"
type: "repository-overview"
domain: "enforcement"
version: "0.13.0"
doi: "10.5281/zenodo.19080238"
status: "Active"
created: "2026-02-19"
updated: "2026-05-03"

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
  - "CRI-CORE v0.13.0"
  - "Deterministic Enforcement Kernel"
  - "Execution Boundary Enforcement"
---

# CRI-CORE — Execution Boundary Enforcement Kernel

CRI-CORE is a deterministic enforcement engine that decides whether an action is allowed to execute.

It does not generate actions.
It does not manage workflows.
It does not store state.

It enforces one thing:

> Whether a proposed action is admissible at the moment of execution.

---

## Core Concept

All actions must pass through a single evaluation boundary:

```

INPUT:

* compiled_contract
* proposal
* run_context

OUTPUT:

* commit_allowed (True / False)
* stage_results (full trace of evaluation)

````

If `commit_allowed` is `False`, the action must not execute.

---

## Usage

```python
from cricore.api import evaluate_structured

result = evaluate_structured(
    proposal=proposal,
    compiled_contract=compiled_contract,
    run_context=run_context
)

if result.commit_allowed:
    execute_action()
else:
    block_action()
````

---

## Execution Model

CRI-CORE evaluates proposals through a fixed pipeline:

1. Structure
2. Contract binding
3. Independence (role separation)
4. Integrity (context validation)
5. Publication
6. Final commit decision

Each stage produces a deterministic result.

---

## Enforcement Guarantees

### 1. Contract Identity

The proposal must reference the exact contract used for evaluation.

```text
proposal.contract.hash == compiled_contract.contract_hash
```

Mismatch results in a blocked decision.

---

### 2. Proposal Immutability

The evaluation process does not modify the proposal.

All decisions are based on the caller’s original input.

---

### 3. Explicit Execution Mode

Execution mode is never silently downgraded.

```
function argument > run_context["mode"] > "local"
```

---

### 4. Deterministic Outputs

Identical inputs produce identical results.

Payload generation is byte-stable across runs.

---

### 5. Full Decision Trace

Every evaluation returns a complete stage-by-stage trace.

No hidden logic.

---

## Execution Modes

### Local (default)

* advisory enforcement
* missing integrity/publication does not block
* emits warnings

### Strict

* full enforcement
* all required conditions must pass
* no soft failures

---

## Non-Goals

CRI-CORE does not:

* execute actions
* manage identity systems
* persist logs
* provide audit guarantees

Those belong to higher layers (e.g., Waveframe Guard / Cloud).

---

## Status

Structured evaluation pipeline is stable.

Legacy filesystem-based execution is deprecated and retained only for reference.

---

## License

Apache 2.0

---

<div align="center">
  <sub>© 2026 Waveframe Labs — Independent Open-Science Research Entity</sub>
</div>