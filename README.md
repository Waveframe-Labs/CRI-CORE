---
title: "CRI-CORE — Deterministic Enforcement Kernel"
filetype: "documentation"
type: "repository-overview"
domain: "enforcement"
version: "0.14.0"
doi: "10.5281/zenodo.19080238"
status: "Active"
created: "2026-02-19"
updated: "2026-09-07"

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
  - "CRI-CORE v0.14.0"
  - "Deterministic Enforcement Kernel"
  - "Execution Boundary Enforcement"
---

<p align="center">
  <img src="https://raw.githubusercontent.com/Waveframe-Labs/.github/main/assets/branding/canon_wf_logo_extended.png" width="700">
</p>

# CRI-CORE — Execution Boundary Enforcement Kernel

**0.14.0 release candidate:** package publication and external verification are
pending. See the [0.14.0 changelog](CHANGELOG.md#v0140-2026-09-07) for release
notes. Python 3.10 and newer remain supported.

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

The canonical call enforces strictly when mode is omitted. Supply the integrity
and publication context required by the existing policy stages.

```python
from cricore.api import evaluate_structured

result = evaluate_structured(
    proposal=proposal,
    compiled_contract=compiled_contract,
    run_context=run_context,
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

Omitting the function's `mode` selects `"strict"`. The only supported values are
exactly `"strict"` and `"local"`. `None`, other types, unknown strings, empty
strings, case aliases, and whitespace variants raise `ValueError` with the stable
`CRI_MODE_INVALID` diagnostic. Values are never normalized.

If `run_context["mode"]` is present, it must match the function mode exactly
(including the default `"strict"`). A mismatch raises `ValueError` with
`CRI_MODE_CONFLICT` before any policy stage runs. Remove the context declaration
or make both declarations identical. Context alone cannot select local mode.
A configuration exception must block execution.

---

### 4. Deterministic Outputs

Identical inputs produce identical decisions and policy stage traces.
Stage `checked_at_utc` fields record observation time and may differ.

Payload generation is byte-stable across runs.

---

### 5. Full Decision Trace

Every evaluation returns a complete stage-by-stage trace.

No hidden logic.

---

## Execution Modes

### Strict (default enforcement)

* all existing required conditions must pass
* absent integrity or publication context blocks the commit decision
* no soft failures authorize execution

This selects the existing strict policy checks; integrity/publication evidence
sufficiency semantics are unchanged. Absent sections fail, but empty mappings
still satisfy those stages. This release does **not** claim that empty
integrity/publication mappings provide cryptographic provenance verification
or verify published authority. [CRI #4](https://github.com/Waveframe-Labs/CRI-CORE/issues/4)
separately tracks evidence-sufficiency semantics and is not implemented here.

### Local (explicit advisory evaluation)

```python
result = evaluate_structured(
    proposal=proposal,
    compiled_contract=compiled_contract,
    run_context=run_context,
    mode="local",
)
# Inspect advisory diagnostics only. Never use this result to execute a mutation.
```

Local evaluation retains the existing advisory behavior: missing integrity or
publication context produces messages without blocking, and those stages' soft
failures do not block the advisory decision. **Advisory results must never
authorize a mutation**, even when `commit_allowed` is `True`. If the context
includes a mode, it must also be `"local"` for this call.

### Migration to CRI-CORE 0.14.0

Callers that omitted mode now receive strict enforcement. Provide the required
context and handle blocked decisions or configuration exceptions before execution.
Callers that previously selected advisory behavior with only
`run_context["mode"] = "local"` must explicitly pass `mode="local"` for advisory
use, or remove/change the context mode for strict enforcement. Passing `None`
is no longer equivalent to omission.

The same contract applies to `cricore.api.evaluate`, `run_execution_pipeline`,
`run_enforcement_pipeline`, root exports, the retained `evaluate_core` and
`evaluate_proposal` wrappers, and directly imported mode-sensitive stage helpers.
`governed_execute` always uses strict evaluation; it has no advisory execution opt-in.
The canonical API implementation is the `cricore.api` package; the shadowed
`src/cricore/api.py` implementation has been removed.

Guard 0.17 remains compatible **after Guard PR #40** (verified at commit
`2c4a77f89bb234fbde32937435535cffec4dc905`): its retained legacy permission and
execution APIs fail closed with `GUARD_LEGACY_EXECUTION_UNSUPPORTED`. This is a
commit-qualified compatibility statement, not a claim about an older published
0.17 artifact that lacks PR #40. Modern Guard local/cloud/repository behavior and
Ledger authority verification remain separate and unchanged. **Guard 0.18** will
be the coordinated recommended Guard release.

[CRI #2](https://github.com/Waveframe-Labs/CRI-CORE/issues/2) stays open until
0.14.0 is published and externally verified.
[Guard #39](https://github.com/Waveframe-Labs/Waveframe-Guard/issues/39) stays open
pending CRI-CORE 0.14.0 and Guard 0.18.0 releases. This candidate preparation does
not publish either package.

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
