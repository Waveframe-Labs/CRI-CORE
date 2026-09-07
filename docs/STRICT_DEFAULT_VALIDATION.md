# Strict-default correction: issues #1 and #2

## Baseline and public surface inventory

Before editing, `git fetch origin` succeeded and both `origin/main` and branch
`security/strict-enforcement-default` were exactly
`28bc5636e4edadc6442cb003cb91df091286cb05`. The tracked worktree was clean.
No applicable AGENTS.md was present.

| Importable surface | Baseline mode path | Corrected contract |
| --- | --- | --- |
| `cricore.api.evaluate_structured` / `cricore.api.evaluate.evaluate_structured` | `None` forwarded to execution pipeline | Default `"strict"`; explicit `"local"` only |
| `cricore.enforcement.execution.run_execution_pipeline` | Non-None argument, else dict context mode, else `"local"` | Validate argument and context before the first stage |
| `cricore.api.evaluate` / `cricore.api.evaluate.evaluate` | No mode argument; forwarded context to run-path pipeline | Same strict-default argument and validation |
| `cricore.enforcement.execution.run_enforcement_pipeline` | No mode argument; context argument or `run_context.json` selected mode | Context source selection retained; context cannot downgrade default strict |
| Root `cricore.evaluate`, `cricore.run_enforcement_pipeline` | Aliases of the above | Same functions and contract; root additionally exports canonical `evaluate_structured` |
| `cricore.interface.evaluate_core.evaluate_core` | Explicitly defaulted to `"local"`, overriding context | Default strict; validates before forwarding |
| `cricore.interface.evaluate_proposal.evaluate_proposal` | Proposal's embedded context forwarded through filesystem evaluation | Default strict; validates embedded context before filesystem scaffolding |
| `cricore.interface.governed_execute.governed_execute` | Used proposal wrapper's advisory decision to gate callback | Retained signature; always strict; no local execution opt-in |
| `run_integrity_stage`, `run_publication_stage` | Context `"local"` softened missing sections | Same policy checks; shared strict-default argument validation |
| `run_integrity_finalization_stage`, `run_publication_commit_stage` | Missing or any non-`"strict"` mode softened prerequisite failures | Same valid-mode semantics; invalid/default paths corrected |

`run_structure_stage`, version/hash gates, and `run_independence_stage` do not
select execution mode. The separate repository integrity helpers' manifest
presence behavior does not select a pipeline execution mode or authorize commits;
it is unchanged. Loader/validator modules and the empty CLI package expose no
additional whole-proposal execution decision entry point.

### Mode path inventory

At the baseline, omission and explicit `None` were indistinguishable. A dict
context could select local or strict; a non-dict Mapping's mode was ignored by
the pipeline. Explicit function values silently replaced conflicting context.
Unknown strings, case/whitespace variants, empty strings, booleans, numbers,
bytes, lists, and dicts were not validated. Non-strict values could soften the
final commit decision even when the integrity/publication stages failed.

Now omission supplies the literal default `"strict"`. Only exact built-in
strings `"strict"` and `"local"` pass validation. Every present declaration is
validated, including a context value that would previously have been ignored.
Matching declarations pass; mismatches raise `ValueError` with
`CRI_MODE_CONFLICT`. Invalid declarations raise `CRI_MODE_INVALID` without
printing caller data. Invalid context container types raise
`CRI_RUN_CONTEXT_INVALID`. No policy stages run on mode configuration failure.

### The API collision

Normal source imports selected `src/cricore/api/__init__.py`; the root imported
`cricore.api.evaluate`. A fresh baseline build nevertheless shipped all three:

```text
cricore/api.py
cricore/api/__init__.py
cricore/api/evaluate.py
```

The shadowed file offered contradictory filesystem convenience behavior and an
`evaluate_run` name unavailable through normal package imports. Repository-wide
reference inspection found no supported import depending on it. It was removed
from source and distributions; no file-based import compatibility is invented.
`tools/check_distribution.py` requires identical source/wheel/sdist Python/schema
inventories and rejects `cricore/api.py`. Canonical import identity is checked
both in the active suite and in an isolated wheel installation.

## Reproduction and regressions

`tests/fixtures/issue2_baseline.json` preserves the original inputs, decisions,
messages, and stage order captured from the required base before editing.
With valid contract identity and roles but absent integrity/publication context:

