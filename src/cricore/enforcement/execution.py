"""
---
title: "CRI-CORE Enforcement Pipeline Orchestrator"
filetype: "operational"
type: "specification"
domain: "enforcement"
version: "0.4.3"
doi: "TBD-0.4.3"
status: "Active"
created: "2026-02-10"
updated: "2026-03-19"

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
  - "../run/structure.py"
  - "./independence.py"
  - "./integrity.py"
  - "./publication.py"
  - "../results/stage.py"

anchors:
  - "CRI-CORE-EnforcementPipeline-v0.4.3"
---
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, List, Mapping, Optional, Tuple

from ..results.model import EvaluationResult
from ..results.stage import StageResult
from ..run.structure import run_structure_stage
from .independence import run_independence_stage
from .integrity import run_integrity_stage, run_integrity_finalization_stage
from .publication import run_publication_stage, run_publication_commit_stage


def _make_version_gate_stage(
    *,
    expected_contract_version: Optional[str],
    structure_stage: StageResult,
) -> StageResult:
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
        messages=[
            "blocked: structure stage did not pass (version gate cannot be satisfied)"
        ],
        checked_at_utc=structure_stage.checked_at_utc,
        engine_version=None,
    )


def _make_contract_hash_gate_stage(
    *,
    proposal: Mapping[str, Any],
    compiled_contract: Mapping[str, Any],
    version_gate_stage: StageResult,
) -> StageResult:
    if not version_gate_stage.passed:
        return StageResult(
            stage_id="structure-contract-hash-gate",
            passed=False,
            failure_classes=["blocked"],
            messages=["blocked: version gate failed"],
            checked_at_utc=version_gate_stage.checked_at_utc,
            engine_version=None,
        )

    try:
        proposal_hash = proposal["contract"]["hash"]
        compiled_contract_hash = compiled_contract["contract_hash"]

        if proposal_hash != compiled_contract_hash:
            return StageResult(
                stage_id="structure-contract-hash-gate",
                passed=False,
                failure_classes=["contract-hash-mismatch"],
                messages=[
                    "proposal contract hash does not match compiled contract artifact"
                ],
                checked_at_utc=version_gate_stage.checked_at_utc,
                engine_version=None,
            )

        return StageResult(
            stage_id="structure-contract-hash-gate",
            passed=True,
            failure_classes=[],
            messages=[],
            checked_at_utc=version_gate_stage.checked_at_utc,
            engine_version=None,
        )

    except Exception as exc:
        return StageResult(
            stage_id="structure-contract-hash-gate",
            passed=False,
            failure_classes=["contract-hash-validation-error"],
            messages=[str(exc)],
            checked_at_utc=version_gate_stage.checked_at_utc,
            engine_version=None,
        )


def run_execution_pipeline(
    *,
    proposal: Mapping[str, Any],
    compiled_contract: Mapping[str, Any],
    run_context: Mapping[str, Any],
    mode: Optional[str] = None,
    expected_contract_version: Optional[str] = None,
) -> EvaluationResult:
    """
    Execute the canonical CRI-CORE enforcement pipeline.

    Returns:
        (results, commit_allowed)

    commit_allowed is TRUE if and only if the publication-commit stage passes.
    """
    effective_run_context = dict(run_context or {})
    if mode is not None:
        effective_mode = mode
    elif isinstance(run_context, dict) and "mode" in run_context:
        effective_mode = run_context["mode"]
    else:
        effective_mode = "local"
    effective_run_context["mode"] = effective_mode

    stage_results: List[StageResult] = []

    # 1) Structure
    structure_res = run_structure_stage(
        proposal=proposal,
        compiled_contract=compiled_contract,
        expected_contract_version=expected_contract_version,
    )
    stage_results.append(structure_res)

    # 2) Version gate
    version_gate_res = _make_version_gate_stage(
        expected_contract_version=expected_contract_version,
        structure_stage=structure_res,
    )
    stage_results.append(version_gate_res)

    # 3) Contract hash gate
    hash_gate_res = _make_contract_hash_gate_stage(
        proposal=proposal,
        compiled_contract=compiled_contract,
        version_gate_stage=version_gate_res,
    )
    stage_results.append(hash_gate_res)

    # 4) Independence
    independence_res = run_independence_stage(
        proposal=proposal,
        compiled_contract=compiled_contract,
        run_context=effective_run_context,
    )
    stage_results.append(independence_res)

    # 5) Integrity
    integrity_res = run_integrity_stage(
        proposal=proposal,
        compiled_contract=compiled_contract,
        run_context=effective_run_context,
    )
    stage_results.append(integrity_res)

    # 6) Integrity finalization
    finalization_res = run_integrity_finalization_stage(
        proposal=proposal,
        compiled_contract=compiled_contract,
        run_context=effective_run_context,
        prerequisite_passed=integrity_res.passed,
    )
    stage_results.append(finalization_res)

    # 7) Publication validation
    publication_res = run_publication_stage(
        proposal=proposal,
        compiled_contract=compiled_contract,
        run_context=effective_run_context,
    )
    stage_results.append(publication_res)

    # 8) Publication commit
    commit_res = run_publication_commit_stage(
        proposal=proposal,
        compiled_contract=compiled_contract,
        prior_stage_results=stage_results,
        run_context=effective_run_context,
    )
    stage_results.append(commit_res)

    commit_allowed = commit_res.passed
    failed_stages = [
        stage.stage_id
        for stage in stage_results
        if not stage.passed
    ]

    summary = (
        "Commit allowed"
        if commit_allowed
        else f"Commit blocked due to failures in: {', '.join(failed_stages)}"
    )

    return EvaluationResult(
        commit_allowed=commit_allowed,
        failed_stages=failed_stages,
        summary=summary,
        stage_results=stage_results,
    )


def run_enforcement_pipeline(
    run_path: str,
    *,
    expected_contract_version: Optional[str] = None,
    run_context: Optional[Mapping[str, Any]] = None,
) -> Tuple[List[StageResult], bool]:
    """
    Backward-compatible run-path pipeline entrypoint.
    """

    proposal_path = Path(run_path) / "proposal.json"
    compiled_contract_path = Path(run_path) / "compiled_contract.json"

    with proposal_path.open("r", encoding="utf-8") as f:
        proposal = json.load(f)

    with compiled_contract_path.open("r", encoding="utf-8") as f:
        compiled_contract = json.load(f)

    if run_context is None:
        run_context_path = Path(run_path) / "run_context.json"
        if run_context_path.exists():
            with run_context_path.open("r", encoding="utf-8") as f:
                run_context = json.load(f)

    result = run_execution_pipeline(
        proposal=proposal,
        compiled_contract=compiled_contract,
        run_context=run_context or {},
        expected_contract_version=expected_contract_version,
    )

    return result.stage_results, result.commit_allowed
