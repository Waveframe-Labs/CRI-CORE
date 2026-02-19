"""
---
title: "CRI-CORE Enforcement Pipeline Orchestrator"
filetype: "operational"
type: "specification"
domain: "enforcement"
version: "0.4.0"
doi: "TBD-0.4.0"
status: "Active"
created: "2026-02-10"
updated: "2026-02-19"

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
ai_assistance_details: "AI-assisted canonical pipeline alignment including lifecycle contract conformity stage and prerequisite-aware gates."

dependencies:
  - "../run/structure.py"
  - "./lifecycle.py"
  - "./independence.py"
  - "./integrity.py"
  - "./publication.py"
  - "../results/stage.py"

anchors:
  - "CRI-CORE-EnforcementPipeline-v0.4.0"
---
"""

from __future__ import annotations

from typing import Any, List, Mapping, Optional

from ..results.stage import StageResult
from ..run.structure import run_structure_stage
from .lifecycle import run_lifecycle_conformity_stage
from .independence import run_independence_stage
from .integrity import run_integrity_stage, run_integrity_finalization_stage
from .publication import run_publication_stage, run_publication_commit_stage


def _make_version_gate_stage(
    *,
    expected_contract_version: Optional[str],
    structure_stage: StageResult,
) -> StageResult:
    """
    Represent the structure contract version gate as a distinct stage result.

    Conservative logic:
      - if expected_contract_version is None → gate passes (skipped)
      - else → gate passes only if structure stage passed
    """

    if expected_contract_version is None:
        return StageResult(
            stage_id="structure-contract-version-gate",
            passed=True,
            failure_classes=[],
            messages=["skipped: no expected_contract_version provided"],
            checked_at_utc=structure_stage.checked_at_utc,
            engine_version=None,
        )

    if structure_stage.passed:
        return StageResult(
            stage_id="structure-contract-version-gate",
            passed=True,
            failure_classes=[],
            messages=[],
            checked_at_utc=structure_stage.checked_at_utc,
            engine_version=None,
        )

    return StageResult(
        stage_id="structure-contract-version-gate",
        passed=False,
        failure_classes=structure_stage.failure_classes,
        messages=["blocked: structure stage did not pass (version gate cannot be satisfied)"],
        checked_at_utc=structure_stage.checked_at_utc,
        engine_version=None,
    )


def run_enforcement_pipeline(
    run_path: str,
    *,
    expected_contract_version: Optional[str] = None,
    run_context: Optional[Mapping[str, Any]] = None,
) -> List[StageResult]:
    """
    Execute the canonical CRI-CORE enforcement pipeline.

    Canonical 8-stage order (v0.4.x):

      1. run-structure
      2. structure-contract-version-gate
      3. lifecycle-contract-conformity
      4. independence
      5. integrity
      6. integrity-finalization
      7. publication
      8. publication-commit

    Properties:
      - All stages always emit results
      - Later stages may be blocked by earlier failures
      - publication-commit hard-gates on ALL prior stages
    """

    results: List[StageResult] = []

    # 1) Structural invariant validation
    structure_res = run_structure_stage(
        run_path,
        expected_contract_version=expected_contract_version,
    )
    results.append(structure_res)

    # 2) Explicit version gate stage
    version_gate_res = _make_version_gate_stage(
        expected_contract_version=expected_contract_version,
        structure_stage=structure_res,
    )
    results.append(version_gate_res)

    # 3) Lifecycle contract conformity
    lifecycle_res = run_lifecycle_conformity_stage(
        run_path,
        run_context=run_context,
    )
    results.append(lifecycle_res)

    # 4) Independence enforcement
    independence_res = run_independence_stage(
        run_path,
        run_context=run_context,
    )
    results.append(independence_res)

    # 5) Integrity enforcement (non-mutating)
    integrity_res = run_integrity_stage(
        run_path,
        run_context=run_context,
    )
    results.append(integrity_res)

    # 6) Integrity finalization (mutating)
    finalization_res = run_integrity_finalization_stage(
        run_path,
        run_context=run_context,
        prerequisite_passed=integrity_res.passed,
    )
    results.append(finalization_res)

    # 7) Publication validation
    publication_res = run_publication_stage(
        run_path,
        run_context=run_context,
    )
    results.append(publication_res)

    # 8) Publication commit (hard gate on ALL prior results)
    commit_res = run_publication_commit_stage(
        run_path,
        prior_stage_results=results,
    )
    results.append(commit_res)

    return results