| Selection | Baseline `commit_allowed` | Candidate |
| --- | --- | --- |
| Omitted | `True` | `False` |
| Explicit strict | `False` | `False` |
| Explicit local | `True` | `True` (advisory only) |
| Invalid `"STRICT"` | `True` despite failed stages | `CRI_MODE_INVALID` |

The committed regression
`test_issue2_reproduction_matches_preserved_baseline` was also run with
`PYTHONPATH` pointing to a clean archive of the required base. It failed with
`AssertionError: assert True is False` on the omitted-mode decision, then passed
with the candidate. This proves the regression detects the original behavior.

Tests cover each public surface, invalid function/context/both declarations,
conflicts before every stage, separate missing integrity and publication
sections, existing strict success conditions, advisory soft failures, callback
blocking, input immutability, and deterministic decisions and policy traces.
Trace comparison excludes only the existing `checked_at_utc` observation time;
stage IDs, order, pass/fail, failure classes, messages, and engine version match.
No stage requirements or evidence-validation semantics were redesigned.

## Local validation

On Windows, Python 3.14.4 and 3.10.18 each passed the complete active CRI suite:
**668 passed, 3 skipped**. One skip is the repository's existing legacy-suite
exclusion; two skip non-JSON bytes in a disk context (bytes remain tested through
function arguments and in-memory contexts). Compilation and `pip check` passed.

Both runtimes built wheel and sdist, passed Twine checks, matched all **40**
Python/schema files across source/wheel/sdist, and passed isolated clean-wheel
canonical-import and strict/default/local checks. Build artifacts and isolated
environments are outside the tracked repository. Runtime dependencies remain
empty; compiler/normalizer requirements used by the existing active tests are
now declared in the development extra.

The complete CRI suite also passed against the installed wheel on both runtimes
(`python -I -m pytest .../tests --import-mode=importlib` from outside the source
checkout): **668 passed, 3 skipped** each.

The declared validation dependency set passed `pip-audit` with no known
vulnerabilities after updating the initial pip/setuptools tool pins to patched
26.2.1/83.0.0. A changed-file secret-pattern scan found no credentials or private
keys. Diff/artifact audits found no generated binaries, environments, unrelated
source changes, archived workflow changes, or release/version metadata changes.
`git diff --check` passed. These are scoped checks of the candidate, not a claim
that unrelated historical repository contents were comprehensively audited.

Active CI validates Python 3.10 and 3.14 on PRs to main and pushes to main,
cancels superseded runs, pins Actions by immutable SHA and direct validation
dependencies by version, and includes the exact Guard compatibility target.
No archived workflow or publication step is restored.

## Exact Guard compatibility

Guard was cloned into a separate temporary checkout, detached at exactly
`2c4a77f89bb234fbde32937435535cffec4dc905`. The CRI candidate wheel was installed
in separate Guard environments, verified under `site-packages`, and compared
byte-for-byte with the candidate's runtime source inventory.

The complete applicable Guard suite (`python -m pytest -q -rs`) passed:

| Environment | Result |
| --- | --- |
| Windows Python 3.14.4, Ledger 0.8.0 | 741 passed, 19 skipped |
| Windows Python 3.10.18, minimum Ledger 0.7.0 | 682 passed, 78 skipped |

Skips are explicit Linux namespace/replacement checks, unavailable Windows
symlink privileges, and Ledger 0.8-only cases in the minimum-dependency run.
The active Ubuntu CI matrix exercises the Linux cases against the same Guard
commit and candidate wheel. Modern local/cloud, guarded tools, and repository
adapter regressions are included in the full suite. Guard source is unchanged.

Guard's `tools.security.reproduce_issue39` was run separately against the actual
installed candidate, outside its strict-mode test fixture. It reported:

```text
strict_control_allowed: false
strict_control_failed_stages: integrity, integrity-finalization,
                             publication, publication-commit
execute_error: GUARD_LEGACY_EXECUTION_UNSUPPORTED
execute_proposal_error: GUARD_LEGACY_EXECUTION_UNSUPPORTED
callback_count: 0
runtime_allowed_events: 0
```

The retained execution/permission API matrix additionally covers decorated
execution, `GovernedRuntime`/`GuardRuntime` execute/execute_proposal/evaluate/
revalidate, and `evaluate_admissibility`, with no CRI evaluation, authority
resolution, callback, allowed event, or successful execution evidence.

Compatibility evidence is also posted to Guard issue #39. That issue and CRI
issues #1/#2 remain open. Recommend CRI-CORE **0.14.0**, coordinated with Guard's
planned **0.18.0**; release/version/tag publication is separate work.
