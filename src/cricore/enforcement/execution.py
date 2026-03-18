"""
---
title: "CRI-CORE Enforcement Pipeline Orchestrator"
filetype: "operational"
type: "specification"
domain: "enforcement"
version: "0.4.2"
doi: "TBD-0.4.2"
status: "Active"
created: "2026-02-10"
updated: "2026-03-17"

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
  - "CRI-CORE-EnforcementPipeline-v0.4.2"
---
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, List, Mapping, Optional, Tuple

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
        messages=["blocked: structure stage did not pass (version gate cannot be satisfied)"],
        checked_at_utc=structure_stage.checked_at_utc,
        engine_version=None,
    )


def _make_contract_hash_gate_stage(
    run_path: str,
    *,
    version_gate_stage: StageResult,
) -> StageResult:

    proposal_path = Path(run_path) / "proposal.json"
    compiled_contract_path = Path(run_path) / "compiled_contract.json"

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
        with proposal_path.open() as f:
            proposal = json.load(f)

        with compiled_contract_path.open() as f:
            compiled_contract = json.load(f)

        proposal_hash = proposal["contract"]["hash"]
        contract_hash = compiled_contract["contract_hash"]

        if proposal_hash != contract_hash:
            return StageResult(
                stage_id="structure-contract-hash-gate",
                passed=False,
                failure_classes=["contract-hash-mismatch"],
                messages=["proposal contract hash does not match compiled contract artifact"],
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


def run_enforcement_pipeline(
    run_path: str,
    *,
    expected_contract_version: Optional[str] = None,
    run_context: Optional[Mapping[str, Any]] = None,
) -> Tuple[List[StageResult], bool]:

    results: List[StageResult] = []

    # 1) Structure
    structure_res = run_structure_stage(
        run_path,
        expected_contract_version=expected_contract_version,
    )
    results.append(structure_res)

    # 2) Version gate
    version_gate_res = _make_version_gate_stage(
        expected_contract_version=expected_contract_version,
        structure_stage=structure_res,
    )
    results.append(version_gate_res)

    # 3) Contract hash gate (FIXED)
    hash_gate_res = _make_contract_hash_gate_stage(
        run_path,
        version_gate_stage=version_gate_res,
    )
    results.append(hash_gate_res)

    # 4) Independence
    independence_res = run_independence_stage(
        run_path,
        run_context=run_context,
    )
    results.append(independence_res)

    # 5) Integrity
    integrity_res = run_integrity_stage(
        run_path,
        run_context=run_context,
    )
    results.append(integrity_res)

    # 6) Integrity finalization
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

    # 8) Publication commit
    commit_res = run_publication_commit_stage(
        run_path,
        prior_stage_results=results,
    )
    results.append(commit_res)

    commit_allowed = commit_res.passed

    return results, commit_allowed