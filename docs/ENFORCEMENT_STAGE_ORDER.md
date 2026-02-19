---
title: "CRI-CORE Canonical Enforcement Stage Order"
filetype: "documentation"
type: "specification"
domain: "enforcement"
version: "0.1.0"
status: "Active"
created: "2026-02-19"
updated: "2026-02-19"
license: "Apache-2.0"
---

# Canonical Enforcement Stage Order

The CRI-CORE enforcement pipeline executes the following stages in fixed, normative order:

1. run-structure
2. structure-contract-version-gate
3. lifecycle-contract-conformity
4. independence
5. integrity
6. integrity-finalization
7. publication
8. publication-commit

## Normative Guarantees

- All stages are emitted in order.
- No stage may be skipped.
- Later stages may be blocked by prior failures.
- `publication-commit` is the sole commit gate.
- `commit_allowed` is defined as the pass state of `publication-commit`.

Stage identifiers are defined in:

`cricore/enforcement/stage_ids.py`

This ordering is considered part of the CRI-CORE enforcement contract surface.
